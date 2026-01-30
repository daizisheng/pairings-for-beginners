#!/usr/bin/env python3
"""Extract all images from Reid.pdf and save them to html/images/."""

import os
import fitz  # PyMuPDF

PDF_PATH = "/Users/shishengli/pairings-for-beginners/ag/Reid.pdf"
OUT_DIR = "/Users/shishengli/pairings-for-beginners/ag/html/images"

os.makedirs(OUT_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
total_images = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images(full=True)
    if images:
        print(f"Page {page_num + 1}: {len(images)} image(s)")
    for img_idx, img_info in enumerate(images):
        xref = img_info[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]  # original format (png, jpeg, etc.)

        # Always save as .png for consistency
        filename = f"fig_page{page_num + 1}_img{img_idx + 1}.png"
        out_path = os.path.join(OUT_DIR, filename)

        # If already png, write directly; otherwise convert via pixmap
        if ext == "png":
            with open(out_path, "wb") as f:
                f.write(image_bytes)
        else:
            # Convert to PNG using fitz Pixmap
            pix = fitz.Pixmap(image_bytes)
            # If CMYK, convert to RGB first
            if pix.n - pix.alpha > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            pix.save(out_path)

        total_images += 1

doc.close()

print(f"\nTotal: {total_images} image(s) extracted to {OUT_DIR}")
