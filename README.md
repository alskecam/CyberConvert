# CyberConvert

A simple image conversion utility using Python and Pillow.

## Installation

This project uses `uv` for dependency management. You can run it directly without manual installation:

```bash
uv run convert.py [arguments]
```

## Usage

### Basic Conversion

To convert a single image:
```bash
uv run convert.py input.jpg output.webp --format webp
```

### Batch Conversion

To convert all images in a directory:
```bash
uv run convert.py ./input_dir ./output_dir --format png
```

### PSD Conversion

Conversion of PSD files is disabled by default. To enable it, use the `--psdconv` flag and specify an output format:

```bash
uv run convert.py input.psd output.png --format png --psdconv
```

In batch mode, PSD files will be skipped unless both `--format` and `--psdconv` are provided.

## Arguments

- `source`: Path to the source image or directory.
- `destination`: Path to the destination image or directory.
- `--format`: Output format. Choices: `jpeg`, `webp`, `png8`, `png`. (Required for PSD conversion).
- `--compress`: Compression value (10-100). Applicable to `jpeg` and `webp`.
- `--psdconv`: Enable PSD conversion.
