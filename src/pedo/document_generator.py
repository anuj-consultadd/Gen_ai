from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
import requests
from io import BytesIO
import subprocess
import os
import re
import matplotlib.pyplot as plt
import numpy as np

def create_formatted_case_study(input_text, logo_url, output_file):
    """Creates a well-formatted Word document from structured input text and converts it to PDF."""
    if not output_file.endswith(".pdf"):
        raise ValueError("Output file must have a .pdf extension")

    docx_file = output_file.replace(".pdf", ".docx")
    doc = Document()
    
    # Set document margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # Add logo
    response = requests.get(logo_url)
    if response.status_code == 200:
        logo = Image.open(BytesIO(response.content))
        logo.save("temp_logo.png")
        doc.add_picture("temp_logo.png", width=Pt(150))
        
        # Center the logo
        logo_paragraph = doc.paragraphs[-1]
        logo_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Add a title page
    title = doc.add_heading(level=0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title.add_run("CASE STUDY REPORT")
    title_run.font.size = Pt(24)
    
    # Add page break after title
    doc.add_page_break()
    
    # Process text content with markdown-like formatting
    data_for_graphs = []
    
    for line in input_text.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("### "): # H3
            p = doc.add_paragraph(line[4:], style="Heading 3")
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            
        elif line.startswith("## "): # H2
            p = doc.add_paragraph(line[3:], style="Heading 2")
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            
        elif line.startswith("# "): # H1
            p = doc.add_paragraph(line[2:], style="Heading 1")
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            
        # Bold Text
        elif re.match(r"\*\*(.*?)\*\*", line):
            p = doc.add_paragraph()
            run = p.add_run(re.sub(r"\*\*(.*?)\*\*", r"\1", line))
            run.bold = True
            
        # Bulleted Lists
        elif line.startswith("- "):
            p = doc.add_paragraph(line[2:], style="List Bullet")
            
        # Numbered Lists
        elif re.match(r"^\d+\.", line):
            p = doc.add_paragraph(line, style="List Number")
            
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
                
        # Normal Text
        else:
            doc.add_paragraph(line)
    
    # Generate and add graphs if data is available
    for i, (labels, values) in enumerate(data_for_graphs):
        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color='skyblue')
        plt.title(f"Data Visualization {i+1}")
        plt.tight_layout()
        
        # Save the graph
        graph_filename = f"temp_graph_{i}.png"
        plt.savefig(graph_filename)
        plt.close()
        
        # Add to document
        doc.add_picture(graph_filename, width=Inches(6))
        graph_paragraph = doc.paragraphs[-1]
        graph_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Add page numbers in footer
    for section in doc.sections:
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.text = "Page "
        
        # Add page number field
        run = footer_para.add_run()
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
        
        run = footer_para.add_run()
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
    os.remove("temp_logo.png")
    for i in range(len(data_for_graphs)):
        os.remove(f"temp_graph_{i}.png")
