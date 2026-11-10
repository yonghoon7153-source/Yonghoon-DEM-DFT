// Test-first regression. Evaluate exact source fragments, never the viewer module.
// Native Node builtins only; tiny THREE records geometry/material call contracts.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const PIN = 'c571a27119ace92ca34d3d6f2b61135219a3f1b4';
const BASELINE_SHA = '015677ba072ab15d5b22c2f4b33767fe54dbd32ca00ab1ba590c2692e89e040e';
const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_SOURCE = resolve(HERE, '../source_snapshot/webapp/static/js/viewer3d.js');
const options = { source: DEFAULT_SOURCE, baseline: DEFAULT_SOURCE };
const argv = process.argv.slice(2);
assert.equal(argv.length % 2, 0, 'expected --source FILE and optional --baseline FILE');
for (let i = 0; i < argv.length; i += 2) {
  assert.ok(['--source', '--baseline'].includes(argv[i]), 'unsupported argument');
  options[argv[i].slice(2)] = resolve(argv[i + 1]);
}
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const baselineBytes = readFileSync(options.baseline);
const sourceBytes = readFileSync(options.source);
assert.equal(sha256(baselineBytes), BASELINE_SHA, 'frozen baseline identity differs');
const utf8 = new TextDecoder('utf-8', { fatal: true });
const baseline = utf8.decode(baselineBytes);
const source = utf8.decode(sourceBytes);

function uniqueIndex(text, marker) {
  const first = text.indexOf(marker);
  assert.ok(first >= 0, `missing extraction marker: ${marker}`);
  assert.equal(text.indexOf(marker, first + marker.length), -1, `ambiguous marker: ${marker}`);
  return first;
}

function exactBlocks(text) {
  const capStart = uniqueIndex(text, '    function buildCap(');
  const capEnd = text.indexOf('\n    const HALF_ANGLE = {', capStart);
  assert.ok(capEnd > capStart);
  const amStart = uniqueIndex(text, 'function renderAmOnlyContactCaps(');
  const amBody = text.slice(amStart);
  const amGeometryStart = amBody.indexOf('  const R0 = 1.005;');
  const amGeometryEnd = amBody.indexOf('  const caps = [];');
  assert.ok(amGeometryStart >= 0 && amGeometryEnd > amGeometryStart);
  const webStart = uniqueIndex(text, '  /* group particles by type */');
  const webEnd = uniqueIndex(text, '  Object.values(state.meshes).forEach(m => { if (m) scene.add(m); });');
  assert.ok(webEnd > webStart);
  return {
    buildCap: text.slice(capStart, capEnd),
    amOnly: amBody.slice(amGeometryStart, amGeometryEnd),
    web02: text.slice(webStart, webEnd),
  };
}

const blocks = exactBlocks(source);
const frozenBlocks = exactBlocks(baseline);

// These classes are deliberately small test doubles, not a Three.js reimplementation.
// Position storage is Float32Array, as for the source's geometry vertex color loop.
const THREE_STUB = String.raw`
class BufferAttribute {
  constructor(array, itemSize) { this.array = array; this.itemSize = itemSize; this.count = array.length / itemSize; }
}
class SphereGeometry {
  constructor(...args) {
    this.args = args;
    const radius = args[0];
    const coordinates = [];
    for (const cosine of fixture.cosines) {
      coordinates.push(radius * Math.sqrt(Math.max(0, 1 - cosine * cosine)), radius * cosine, 0);
    }
    this.attributes = { position: new BufferAttribute(new Float32Array(coordinates), 3) };
  }
  setAttribute(name, attribute) { this.attributes[name] = attribute; }
}
class Color { constructor(value) { this.r = value.r; this.g = value.g; this.b = value.b; } }
class Vector3 {
  constructor(x, y, z) { this.x = x; this.y = y; this.z = z; }
  normalize() { const norm = Math.hypot(this.x, this.y, this.z); this.x /= norm; this.y /= norm; this.z /= norm; return this; }
}
class MeshBasicMaterial { constructor(options) { this.options = options; } }
class Mesh {
  constructor(geometry, material) {
    this.geometry = geometry; this.material = material;
    this.position = { set: (x, y, z) => { this.positionValue = [x, y, z]; } };
    this.quaternion = { setFromUnitVectors: (from, to) => { this.directionValue = { from, to }; } };
  }
}
const THREE = { BufferAttribute, SphereGeometry, Color, Vector3, MeshBasicMaterial, Mesh, FrontSide: 'TEST_FRONT_SIDE' };
`;

