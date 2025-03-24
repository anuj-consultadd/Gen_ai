from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import requests
import subprocess
import os
import re
import matplotlib.pyplot as plt
from docx.shared import RGBColor, Length
from docx.enum.style import WD_STYLE_TYPE

def create_formatted_case_study(input_text, logo_url, output_file, colors=None):
    """
    Creates a well-formatted Word document from structured input text and converts it to PDF.
    Enhanced with custom fonts and improved spacing.
    
    Args:
        input_text (str): The formatted text content
        logo_url (str): URL to the company logo
        output_file (str): Path to save the PDF
        colors (dict): Dictionary with color settings (e.g. {'border': '000080', 'header': '4472C4'})
    """
    if not output_file.endswith(".pdf"):
        raise ValueError("Output file must have a .pdf extension")

    # Default colors if none provided
    if colors is None:
        colors = {
            'border': '000000',      # Black
            'header': '4472C4',      # Blue
            'footer': '4472C4',      # Blue (same as header by default)
            'heading1': '2F5597',    # Dark blue
            'heading2': '5B9BD5',    # Medium blue
            'accent': '70AD47'       # Green
        }
    
    # Ensure footer color exists (use header color as fallback)
    if 'footer' not in colors and 'header' in colors:
        colors['footer'] = colors['header']
    
    docx_file = output_file.replace(".pdf", ".docx")
    doc = Document()
    
    # Set document margins
    for section in doc.sections:
        section.top_margin = Inches(1.25)  # Increased to 1.25 inches
        section.bottom_margin = Inches(1.25)  # Increased to 1.25 inches
        section.left_margin = Inches(1)  # Kept at 1 inch
        section.right_margin = Inches(1)  # Kept at 1 inch
    
    # Set up custom styles for different text elements
    # Heading 1 Style (Graphik-Bold, 24pt)
    style_h1 = doc.styles.add_style('CustomHeading1', WD_STYLE_TYPE.PARAGRAPH)
    style_h1.font.name = 'Graphik-Bold'
    style_h1.font.size = Pt(24)
    style_h1.font.bold = True
    style_h1.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_h1.paragraph_format.space_before = Pt(20)
    style_h1.paragraph_format.space_after = Pt(15)
    style_h1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_h1.paragraph_format.line_spacing = Pt(30)
    
    # Heading 2 Style (Graphik-Bold, 18pt)
    style_h2 = doc.styles.add_style('CustomHeading2', WD_STYLE_TYPE.PARAGRAPH)
    style_h2.font.name = 'Graphik-Bold'
    style_h2.font.size = Pt(18)
    style_h2.font.bold = True
    style_h2.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_h2.paragraph_format.space_before = Pt(18)
    style_h2.paragraph_format.space_after = Pt(12)
    style_h2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_h2.paragraph_format.line_spacing = Pt(22)
    
    # Heading 3 Style (Graphik-Bold, 14pt)
    style_h3 = doc.styles.add_style('CustomHeading3', WD_STYLE_TYPE.PARAGRAPH)
    style_h3.font.name = 'Graphik-Bold'
    style_h3.font.size = Pt(14)
    style_h3.font.bold = True
    style_h3.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_h3.paragraph_format.space_before = Pt(15)
    style_h3.paragraph_format.space_after = Pt(10)
    style_h3.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_h3.paragraph_format.line_spacing = Pt(20)
    
    # Heading 4 Style (Graphik-Bold, 12pt)
    style_h4 = doc.styles.add_style('CustomHeading4', WD_STYLE_TYPE.PARAGRAPH)
    style_h4.font.name = 'Graphik-Bold'
    style_h4.font.size = Pt(12)
    style_h4.font.bold = True
    style_h4.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_h4.paragraph_format.space_before = Pt(15)
    style_h4.paragraph_format.space_after = Pt(10)
    style_h4.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_h4.paragraph_format.line_spacing = Pt(18)
    
    # Body Text Style (Graphik-Regular, 11pt)
    style_body = doc.styles.add_style('CustomBody', WD_STYLE_TYPE.PARAGRAPH)
    style_body.font.name = 'Graphik-Regular'
    style_body.font.size = Pt(11)
    style_body.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_body.paragraph_format.space_before = Pt(6)
    style_body.paragraph_format.space_after = Pt(6)
    style_body.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_body.paragraph_format.line_spacing = Pt(14)
    
    # Bullet Point Style (ArialMT, 9pt)
    style_bullet = doc.styles.add_style('CustomBullet', WD_STYLE_TYPE.PARAGRAPH)
    style_bullet.font.name = 'ArialMT'
    style_bullet.font.size = Pt(9)
    style_bullet.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_bullet.paragraph_format.space_before = Pt(4)
    style_bullet.paragraph_format.space_after = Pt(4)
    style_bullet.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_bullet.paragraph_format.line_spacing = Pt(11)
    style_bullet.paragraph_format.left_indent = Pt(18)
    
    # Numbered List Style (ArialMT, 9pt)
    style_numbered = doc.styles.add_style('CustomNumbered', WD_STYLE_TYPE.PARAGRAPH)
    style_numbered.font.name = 'ArialMT'
    style_numbered.font.size = Pt(9)
    style_numbered.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style_numbered.paragraph_format.space_before = Pt(4)
    style_numbered.paragraph_format.space_after = Pt(4)
    style_numbered.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_numbered.paragraph_format.line_spacing = Pt(11)
    style_numbered.paragraph_format.left_indent = Pt(18)
    
    # Title Style (Graphik-Bold, 26pt)
    style_title = doc.styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
    style_title.font.name = 'Graphik-Bold'
    style_title.font.size = Pt(26)
    style_title.font.bold = True
    style_title.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    style_title.paragraph_format.space_before = Pt(10)
    style_title.paragraph_format.space_after = Pt(20)
    style_title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    style_title.paragraph_format.line_spacing = Pt(30)
    
    # Add logo
    import traceback
    import requests
    from PIL import Image
    from io import BytesIO
    import os
    import traceback

    try:
        if logo_url:
            print(f"📥 Downloading logo from URL: {logo_url}")
            response = requests.get(logo_url, timeout=10)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                content_length = len(response.content)

                print(f"✅ Response received. Content Type: {content_type}, Size: {content_length} bytes")

                # Validate Content-Type for images (PNG, JPEG, etc.)
                if not content_type.startswith("image/"):
                    print("❌ Error: The downloaded file is not an image. Skipping logo.")
                else:
                    # Try loading the image with PIL to ensure it's valid
                    try:
                        image = Image.open(BytesIO(response.content))
                        image_format = image.format  # Get image format (PNG, JPG, etc.)

                        if image_format not in ["PNG", "JPEG", "JPG"]:
                            print(f"⚠️ Warning: Unsupported image format: {image_format}. Trying to convert to PNG.")

                            # Convert to PNG if not in a valid format
                            image = image.convert("RGB")
                            temp_logo_path = "temp_logo.png"
                            image.save(temp_logo_path, format="PNG")
                        else:
                            # Save the valid image
                            temp_logo_path = f"temp_logo.{image_format.lower()}"
                            image.save(temp_logo_path)

                        print(f"✅ Saved logo to {temp_logo_path}, size: {os.path.getsize(temp_logo_path)} bytes")

                        # Verify the saved file is valid
                        if os.path.exists(temp_logo_path) and os.path.getsize(temp_logo_path) > 0:
                            doc.add_picture(temp_logo_path, width=Pt(200))
                            logo_paragraph = doc.paragraphs[-1]
                            logo_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                            logo_paragraph.space_after = Pt(20)
                            print("✅ Added logo to document and centered it")
                        else:
                            print("⚠️ Warning: The logo image was not saved properly or is corrupted.")

                    except Exception as image_error:
                        print(f"❌ Error: The downloaded file is not a valid image: {image_error}")
                        traceback.print_exc()

            else:
                print(f"⚠️ Failed to download logo. HTTP Status Code: {response.status_code}")
                print("🛠️ Possible Fixes:")
                print("   - Check if the logo URL is correct and accessible.")
                print("   - Ensure there is an active internet connection.")
                print("   - Try using a different logo provider or manually downloading the image.")

        else:
            print("⚠️ No logo URL provided, skipping logo addition.")

    except requests.exceptions.Timeout:
        print("❌ Error: The request for downloading the logo timed out. Try again with a stable internet connection.")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Network connection issue. Ensure you have internet access.")

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Unexpected error during logo download: {req_err}")
        traceback.print_exc()

    except Exception as e:
        print(f"❌ Critical error while processing the logo: {e}")
        traceback.print_exc()
    
    # Extract company name from filename if available
    company_name = ""
    if output_file:
        base_name = os.path.basename(output_file)
        if base_name.startswith("case_study_"):
            company_parts = base_name.replace("case_study_", "").split("_")
            if len(company_parts) > 0:
                company_name = " ".join([part.capitalize() for part in company_parts[0].split("_")])
    
    # Add a title page header with Graphik-Regular font
    header = doc.sections[0].header
    header_para = header.paragraphs[0]
    header_para.text = company_name
    header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    header_run = header_para.runs[0]
    header_run.font.name = 'Graphik-Regular'
    header_run.font.size = Pt(10)
    header_run.font.bold = True
    header_run.font.color.rgb = RGBColor.from_string(colors['header'])
    
    # Add a title page with custom title style
    title_para = doc.add_paragraph(style='CustomTitle')
    title_run = title_para.add_run("CASE STUDY REPORT")
    title_run.font.color.rgb = RGBColor.from_string(colors['heading1'])
    
    # Add page break after title
    doc.add_page_break()
    
    # Process text content with markdown-like formatting
    data_for_graphs = []
    
    for line in input_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("#### "): # H4
            p = doc.add_paragraph(line[5:], style='CustomHeading4')
            for run in p.runs:
                run.font.color.rgb = RGBColor.from_string(colors['heading2'])
            
        elif line.startswith("### "): # H3
            p = doc.add_paragraph(line[4:], style='CustomHeading3')
            for run in p.runs:
                run.font.color.rgb = RGBColor.from_string(colors['heading2'])
            
        elif line.startswith("## "): # H2
            p = doc.add_paragraph(line[3:], style='CustomHeading2')
            for run in p.runs:
                run.font.color.rgb = RGBColor.from_string(colors['heading2'])
            
        elif line.startswith("# "): # H1
            p = doc.add_paragraph(line[2:], style='CustomHeading1')
            for run in p.runs:
                run.font.color.rgb = RGBColor.from_string(colors['heading1'])
            
        elif "**" in line:
            p = doc.add_paragraph(style='CustomBody')
            parts = re.split(r"(\*\*.*?\*\*)", line)  # Split by bold markers
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    run = p.add_run(part[2:-2])  # Remove "**" from start and end
                    run.font.name = 'Graphik-Bold'
                    run.bold = True
                else:
                    p.add_run(part)  # Normal text

            
        # Bulleted Lists - using ArialMT
        elif line.startswith("- ") or line.startswith("• "):
            p = doc.add_paragraph(line[2:], style='CustomBullet')
            # Ensure first character is a bullet
            p.style.paragraph_format.first_line_indent = Pt(-12)
            bullet_run = p.add_run("• ", 0)
            bullet_run.font.name = 'ArialMT'
            
        # Numbered Lists - using ArialMT
        elif re.match(r"^\d+\.", line):
            number_match = re.match(r"^(\d+)\.(.*)$", line)
            if number_match:
                number, content = number_match.groups()
                p = doc.add_paragraph(style='CustomNumbered')
                # Add the number with special formatting
                p.style.paragraph_format.first_line_indent = Pt(-12)
                number_run = p.add_run(f"{number}. ", 0)
                number_run.font.name = 'ArialMT'
                # Add the content
                content_run = p.add_run(content.strip())
                content_run.font.name = 'ArialMT'
            
        # Data for graphs (simple format: "GRAPH: label1,value1;label2,value2")
        elif line.startswith("GRAPH:"):
            data_str = line[6:].strip()
            items = data_str.split(";")
            labels = []
            values = []
            
            for item in items:
                parts = item.split(",")
                if len(parts) == 2:
                    labels.append(parts[0].strip())
                    values.append(float(parts[1].strip()))
            
            if labels and values:
                data_for_graphs.append((labels, values))
                
        # Normal Text - using Graphik-Regular
        else:
            p = doc.add_paragraph(line, style='CustomBody')
    
    # Generate and add graphs if data is available
    for i, (labels, values) in enumerate(data_for_graphs):
        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color=f'#{colors["accent"]}')
        plt.title(f"Data Visualization {i+1}", fontname='Graphik-Bold', fontsize=14)
        plt.xticks(fontname='Graphik-Regular', fontsize=9)
        plt.yticks(fontname='Graphik-Regular', fontsize=9)
        plt.tight_layout()
        
        # Save the graph
        graph_filename = f"temp_graph_{i}.png"
        plt.savefig(graph_filename)
        plt.close()
        
        # Add to document with proper spacing
        doc.add_picture(graph_filename, width=Inches(6))
        graph_paragraph = doc.paragraphs[-1]
        graph_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        graph_paragraph.space_before = Pt(12)
        graph_paragraph.space_after = Pt(12)
    
    # Add page borders with user-specified color (keeping existing border code)
    for section in doc.sections:
        # Add page borders - all sides
        section_properties = section._sectPr
        page_borders = OxmlElement('w:pgBorders')
        page_borders.set(qn('w:offsetFrom'), 'page')
        
        for border_name in ['top', 'left', 'bottom', 'right']:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single')  # single line
            border.set(qn('w:sz'), '4')       # thickness in 1/8 points (4 = 0.5pt)
            border.set(qn('w:space'), '24')   # space in points
            border.set(qn('w:color'), colors['border'])  # Use user-specified border color
            page_borders.append(border)
            
        section_properties.append(page_borders)
    
    # Add page numbers in footer with user-specified color and Graphik-Regular font
    for section in doc.sections:
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.text = f"{company_name} Case Study | Page "
        
        # Style the footer text with user's footer color and Graphik-Regular font
        for run in footer_para.runs:
            run.font.name = 'Graphik-Regular'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor.from_string(colors['footer'])
        
        # Add page number field
        run = footer_para.add_run()
        run.font.name = 'Graphik-Regular'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(colors['footer'])
        fldChar = OxmlElement('w:fldChar')
        fldChar.set(qn('w:fldCharType'), 'begin')
        run._element.append(fldChar)
        
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        run._element.append(instrText)
        
        fldChar = OxmlElement('w:fldChar')
        fldChar.set(qn('w:fldCharType'), 'end')
        run._element.append(fldChar)
        
        run = footer_para.add_run(" of ")
        run.font.name = 'Graphik-Regular'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(colors['footer'])
        
        run = footer_para.add_run()
        run.font.name = 'Graphik-Regular'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(colors['footer'])
        fldChar = OxmlElement('w:fldChar')
        fldChar.set(qn('w:fldCharType'), 'begin')
        run._element.append(fldChar)
        
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "NUMPAGES"
        run._element.append(instrText)
        
        fldChar = OxmlElement('w:fldChar')
        fldChar.set(qn('w:fldCharType'), 'end')
        run._element.append(fldChar)
        
        run = footer_para.add_run(" | Confidential")
        run.font.name = 'Graphik-Regular'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(colors['footer'])
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Save document
    doc.save(docx_file)
    print(f"✅ DOCX saved as {docx_file}")
    
    # Convert to PDF
    pdf_file = output_file
    try:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", docx_file, "--outdir", os.path.dirname(pdf_file)], check=True)
        print(f"✅ PDF saved as {pdf_file}")
    except Exception as e:
        print(f"❌ PDF conversion failed: {e}")
    
    # Cleanup temporary files
    try:
        if os.path.exists("temp_logo.png"):
            os.remove("temp_logo.png")
            print("✅ Removed temporary logo file")
        for i in range(len(data_for_graphs)):
            if os.path.exists(f"temp_graph_{i}.png"):
                os.remove(f"temp_graph_{i}.png")
                print(f"✅ Removed temporary graph file: temp_graph_{i}.png")
    except Exception as e:
        print(f"⚠️ Failed to clean up temporary files: {e}")