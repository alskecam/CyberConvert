# /// script
# dependencies = [
#   "pytest",
#   "pillow",
# ]
# ///

import subprocess
import sys
from pathlib import Path
from PIL import Image

def test_psd_file_requires_flags(tmp_path):
    psd_file = tmp_path / "test.psd"
    psd_file.touch()

    # Try without flags
    result = subprocess.run([sys.executable, "convert.py", str(psd_file), str(tmp_path / "out.png")], capture_output=True, text=True)
    assert result.returncode != 0
    assert "PSD conversion is not enabled" in result.stderr

    # Try with --psdconv but no --format
    result = subprocess.run([sys.executable, "convert.py", str(psd_file), str(tmp_path / "out.png"), "--psdconv"], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Format must be specified for PSD conversion" in result.stderr

def test_psd_batch_skips_without_flags(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    psd_file = src_dir / "test.psd"
    psd_file.touch()
    png_file = src_dir / "test.png"
    # Create a real PNG so Pillow can open it
    img = Image.new('RGB', (10, 10), color='red')
    img.save(png_file)

    dest_dir = tmp_path / "dest"

    # Run without psd flags
    result = subprocess.run([sys.executable, "convert.py", str(src_dir), str(dest_dir), "--format", "webp"], capture_output=True, text=True)
    # The script should convert the PNG and skip the PSD
    assert "Successfully converted" in result.stdout
    assert "1/2 files" in result.stdout

def test_psd_batch_with_flags_attempt_conversion(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    psd_file = src_dir / "test.psd"
    psd_file.touch() # This will fail during actual conversion but we check if it's ATTEMPTED

    dest_dir = tmp_path / "dest"

    # Run with psd flags
    result = subprocess.run([sys.executable, "convert.py", str(src_dir), str(dest_dir), "--format", "png", "--psdconv"], capture_output=True, text=True)
    # Since test.psd is not a real image, convert_image will return False and print an error
    assert "Error converting" in result.stderr
    assert "0/1 files" in result.stdout