function evaluateFragment(fragment, fixture) {
  // The fragment has no DOM, filesystem, imports, require, process, or fetch in its context.
  // The VM timeout covers construction AND invocation. This is not claimed as an OS sandbox.
  const context = vm.createContext(Object.create(null), {
    codeGeneration: { strings: false, wasm: false },
  });
  const code = `'use strict';\nconst fixture = ${JSON.stringify(fixture)};\n${THREE_STUB}\n${fragment}`;
  const result = new vm.Script(code, { filename: 'synthetic-viewer-fragment.js' }).runInContext(context, { timeout: 1000 });
  return JSON.parse(JSON.stringify(result));
}

function cap(radius, cosines, halfAngle = Math.PI / 3) {
  return evaluateFragment(`
const STAGE_COL = { microcrack: { r: 0.125, g: 0.5, b: 0.875 } };
const STAGE_RANK = { microcrack: 2 };
${blocks.buildCap}
const mesh = buildCap(fixture.radius, { x: 2, y: 3, z: 5 }, { x: 2, y: 3, z: 6 }, 'microcrack', fixture.halfAngle);
({ colors: Array.from(mesh.geometry.attributes.color.array), itemSize: mesh.geometry.attributes.color.itemSize,
   geometryArgs: mesh.geometry.args, material: mesh.material.options, position: mesh.positionValue,
   direction: mesh.directionValue, renderOrder: mesh.renderOrder });
`, { radius, cosines, halfAngle });
}

function amOnly(cosines, halfAngle = Math.PI / 3) {
  return evaluateFragment(`
const ha = fixture.halfAngle;
${blocks.amOnly}
({ colors: Array.from(geo.attributes.color.array), itemSize: geo.attributes.color.itemSize, geometryArgs: geo.args });
`, { cosines, halfAngle });
}

function grouping(types, atomsOnly) {
  return evaluateFragment(`
const data = { atoms_only: fixture.atomsOnly, particles: fixture.types.map((type, i) => ({ id: i + 1, type })) };
const state = { meshes: {} };
const lamps = [{ isAmbientLight: true, intensity: 0.6 }, { isDirectionalLight: true, intensity: 0.7 }];
const scene = { traverse: callback => lamps.forEach(callback) };
const COL = { AM_P: 'P', AM_S: 'S', SE: 'E', ATOMS_ONLY: 'GRAY' };
const OPA = { SE: 0.37 };
const createInstancedSpheres = (particles, segments, color, opacity, transparent) => ({
  ids: particles.map(p => p.id), segments, color, opacity, transparent,
});
${blocks.web02}
({ meshes: state.meshes, ids: Object.keys(state.idIndex).map(Number), atomsOnly: state.atomsOnly,
   am: state.amParticles.map(p => p.id), se: state.seParticles.map(p => p.id), lamps });
`, { types, atomsOnly, cosines: [] });
}

const tests = [];
const test = (name, fn) => tests.push({ name, fn });
const near = (actual, expected, label) => assert.ok(
  Number.isFinite(actual) && Math.abs(actual - expected) <= 5e-6,
  `${label}: expected ${expected}, got ${actual}`,
);
const radii = [0.5, 1, 2];
const alpha = (result, index) => result.colors[index * 4 + 3];

test('AM-only exact preservation with one historical comment correction; WEB02 exact', () => {
  const oldComment = 'Brittle 은 나누지 않아';
  assert.equal(frozenBlocks.amOnly.split(oldComment).length, 2, 'one known old comparison comment');
  const historicalCommentOnly = frozenBlocks.amOnly.replace(oldComment, '구본 Brittle 은 나누지 않아');
  assert.ok(blocks.amOnly === frozenBlocks.amOnly || blocks.amOnly === historicalCommentOnly,
    'AM-only bytes changed beyond the single historical comparison comment');
  assert.equal(blocks.web02, frozenBlocks.web02);
});

test('brittle pole is opaque for each declared radius', () => {
  for (const radius of radii) near(alpha(cap(radius, [1]), 0), 1, `pole r=${radius}`);
});

test('brittle rim is transparent for each declared radius', () => {
  for (const radius of radii) near(alpha(cap(radius, [0.5]), 0), 0, `rim r=${radius}`);
});

test('brittle interior hand oracle is one quarter for each radius', () => {
  for (const radius of radii) near(alpha(cap(radius, [0.75]), 0), 0.25, `interior r=${radius}`);
});

test('brittle production half angles obey normalized geometric oracle', () => {
  for (const halfAngle of [Math.PI / 9, Math.PI / 6, Math.PI / 4.5, Math.PI / 3.5]) {
    const rim = Math.cos(halfAngle);
    const cosines = [1, rim, Math.cos(halfAngle / 2)];
    const expected = cosines.map(cosine => Math.max(0, Math.min(1, (cosine - rim) / (1 - rim))) ** 2);
    for (const radius of radii) {
      const result = cap(radius, cosines, halfAngle);
      expected.forEach((value, index) => near(alpha(result, index), value, `angle=${halfAngle}, r=${radius}, vertex=${index}`));
    }
  }
});

