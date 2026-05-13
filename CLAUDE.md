# Project conventions for Claude Code sessions

## Viewing figures / PDFs on this WSL machine

WSL paths (`/home/yonghoon/...`) cannot be opened directly with
`explorer.exe`.  Always **copy the file to the Windows Downloads
folder first**, then launch explorer from there.

**Path:** `/mnt/c/Users/안용훈/Downloads/`
(Windows: `C:\Users\안용훈\Downloads\`)

### Single file

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp <path/to/file.png> "$DL/" && explorer.exe "$(wslpath -w "$DL/<file.png>")"
```

### Multiple files (open Downloads folder once)

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp docs/figures/<glob>.png "$DL/" && explorer.exe "$(wslpath -w "$DL")"
```

### Concrete example (the brittle z-distribution plots)

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp docs/figures/brittle_z_*.png "$DL/" && explorer.exe "$(wslpath -w "$DL")"
```

This convention applies to PNGs, PDFs, STL files, and any other output
the user wants to view through Windows.  When suggesting view commands,
always use this `cp … "$DL/"` pattern — never call `explorer.exe` on a
raw `/home/...` WSL path because Windows can't resolve it.
