# bg-remove

A simple CLI tool for removing backgrounds from images using AI (Inspyrenet model).

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install pillow transparent-background
```

## Usage

### Basic usage

```bash
# Remove background from a single image
python main.py input.jpg

# This creates input_nobg.png
```

### Specify output file

```bash
python main.py input.jpg -o output.png
```

### Process multiple files

```bash
# Process all JPG files in current directory
python main.py *.jpg

# Use custom suffix
python main.py *.jpg --suffix _transparent
```

### Use faster model

```bash
# Trade accuracy for speed
python main.py input.jpg --fast
```

### Quiet mode

```bash
# Suppress success messages
python main.py input.jpg --quiet
```

### Help

```bash
python main.py --help
```

## Features

- ✅ Single or batch processing
- ✅ Automatic output naming
- ✅ Fast and base model options
- ✅ Multiple image format support (JPG, PNG, etc.)
- ✅ Transparent PNG output
- ✅ Progress feedback

## Requirements

- Python >= 3.13
- pillow >= 12.0.0
- transparent-background >= 1.3.4
- numpy (for dark mode color inversion)

## Notes

- The model files (~350MB) will be downloaded automatically on first run
- Output files are always saved as PNG with transparency
- Input images are automatically converted to RGB format before processing
