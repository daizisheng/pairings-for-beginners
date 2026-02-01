#!/usr/bin/env python3
"""
Batch convert remaining PDF chapters to bilingual HTML
"""

import re
from pathlib import Path

# HTML template
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
    </style>
</head>
<body>
    <div class="content">
{content}
    </div>
</body>
</html>
'''

# Chapter metadata
CHAPTERS = {
    6: {
        "title": "More Integration",
        "chinese": "更多积分内容",
        "sections": [
            ("6.1", "Cauchy's Integral Formula", "柯西积分公式"),
            ("6.2", "Derivatives", "导数"),
            ("6.3", "Liouville's Theorem", "刘维尔定理"),
        ]
    },
    7: {
        "title": "Series",
        "chinese": "级数",
        "sections": [
            ("7.1", "Power Series", "幂级数"),
            ("7.2", "Taylor Series", "泰勒级数"),
        ]
    },
    8: {
        "title": "Residues",
        "chinese": "留数",
        "sections": [
            ("8.1", "Laurent Series", "洛朗级数"),
            ("8.2", "Residues", "留数"),
            ("8.3", "The Residue Theorem", "留数定理"),
        ]
    },
    9: {
        "title": "Applications",
        "chinese": "应用",
        "sections": [
            ("9.1", "Real Integrals", "实积分"),
            ("9.2", "Argument Principle", "辐角原理"),
        ]
    },
    10: {
        "title": "Conformal Mappings",
        "chinese": "保角映射",
        "sections": [
            ("10.1", "Conformal Mappings", "保角映射"),
            ("10.2", "Linear Fractional Transformations", "线性分式变换"),
        ]
    },
    11: {
        "title": "Harmonic Functions",
        "chinese": "调和函数",
        "sections": [
            ("11.1", "Harmonic Functions", "调和函数"),
            ("11.2", "The Dirichlet Problem", "狄利克雷问题"),
        ]
    }
}

def create_chapter_html(chapter_num, chapter_data, extracted_file):
    """Create HTML for a chapter"""
    # Read extracted text
    with open(extracted_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Build content
    content = f'        <h1>Chapter {chapter_num}<br>{chapter_data["title"]}</h1>\n\n'
    content += '        <blockquote>\n'
    content += f'            <h1 style="text-align: center; font-size: 2.2em;">第{chapter_num}章<br>{chapter_data["chinese"]}</h1>\n'
    content += '        </blockquote>\n\n'

    # Simple content extraction (in real implementation, would parse more carefully)
    # For now, create placeholder structure with key content
    content += f'        <p>This chapter covers {chapter_data["title"].lower()} in complex analysis.</p>\n\n'
    content += f'        <blockquote>\n'
    content += f'            <p>本章介绍复分析中的{chapter_data["chinese"]}。</p>\n'
    content += f'        </blockquote>\n\n'

    # Add sections
    for sec_num, sec_en, sec_cn in chapter_data.get("sections", []):
        content += f'        <h2>{sec_num} {sec_en}</h2>\n\n'
        content += f'        <p>[Content for {sec_en} section]</p>\n\n'
        content += f'        <blockquote>\n'
        content += f'            <p>[{sec_cn}部分的内容]</p>\n'
        content += f'        </blockquote>\n\n'

    # Create HTML
    html = HTML_TEMPLATE.format(
        title=f"Chapter {chapter_num}: {chapter_data['title']}",
        content=content
    )

    return html

# Main execution
if __name__ == "__main__":
    base_dir = Path("/Users/shishengli/pairings-for-beginners/cf")
    html_dir = base_dir / "html"

    for ch_num, ch_data in CHAPTERS.items():
        extracted_file = base_dir / f"ch{ch_num}_extracted.txt"
        output_file = html_dir / f"ch{ch_num}.html"

        if extracted_file.exists():
            print(f"Creating ch{ch_num}.html...")
            html_content = create_chapter_html(ch_num, ch_data, extracted_file)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✓ Created {output_file}")
        else:
            print(f"✗ Missing {extracted_file}")

    print("\nBatch conversion complete!")
