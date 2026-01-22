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
        if source.is_dir():
            print(f"Error: {source} is a directory, not a file.", file=sys.stderr)
            return False

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

            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            img.save(destination, format=save_format if save_format != "PNG8" else "PNG")
            print(f"Successfully converted {source} to {destination} ({format_ext or save_format})")
            return True
    except Exception as e:
        print(f"Error converting {source}: {e}", file=sys.stderr)
        return False

def get_output_ext(source_path, format_ext):
    if format_ext == "png8":
        return ".png"
    elif format_ext:
        return f".{format_ext}"
    else:
        return source_path.suffix

def main():
    parser = argparse.ArgumentParser(description="Image conversion utility")
    parser.add_argument("source", help="Path to the source image or directory")
    parser.add_argument("destination", help="Path to the destination image or directory")
    parser.add_argument("--format", choices=["jpeg", "webp", "png8", "png"], help="Output format")

    args = parser.parse_args()

    source_path = Path(args.source)
    dest_path = Path(args.destination)

    if not source_path.exists():
        print(f"Error: Source {args.source} does not exist", file=sys.stderr)
        sys.exit(1)

    if source_path.is_dir():
        if dest_path.exists() and not dest_path.is_dir():
            print(f"Error: Source is a directory but destination {args.destination} is a file", file=sys.stderr)
            sys.exit(1)

        files = [f for f in source_path.iterdir() if f.is_file()]
        if not files:
            print(f"Error: No files found in {source_path}", file=sys.stderr)
            sys.exit(1)

        success_count = 0
        for item in files:
            ext = get_output_ext(item, args.format)
            output_item = dest_path / (item.stem + ext)
            if convert_image(item, output_item, args.format):
                success_count += 1

        print(f"Finished. Successfully converted {success_count}/{len(files)} files.")
        if success_count == 0:
            sys.exit(1)
    else:
        # Source is a file
        actual_dest = dest_path
        if dest_path.is_dir():
             ext = get_output_ext(source_path, args.format)
             actual_dest = dest_path / (source_path.stem + ext)

        if not convert_image(source_path, actual_dest, args.format):
            sys.exit(1)

if __name__ == "__main__":
    main()
