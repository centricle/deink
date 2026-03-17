# deink

Strips colored backgrounds from PDFs for clean printing. Corporate PDFs with colored fills and white text waste ink and print poorly. `deink` converts them to black text on white.

## Install

```
pipx install deink
```

If you don't have `pipx`, plain pip works too:

```
pip install deink
```

On macOS, pip may install the `deink` binary to a directory that's not on your PATH. If you get `command not found` after installing, run it directly:

```
python3 -m deink input.pdf
```

## Usage

```bash
# Convert a single file (creates input_deink.pdf)
deink input.pdf

# Specify output path
deink input.pdf -o output.pdf

# Batch convert
deink *.pdf
```

## License

MIT
