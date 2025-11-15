#!/usr/bin/env python
"""Convert logo.jpg to logo.ico"""
import os
from PIL import Image

logo_jpg = "logo.jpg"
logo_ico = "logo.ico"

if os.path.exists(logo_jpg):
    try:
        img = Image.open(logo_jpg).convert("RGBA")
        # Resize to standard icon size (256x256)
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        # Save as ICO
        img.save(logo_ico, "ICO")
        print(f"✓ Converted {logo_jpg} to {logo_ico}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print(f"✗ File not found: {logo_jpg}")
