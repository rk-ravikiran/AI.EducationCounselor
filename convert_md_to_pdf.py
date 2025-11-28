"""
Simple MD to HTML converter for viewing in browser and printing to PDF
Renders Mermaid diagrams using mermaid.js CDN - NO external dependencies needed!
Just run: python convert_md_to_pdf.py
Then open ARCHITECTURE.html in Chrome and print to PDF (Ctrl+P)
"""
import re
from pathlib import Path

def convert_md_to_html_with_mermaid(md_file='ARCHITECTURE.md', output_file='ARCHITECTURE.html'):
    """Convert Markdown to HTML with embedded Mermaid.js rendering"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert basic markdown elements
    html_content = md_content
    
    # FIRST: Extract and protect Mermaid blocks
    mermaid_blocks = []
    def save_mermaid(match):
        content = match.group(1)
        # Remove YAML frontmatter (---\nid: ...\n---)
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL | re.MULTILINE)
        placeholder = f"___MERMAID_BLOCK_{len(mermaid_blocks)}___"
        mermaid_blocks.append(content.strip())
        return placeholder
    
    html_content = re.sub(
        r'```mermaid\n(.*?)```',
        save_mermaid,
        html_content,
        flags=re.DOTALL
    )
    
    # Headers
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    
    # Code blocks (non-mermaid) - mermaid already extracted
    # Special handling for tree structures (no language specified or plain text)
    def format_code_block(match):
        lang = match.group(1) if match.group(1) else ''
        content = match.group(2)
        # Check if it's a file tree structure
        if not lang or lang == 'text' or '├──' in content or '└──' in content or '│' in content:
            # Preserve whitespace for tree structures
            return f'<pre style="font-family: monospace; background: #f8f8f8; padding: 15px; border: 1px solid #ddd; border-radius: 5px; overflow-x: auto; line-height: 1.4;">{content}</pre>'
        else:
            return f'<pre><code class="language-{lang}">{content}</code></pre>'
    
    html_content = re.sub(
        r'```(\w*)\n(.*?)```',
        format_code_block,
        html_content,
        flags=re.DOTALL
    )
    
    # Convert mermaid blocks - removed, already handled above
    
    # Bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Italic
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # Links
    html_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html_content)
    
    # Lists
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    
    # Tables
    def convert_table(match):
        lines = match.group(0).strip().split('\n')
        header = lines[0]
        rows = lines[2:]  # Skip separator line
        
        headers = [h.strip() for h in header.split('|')[1:-1]]
        table_html = '<table><thead><tr>'
        for h in headers:
            table_html += f'<th>{h}</th>'
        table_html += '</tr></thead><tbody>'
        
        for row in rows:
            cells = [c.strip() for c in row.split('|')[1:-1]]
            table_html += '<tr>'
            for cell in cells:
                table_html += f'<td>{cell}</td>'
            table_html += '</tr>'
        
        table_html += '</tbody></table>'
        return table_html
    
    html_content = re.sub(
        r'\|.+?\|.+?\n\|[-:\| ]+\|.+?\n(?:\|.+?\|.+?\n)+',
        convert_table,
        html_content,
        flags=re.MULTILINE
    )
    
    # Paragraphs
    html_content = re.sub(r'\n\n', '</p><p>', html_content)
    
    # FINALLY: Restore Mermaid blocks
    for i, mermaid_code in enumerate(mermaid_blocks):
        placeholder = f"___MERMAID_BLOCK_{i}___"
        html_content = html_content.replace(placeholder, f'</p><div class="mermaid">\n{mermaid_code}\n</div><p>')
    
    # Complete HTML with Mermaid.js CDN
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Singapore Education Counselor - Architecture</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        }});
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
            background: #fff;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 40px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #555;
            margin-top: 25px;
        }}
        h4 {{
            color: #666;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .mermaid {{
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        ul {{
            margin: 10px 0;
        }}
        li {{
            margin: 5px 0;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        @media print {{
            body {{
                max-width: none;
                padding: 20px;
            }}
            .mermaid {{
                page-break-inside: avoid;
            }}
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <p>{html_content}</p>
</body>
</html>"""
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return output_file

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        md_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) >= 3 else md_file.replace('.md', '.html')
        convert_md_to_html_with_mermaid(md_file, output_file)
    else:
        convert_md_to_html_with_mermaid()