test('brittle alpha remains clamped for explicitly synthetic out-of-cap vertices', () => {
  for (const radius of radii) {
    const result = cap(radius, [1.2, 0.2]);
    near(alpha(result, 0), 1, `above pole r=${radius}`);
    near(alpha(result, 1), 0, `below rim r=${radius}`);
  }
});

test('brittle geometry, color and transform call contracts stay unchanged', () => {
  for (const radius of radii) {
    const result = cap(radius, [1, 0.5, 0.75]);
    assert.deepEqual(result.geometryArgs, [radius * 1.005, 28, 14, 0, Math.PI * 2, 0, Math.PI / 3]);
    assert.equal(result.itemSize, 4);
    for (let i = 0; i < 3; i++) assert.deepEqual(result.colors.slice(i * 4, i * 4 + 3), [0.125, 0.5, 0.875]);
    assert.deepEqual(result.material, { vertexColors: true, transparent: true, depthWrite: false, side: 'TEST_FRONT_SIDE' });
    assert.deepEqual(result.position, [2, 5, 3]);
    assert.deepEqual(result.direction.from, { x: 0, y: 1, z: 0 });
    near(result.direction.to.x, 2 / 7, 'swapped direction x');
    near(result.direction.to.y, 6 / 7, 'swapped direction y');
    near(result.direction.to.z, 3 / 7, 'swapped direction z');
    assert.equal(result.renderOrder, 6);
  }
});

test('existing AM-only normalized linear alpha floor is preserved', () => {
  const result = amOnly([1, 0.5, 0.75]);
  assert.deepEqual(result.geometryArgs, [1.005, 16, 6, 0, Math.PI * 2, 0, Math.PI / 3]);
  assert.equal(result.itemSize, 4);
  [1, 0.3, 0.65].forEach((value, index) => near(alpha(result, index), value, `AM vertex=${index}`));
  for (let i = 0; i < 3; i++) assert.deepEqual(result.colors.slice(i * 4, i * 4 + 3), [1, 1, 1]);
});

test('existing WEB02 grouping preserves every particle and color choice', () => {
  const scenarios = [
    { types: ['AM_P', 'AM_S', 'SE'], atomsOnly: true, gray: false },
    { types: ['AM_P', 'SE'], atomsOnly: true, gray: false },
    { types: ['AM_P', 'UNKNOWN', 'SE'], atomsOnly: true, gray: true },
    { types: ['UNKNOWN', 'T3'], atomsOnly: true, gray: true },
    { types: ['AM_P', 'UNKNOWN', 'SE'], atomsOnly: false, gray: false },
  ];
  for (const scenario of scenarios) {
    const result = grouping(scenario.types, scenario.atomsOnly);
    const expectedIds = scenario.types.map((_, index) => index + 1);
    assert.deepEqual(result.ids, expectedIds);
    assert.deepEqual(Object.values(result.meshes).flatMap(mesh => mesh.ids).sort((a, b) => a - b), expectedIds);
    assert.equal(result.atomsOnly, scenario.atomsOnly);
    for (const [type, knownColor] of [['AM_P', 'P'], ['AM_S', 'S'], ['SE', 'E']]) {
      assert.equal(result.meshes[type].color, scenario.gray ? 'GRAY' : knownColor);
      assert.deepEqual(result.meshes[type].ids, expectedIds.filter(id => scenario.types[id - 1] === type));
    }
    if (result.meshes.OTHER) assert.equal(result.meshes.OTHER.color, 'GRAY');
    assert.deepEqual(result.am, [...result.meshes.AM_P.ids, ...result.meshes.AM_S.ids]);
    assert.deepEqual(result.se, result.meshes.SE.ids);
    assert.equal(result.meshes.SE.segments, scenario.gray ? 16 : 12);
    assert.equal(result.meshes.SE.opacity, scenario.gray ? 1 : 0.37);
    assert.equal(result.meshes.SE.transparent, !scenario.gray);
    assert.deepEqual(result.lamps.map(lamp => lamp.intensity), scenario.gray ? [0.3, 0.9] : [0.6, 0.7]);
  }
});

const results = [];
for (const { name, fn } of tests) {
  try { fn(); results.push({ name, status: 'PASS' }); }
  catch (error) { results.push({ name, status: 'FAIL', error: String(error?.stack || error) }); }
}
const failures = results.filter(result => result.status === 'FAIL').length;
console.log(JSON.stringify({
  baseline_pin: PIN, baseline_sha256: sha256(baselineBytes), source_sha256: sha256(sourceBytes),
  exact_block_sha256: Object.fromEntries(Object.entries(blocks).map(([key, value]) => [key, sha256(Buffer.from(value, 'utf8'))])),
  methods: tests.length, failures, results,
  scope: 'exact extracted source blocks with tiny THREE stubs; not browser, real Three.js, app, engine or physical data',
}, null, 2));
process.exitCode = failures ? 1 : 0;
