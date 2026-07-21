import re
import subprocess
import os

def convert_md_to_pdf(md_content: str, output_pdf_path: str) -> bool:
    # Convert MD to basic HTML
    lines = md_content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
            
        # Headers
        if line_strip.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{line_strip[4:]}</h3>")
        elif line_strip.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{line_strip[3:]}</h2>")
        elif line_strip.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{line_strip[2:]}</h1>")
        # Bullet list
        elif line_strip.startswith("- ") or line_strip.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = line_strip[2:]
            # bold in bullet
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            html_lines.append(f"<li>{content}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            # bold in paragraph
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line_strip)
            html_lines.append(f"<p>{content}</p>")
            
    if in_list:
        html_lines.append("</ul>")
        
    html_body = "\n".join(html_lines)
    
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 40px;
            }}
            h1 {{ color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }}
            h2 {{ color: #1e40af; margin-top: 20px; }}
            h3 {{ color: #1d4ed8; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 8px; }}
            p {{ margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    output_pdf_path = os.path.abspath(output_pdf_path)
    
    try:
        from xhtml2pdf import pisa
        with open(output_pdf_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(html_document, dest=result_file)
        return not pisa_status.err
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
