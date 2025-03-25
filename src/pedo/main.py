import argparse
import os
import sys
from datetime import datetime
from crewai import Crew
from pedo.crew import Pedo
from pedo.document_generator import create_formatted_case_study
from pedo.logo_finder import get_company_logo_url
import traceback



def run(args):
    """
    Run the crew pipeline and generate the final PDF with custom colors for header, footer, border.
    """
    pdf_path = args.pdf
    date_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Use provided company name or derive from filename
    company_name = args.company or os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(f"🚀 Starting PDF processing for {pdf_path}")
    print(f"📋 Company name: {company_name}")
    
    # Prepare color settings with user-provided values
    colors = {
        'border': args.border_color,
        'header': args.header_color,
        'heading1': args.heading1_color,
        'heading2': args.heading2_color,
        'accent': args.accent_color
    }
    
    # Set footer color (defaults to header color if not specified)
    colors['footer'] = args.footer_color or args.header_color
    
    # Print color settings for confirmation
    print(f"🎨 Using color scheme:")
    for color_type, color_code in colors.items():
        print(f"   - {color_type.capitalize()}: #{color_code}")
    
    try:
        # Initialize CrewAI for text extraction
        pdf_crew = Pedo()
        crew_output = pdf_crew.crew().kickoff(inputs={"pdf_path": pdf_path})

        # Convert CrewOutput to a string if needed
        if isinstance(crew_output, list):
            structured_text = " ".join(map(str, crew_output))
        elif not isinstance(crew_output, str):
            structured_text = str(crew_output)
        else:
            structured_text = crew_output

        # Save structured text for debugging
        os.makedirs("output", exist_ok=True)
        debug_structured_text_path = f"output/structured_text_{date_now}.txt"
        with open(debug_structured_text_path, "w", encoding="utf-8") as f:
            f.write(structured_text)
        
        print(f"✅ Saved structured text to {debug_structured_text_path}")
            
    except Exception as e:
        print(f"❌ Error during PDF text extraction: {e}")
        traceback.print_exc()
        return
    
    # Fetch company logo
    logo_url = get_company_logo_url(company_name) 
    
    # Generate the formatted case study document
    try:
        output_file = f"output/case_study_{company_name.replace(' ', '_')}_{date_now}.pdf"
        create_formatted_case_study(structured_text, logo_url, output_file, colors)
        print(f"✅ Final PDF saved at {output_file}")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        traceback.print_exc()

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Generate formatted case study from PDF")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    parser.add_argument("--company", help="Company name (defaults to PDF filename)")
    
    # Color options with clear descriptions
    parser.add_argument("--border-color", default="000080", 
                      help="HEX color code for document borders (default: 000080 navy blue)")
    parser.add_argument("--header-color", default="4472C4", 
                      help="HEX color code for document header text (default: 4472C4 blue)")
    parser.add_argument("--footer-color", 
                      help="HEX color code for document footer text (defaults to header color)")
    parser.add_argument("--heading1-color", default="2F5597", 
                      help="HEX color code for main headings (default: 2F5597 dark blue)")
    parser.add_argument("--heading2-color", default="5B9BD5", 
                      help="HEX color code for subheadings (default: 5B9BD5 medium blue)")
    parser.add_argument("--accent-color", default="70AD47", 
                      help="HEX color code for graphs and accents (default: 70AD47 green)")
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.pdf):
        print(f"Error: PDF file not found: {args.pdf}")
        sys.exit(1)
    
    # Run the main processing function
    run(args)

if __name__ == "__main__":
    main()