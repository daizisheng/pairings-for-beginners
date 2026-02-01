#!/usr/bin/env python3
"""
PDF to Bilingual HTML Converter
Converts PDF files to HTML with English and Chinese content
"""

import pdfplumber
import pypdf
from pathlib import Path
import re
import os

# HTML template matching ch1.html and ch2.html style
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: "Computer Modern", "Latin Modern Roman", Georgia, serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }}
        .content {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 0.3em;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }}
        h2 {{
            font-size: 1.8em;
            margin-top: 2em;
            margin-bottom: 1em;
            color: #2c3e50;
        }}
        h3 {{
            font-size: 1.3em;
            margin-top: 1.5em;
            color: #34495e;
        }}
        p {{
            margin: 1em 0;
            text-align: justify;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 1em 0;
            padding: 0.5em 1em;
            background-color: #ecf0f1;
            font-style: normal;
            color: #555;
        }}
        .exercises {{
            background-color: #f8f9fa;
            padding: 1.5em;
            margin: 2em 0;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
        }}
        .exercises h3 {{
            color: #e74c3c;
            margin-top: 0;
        }}
        .exercise-item {{
            margin: 1em 0;
            padding-left: 1.5em;
        }}
        .example {{
            background-color: #fff9e6;
            padding: 1em;
            margin: 1.5em 0;
            border-left: 4px solid #f39c12;
            border-radius: 4px;
        }}
        .example-title {{
            font-weight: bold;
            color: #f39c12;
            margin-bottom: 0.5em;
        }}
        .figure {{
            text-align: center;
            margin: 2em 0;
        }}
        .figure img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
        }}
        .figure-caption {{
            font-style: italic;
            color: #666;
            margin-top: 0.5em;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
        }}
    </style>
</head>
<body>
    <div class="content">
{content}
    </div>
</body>
</html>
'''


def extract_images_from_pdf(pdf_path, output_dir):
    """Extract images from PDF using pypdf"""
    images = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            if '/XObject' in page['/Resources']:
                x_objects = page['/Resources']['/XObject'].get_object()
                for obj_name in x_objects:
                    obj = x_objects[obj_name]
                    if obj['/Subtype'] == '/Image':
                        try:
                            # Extract image data
                            size = (obj['/Width'], obj['/Height'])
                            data = obj.get_data()
                            # Save image
                            img_filename = f"fig{page_num + 1}_{obj_name[1:]}.png"
                            img_path = output_dir / img_filename
                            with open(img_path, 'wb') as img_file:
                                img_file.write(data)
                            images.append((page_num, img_filename))
                        except Exception as e:
                            print(f"Could not extract image from page {page_num + 1}: {e}")
    except Exception as e:
        print(f"Error extracting images: {e}")
    return images


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    text_by_page = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_by_page.append(text)
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text_by_page


def convert_inline_math(text):
    """Convert inline math to LaTeX format"""
    # This is a simple heuristic - may need adjustment based on actual PDF content
    # Convert standalone equations to display math
    text = re.sub(r'\n([A-Za-z0-9\+\-\=\(\)\[\]\{\}\^\*\/\\\s]+)\n', r'\n\\[ \\1 \\]\n', text)
    return text


def translate_to_chinese(english_text):
    """
    Placeholder for translation. In a real implementation, you would use:
    - A translation API (Google Translate, DeepL, etc.)
    - A pre-translated glossary
    - Manual translation

    For now, this returns a placeholder
    """
    # This is where you'd integrate actual translation
    # For demonstration, returning a placeholder
    return "[中文翻译待添加]"


def process_chapter_content(text_pages, chapter_num):
    """
    Process chapter content and structure it for HTML
    This is a simplified version - you'll need to enhance based on actual PDF structure
    """
    full_text = "\n\n".join(text_pages)

    # Split into sections (this is very basic - adjust based on actual structure)
    sections = []
    current_section = {"title": "", "content": []}

    for line in full_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Detect section headers (adjust pattern based on actual PDF)
        if re.match(r'^\d+\.\d+\s+', line) or re.match(r'^[A-Z][A-Za-z\s]+$', line):
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": line, "content": []}
        else:
            current_section["content"].append(line)

    if current_section["content"]:
        sections.append(current_section)

    return sections


def generate_html_content(chapter_num, chapter_title, sections, images_dir="images"):
    """Generate HTML content with bilingual text"""
    content = f'        <h1>Chapter {chapter_num}<br>{chapter_title}</h1>\n\n'
    content += '        <blockquote>\n'
    content += f'            <h1 style="text-align: center; font-size: 2.2em;">第{chapter_num}章<br>{chapter_title}</h1>\n'
    content += '        </blockquote>\n\n'

    for section in sections:
        if section["title"]:
            content += f'        <h2>{section["title"]}</h2>\n\n'

        for para in section["content"]:
            # Convert to paragraph
            content += f'        <p>{para}</p>\n\n'
            # Add Chinese translation
            content += '        <blockquote>\n'
            content += f'            <p>{translate_to_chinese(para)}</p>\n'
            content += '        </blockquote>\n\n'

    return content


def convert_pdf_to_html(pdf_path, output_html_path, chapter_num, chapter_title):
    """Main conversion function"""
    print(f"Converting {pdf_path} to {output_html_path}...")

    # Create images directory
    images_dir = Path(output_html_path).parent / "images"
    images_dir.mkdir(exist_ok=True)

    # Extract text
    print("Extracting text...")
    text_pages = extract_text_from_pdf(pdf_path)

    # Extract images
    print("Extracting images...")
    images = extract_images_from_pdf(pdf_path, images_dir)
    print(f"Extracted {len(images)} images")

    # Process content
    print("Processing content...")
    sections = process_chapter_content(text_pages, chapter_num)

    # Generate HTML
    print("Generating HTML...")
    html_content = generate_html_content(chapter_num, chapter_title, sections)

    # Create full HTML
    full_html = HTML_TEMPLATE.format(
        title=f"Chapter {chapter_num}: {chapter_title}",
        content=html_content
    )

    # Write to file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✓ Conversion complete: {output_html_path}")
    return True


if __name__ == "__main__":
    # Configuration for chapters
    chapters = {
        3: "Chapter Title 3",  # Update with actual titles
        4: "Chapter Title 4",
        5: "Chapter Title 5",
        6: "Chapter Title 6",
        7: "Chapter Title 7",
        8: "Chapter Title 8",
        9: "Chapter Title 9",
        10: "Chapter Title 10",
        11: "Chapter Title 11",
    }

    base_dir = Path("/Users/shishengli/pairings-for-beginners/cf")
    html_dir = base_dir / "html"
    html_dir.mkdir(exist_ok=True)

    # Process ch3.pdf first
    chapter_num = 3
    pdf_file = base_dir / f"ch{chapter_num}.pdf"
    html_file = html_dir / f"ch{chapter_num}.html"

    if pdf_file.exists():
        convert_pdf_to_html(
            pdf_file,
            html_file,
            chapter_num,
            chapters.get(chapter_num, f"Chapter {chapter_num}")
        )
    else:
        print(f"PDF file not found: {pdf_file}")
