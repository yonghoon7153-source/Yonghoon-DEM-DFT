# Project conventions for Claude Code sessions

## Viewing figures / PDFs on this WSL machine

WSL paths (`/home/yonghoon/...`) cannot be opened directly with
`explorer.exe`.  Always **copy the file to `~/Downloads` first**, then
launch the explorer (or open) from there:

```bash
cp <path/to/file.png> ~/Downloads/ && explorer.exe ~/Downloads/<file.png>
```

When suggesting view commands to the user, write them in this two-step
form, e.g.:

```bash
cp docs/figures/brittle_z_input_8mAh_9.png ~/Downloads/ \
    && explorer.exe ~/Downloads/brittle_z_input_8mAh_9.png
```

If multiple files need to open at once, copy all then open all:

```bash
cp docs/figures/brittle_z_*.png ~/Downloads/ \
    && explorer.exe ~/Downloads/  # opens the Downloads folder
```

This convention applies to PNGs, PDFs, STL files, and any other output
the user wants to view through Windows.
