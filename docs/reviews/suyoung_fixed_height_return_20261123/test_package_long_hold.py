"""Verify the operator package against the actual pinned block; use a stub commit, never a solver."""
import argparse
import base64
import importlib.util
import io
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("package_long_hold", Path(__file__).with_name("package_long_hold.py"))
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


def extract(raw):
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as reader:
        members = reader.getmembers()
        assert len({m.name for m in members}) == len(members) and all(m.isfile() for m in members)
        return {m.name: reader.extractfile(m).read() for m in members}


def embedded(block, marker):
    header, tail = block.split(b"<<'" + marker + b"'\n", 1)
    payload, footer = tail.split(b'\n' + marker + b'\n', 1)
    archive = base64.b64decode(b''.join(payload.splitlines()), validate=True)
    assert package.digest(archive).encode('ascii') in footer
    return header, extract(archive), footer


class OperatorBlockTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pin = 'abcd' * 10
        self.runner = Path(__file__).with_name('run_long_hold.sh').read_bytes()
        driver = b'raise SystemExit("package test stub")\n'
        self.tree = {package.FOLDER + 'long_hold.py': driver, package.FOLDER + 'run_long_hold.sh': self.runner}
        self.git_calls = []

    def git(self, args):
        self.git_calls.append(args)
        if 'rev-parse' in args:
            self.assertEqual(args[-1], 'demo^{commit}')
            return (self.pin + '\n').encode('ascii')
        self.assertEqual(['show', self.pin], [args[-2], args[-1].split(':', 1)[0]])
        return self.tree[args[-1].split(':', 1)[1]]

    def build(self, output):
        with patch.object(package.subprocess, 'check_output', side_effect=self.git), \
             patch.object(package.subprocess, 'run') as ancestor:
            result = package.build(self.root, PREVIOUS, output, 'demo')
        self.assertEqual(ancestor.call_args.args[0][-4:], ['merge-base', '--is-ancestor', package.BASE, self.pin])
        self.assertTrue(ancestor.call_args.kwargs['check'])
        return result

    def test_frozen_sources_and_reproducible_block(self):
        path, digest, _ = self.build(self.root / 'release')
        self.assertEqual(path.name, 'PASTE_SUYOUNG_LONG_HOLD_abcdabcdabcd_1123.txt')
        self.assertEqual(path.with_suffix('.txt.sha256').read_bytes(), f'{digest}  {path.name}\n'.encode('ascii'))
        data = path.read_bytes()
        self.assertEqual(package.digest(data), digest)
        header, files, footer = embedded(data, b'LONG_HOLD_SOURCES')
        self.assertIn(b'[[ $# -eq 7', header)
        self.assertIn(b'GO_SUYOUNG_LONG_HOLD_ONCE', header)
        self.assertIn(b'run_long_hold.sh "$1" "$depth" "$prior" "$material" "$baseline" "$quarter" "$fixed"', footer)
        _, previous, _ = embedded(PREVIOUS.read_bytes(), b'FIXED_HEIGHT_SOURCES')
        self.assertEqual(files.pop('SOURCE_SHA256SUMS'), package.manifest(files))
        self.assertEqual(files.pop('RELEASE'), (self.pin + '\n').encode('ascii'))
        for name, contents in self.tree.items():
            self.assertEqual(files.pop(name), contents)
        self.assertEqual(files, {'history/' + name: contents for name, contents in previous.items()})
        self.assertEqual(files['history/RELEASE'].decode().strip(), package.BASE)
        self.assertIn('history/history/history/history/history/RELEASE', files)
        self.assertEqual(self.build(self.root / 'release')[0].read_bytes(), data)
        self.assertEqual(self.build(self.root / 'another')[0].read_bytes(), data)

    def test_modified_source_block_and_source_archive_rejected(self):
        changed = self.root / 'altered.txt'
        changed.write_bytes(PREVIOUS.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'operator block'):
            package.previous_sources(changed)
        with patch.object(package, 'ARCHIVE_SHA', '0' * 64), self.assertRaisesRegex(ValueError, 'source archive'):
            package.previous_sources(PREVIOUS)

    def test_existing_different_output_preserved(self):
        path, _, _ = self.build(self.root)
        path.write_bytes(b'existing user file')
        with self.assertRaises(FileExistsError):
            self.build(self.root)
        self.assertEqual(path.read_bytes(), b'existing user file')

    def test_once_mode_and_measurement_contract(self):
        runner = self.runner.decode('ascii')
        for literal in ('--depth "$depth" --prior "$prior" --material "$material" --baseline "$baseline" --quarter "$quarter"',
                        'F12_RAMP_STEPS=1638', 'F24_RAMP_STEPS=3276', 'F12_HOLD_STEPS=4800', 'F24_HOLD_STEPS=9600', 'RAMP_SPEED_RATIO=0.25', 'HOLD_SPEED=0', 'F12_BUDGET_SECONDS=2400', 'F24_BUDGET_SECONDS=7200',
                        'WATCHDOG_GRACE_SECONDS=30', 'RETRIES=0', '12) watchdog=2430', '24) watchdog=7230',
                        'taskset -c "$cpu"', 'OPENBLAS_NUM_THREADS=1', 'OMP_NUM_THREADS=1',
                        'suyoung_long_hold_result.tar.gz', 'LONG_HOLD_READBACK_COMPLETE'):
            self.assertIn(literal, runner)
        self.assertEqual(runner.count('"$'+'{app[@]}" arm'),1)
        self.assertIn('for cells in 12 24; do',runner)
        self.assertIn('--cells "$cells"',runner)
        for name in ('depth', 'prior', 'material', 'baseline', 'quarter','fixed'):
            self.assertRegex(runner, re.compile('^' + name + '_hash=[0-9a-f]{64}$', re.M))
            self.assertIn('$(sha256sum < "$' + name + '")', runner)
        positions = [runner.index(text) for text in ('"${app[@]}" check', '== CHECK_ONLY', 'mkdir -- "$once"',
                    'trap finish EXIT', '"${app[@]}" arm', '"${app[@]}" summary')]
        self.assertEqual(sorted(positions), positions)

    @unittest.skipIf(os.name == "nt","GNU userland shell integration runs on the WSL operator platform")
    def test_shell_runs_stub_once_preserves_partial_return_and_does_not_launch_from_check(self):
        # The reference driver is replaced by a test interpreter; native physics never runs.
        bash = shutil.which("bash")
        if not bash:
            self.skipTest("Bash unavailable")
        body = self.runner.decode("ascii")
        files = {"RELEASE": (self.pin+"\n").encode("ascii")}
        for depth,pin_name in enumerate(("fixed","quarter","depth","previous","material","balance"),1):
            pin = re.search(r"^"+pin_name+r"_pin=([0-9a-f]{40})$",body,re.M).group(1)
            files["history/"*depth+"RELEASE"] = (pin+"\n").encode("ascii")
        for name in ("depth","prior","material","baseline","quarter","fixed"):
            contents = name.encode("ascii")
            (self.root/(name+".tar")).write_bytes(contents)
            body = re.sub(r"^"+name+r"_hash=[0-9a-f]{64}$",name+"_hash="+package.digest(contents),body,flags=re.M)
        files["SOURCE_SHA256SUMS"] = package.manifest(files)
        for name,raw in files.items():
            dest=self.root/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(raw)
        runner=self.root/"runner.sh"
        runner.write_bytes(body.encode("ascii"))
        def script(name, text):
            dest=self.root/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(("#!/usr/bin/env bash\nset -euo pipefail\n"+text+"\n").encode("ascii"))
            dest.chmod(0o755)
        script("home/Yonghoon-DEM-DFT/venv/bin/python", """
if [[ "$3" == -c ]]; then printf '0\\n'; exit 0; fi
shift 3
mode=$1; shift
run=missing; cells=0
while [[ $# -gt 0 ]]; do
    case "$1" in --run) run=$2;; --cells) cells=$2;; esac
    shift 2
done
printf '%s %s\\n' "$mode" "$cells" >> "$HOME/mock_calls"
if [[ "$mode" == arm && "$cells" == 24 && "${STUB_FAIL:-}" == yes ]]; then exit 7; fi
if [[ "$mode" == summary ]]; then printf '{}\\n' > "$run/summary.json"; fi""")
        script("bin/taskset", 'shift 2; exec "$@"')
        script("bin/timeout", 'shift 2; exec "$@"')
        cmd = ('export HOME="$PWD/home" PATH="$PWD/bin:$PATH" STUB_FAIL="$2"; '
               'bash runner.sh "$1" depth.tar prior.tar material.tar baseline.tar quarter.tar fixed.tar')
        def run(mode,fail="no"):
            return subprocess.run([bash,"-c",cmd,"sh",mode,fail],cwd=self.root,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        before=run("CHECK_ONLY")
        self.assertEqual(before.returncode,0,before.stdout)
        home=self.root/"home"
        self.assertFalse(any(home.glob("suyoung_long_hold_once_*")))
        first=run("GO_SUYOUNG_LONG_HOLD_ONCE","yes")
        self.assertEqual(first.returncode,7,first.stdout)
        ret, = home.glob("suyoung_long_hold_return_*")
        armed=home/"mock_calls"
        with tarfile.open(ret/"suyoung_long_hold_result.tar.gz","r:gz") as archive:
            self.assertIn(b'"phase":"F24","rc":7',archive.extractfile("run/incomplete.json").read())
        self.assertEqual(armed.read_text().splitlines().count("arm 24"),1)
        again=run("GO_SUYOUNG_LONG_HOLD_ONCE")
        self.assertNotEqual(again.returncode,0)
        self.assertEqual(armed.read_text().splitlines().count("arm 24"),1)
        # Another scratch operator home demonstrates the successful path.
        home.rename(self.root/"first_fixture_home")
        (home/"Yonghoon-DEM-DFT/venv/bin").mkdir(parents=True)
        shutil.copy2(self.root/"first_fixture_home/Yonghoon-DEM-DFT/venv/bin/python",
                     home/"Yonghoon-DEM-DFT/venv/bin/python")
        good=run("GO_SUYOUNG_LONG_HOLD_ONCE")
        self.assertEqual(good.returncode,0,good.stdout)
        self.assertEqual(armed.read_text().splitlines(),["check 0","arm 12","arm 24","summary 0"])
        self.assertIn("LONG_HOLD_READBACK_COMPLETE",good.stdout)
        success, = home.glob("suyoung_long_hold_return_*")
        sums=(success/"SHA256SUMS").read_text().splitlines()
        self.assertEqual(len(sums),2)
        for line in sums:
            digest,name=line.split("  ")
            self.assertEqual(digest,package.digest((success/name).read_bytes()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('previous_block', type=Path)
    PREVIOUS = parser.parse_args().previous_block.resolve()
    unittest.main(argv=[sys.argv[0]], verbosity=2)
