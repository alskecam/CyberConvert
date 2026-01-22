# /// script
# dependencies = [
#   "pillow",
# ]
# ///

import argparse
from pathlib import Path
from PIL import Image
import sys

def convert_image(source, destination, format_ext=None):
    try:
        with Image.open(source) as img:
            if format_ext == "png8":
                # Convert to 8-bit palette
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
                save_format = "PNG"
            elif format_ext:
                save_format = format_ext.upper()
                if save_format == "JPEG":
                    # JPEG doesn't support RGBA, convert to RGB
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
            else:
                # Infer format from destination extension
                save_format = Path(destination).suffix.lstrip('.').upper()
                if save_format == "JPG":
                    save_format = "JPEG"

                if save_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

            img.save(destination, format=save_format if save_format != "PNG8" else "PNG")
            print(f"Successfully converted {source} to {destination} ({format_ext or save_format})")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Image conversion utility")
    parser.add_argument("source", help="Path to the source image")
    parser.add_argument("destination", help="Path to the destination image")
    parser.add_argument("--format", choices=["jpeg", "webp", "png8", "png"], help="Output format")

    args = parser.parse_args()

    source_path = Path(args.source)
    dest_path = Path(args.destination)

    if not source_path.exists():
        print(f"Error: Source file {args.source} does not exist", file=sys.stderr)
        sys.exit(1)

    convert_image(source_path, dest_path, args.format)

if __name__ == "__main__":
    main()
