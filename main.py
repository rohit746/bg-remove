#!/usr/bin/env python3
"""
bg-remove: A CLI tool for removing backgrounds from images using AI.
"""
import warnings

# Suppress known warnings from dependencies
warnings.filterwarnings("ignore", message="Failed to import flet")
warnings.filterwarnings("ignore", message="torch.meshgrid")

from transparent_background import Remover
from PIL import Image, ImageOps
import argparse
import sys
import os
from pathlib import Path
import numpy as np


def invert_dark_colors(image, threshold=128, brightness_boost=1.2):
    """
    Inverts dark colors in an image while preserving transparency.
    Useful for dark mode applications like Obsidian.

    Args:
        image (PIL.Image): RGBA image to process.
        threshold (int): Brightness threshold (0-255). Pixels darker than this will be inverted.
        brightness_boost (float): Factor to boost brightness of inverted colors.

    Returns:
        PIL.Image: Image with dark colors inverted.
    """
    # Convert to numpy array for easier manipulation
    img_array = np.array(image)

    # Separate RGB and alpha channels
    rgb = img_array[:, :, :3]
    alpha = img_array[:, :, 3]

    # Calculate brightness (perceived luminance)
    brightness = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]

    # Create mask for dark pixels
    dark_mask = brightness < threshold

    # Invert dark pixels
    inverted_rgb = rgb.copy()
    inverted_rgb[dark_mask] = 255 - rgb[dark_mask]

    # Apply brightness boost to inverted pixels
    if brightness_boost != 1.0:
        inverted_rgb = inverted_rgb.astype(float)
        inverted_rgb[dark_mask] = np.clip(
            inverted_rgb[dark_mask] * brightness_boost, 0, 255
        )
        inverted_rgb = inverted_rgb.astype(np.uint8)

    # Reconstruct image with alpha channel
    result_array = np.dstack([inverted_rgb, alpha])

    return Image.fromarray(result_array, mode="RGBA")


def remove_background(
    input_path,
    output_path,
    model_name="base",
    dark_mode=False,
    invert_threshold=128,
    brightness_boost=1.2,
):
    """
    Removes the background from an image using the Inspyrenet model.

    Args:
        input_path (str): The path to the input image file (JPG, PNG, etc.).
        output_path (str): The path to save the output transparent PNG file.
        model_name (str): Model to use ('base' or 'fast'). Default is 'base'.
        dark_mode (bool): If True, inverts dark colors for better visibility in dark mode.
        invert_threshold (int): Brightness threshold for dark color inversion (0-255).
        brightness_boost (float): Brightness multiplier for inverted colors.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Initialize the remover model
        remover = Remover(mode=model_name)

        # Open the input image
        input_image = Image.open(input_path)

        # Convert to RGB to ensure consistent format (removes alpha channel if present)
        if input_image.mode != "RGB":
            input_image = input_image.convert("RGB")

        # Process the image to remove the background
        output_image = remover.process(input_image, type="rgba")

        # Apply dark mode color inversion if requested
        if dark_mode:
            output_image = invert_dark_colors(
                output_image, invert_threshold, brightness_boost
            )

        # Save the resulting image
        output_image.save(output_path)

        return True

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def generate_output_path(input_path, output_path=None, suffix="_nobg"):
    """
    Generates an output path based on the input path if not provided.

    Args:
        input_path (str): Input file path.
        output_path (str): Optional output path.
        suffix (str): Suffix to add to the filename.

    Returns:
        str: The output path with .png extension.
    """
    if output_path:
        return output_path

    input_pathobj = Path(input_path)
    output_name = f"{input_pathobj.stem}{suffix}.png"
    return str(input_pathobj.parent / output_name)


def main():
    parser = argparse.ArgumentParser(
        description="Remove backgrounds from images using AI (Inspyrenet model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg                    # Creates input_nobg.png
  %(prog)s input.jpg -o output.png      # Specify output file
  %(prog)s input.jpg --fast             # Use faster model
  %(prog)s *.jpg                        # Process multiple files
        """,
    )

    parser.add_argument(
        "input", nargs="+", help="Input image file(s) to process (JPG, PNG, etc.)"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (only valid for single input file). Default: <input>_nobg.png",
    )

    parser.add_argument(
        "--suffix",
        default="_nobg",
        help="Suffix to add to output filename when processing multiple files (default: _nobg)",
    )

    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use fast model instead of base model (faster but less accurate)",
    )

    parser.add_argument(
        "--dark-mode",
        action="store_true",
        help="Invert dark colors for better visibility in dark mode (e.g., Obsidian)",
    )

    parser.add_argument(
        "--invert-threshold",
        type=int,
        default=128,
        metavar="N",
        help="Brightness threshold for dark color inversion, 0-255 (default: 128)",
    )

    parser.add_argument(
        "--brightness-boost",
        type=float,
        default=1.2,
        metavar="F",
        help="Brightness multiplier for inverted colors (default: 1.2)",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress success messages"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Validate arguments
    if args.output and len(args.input) > 1:
        parser.error("--output can only be used with a single input file")

    # Determine model
    model_name = "fast" if args.fast else "base"

    # Process files
    success_count = 0
    total_count = len(args.input)

    for input_file in args.input:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            continue

        # Generate output path
        output_file = generate_output_path(input_file, args.output, args.suffix)

        if not args.quiet:
            print(f"Processing: {input_file} -> {output_file}")

        # Remove background
        if remove_background(
            input_file,
            output_file,
            model_name,
            args.dark_mode,
            args.invert_threshold,
            args.brightness_boost,
        ):
            success_count += 1
            if not args.quiet:
                print(f"✓ Successfully processed: {input_file}")
        else:
            if not args.quiet:
                print(f"✗ Failed to process: {input_file}")

    # Summary
    if total_count > 1 and not args.quiet:
        print(f"\nProcessed {success_count}/{total_count} images successfully")

    # Exit with appropriate code
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
