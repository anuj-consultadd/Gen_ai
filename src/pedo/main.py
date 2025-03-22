import argparse
from crewai import Crew
import os
import requests
from datetime import datetime
from pedo.crew import Pedo
from pedo.document_generator import create_formatted_case_study
import re

def get_company_logo_url(company_name):
    """Fetch a company logo URL using Clearbit Logo API with fallbacks."""
    print(f"🔍 Searching for logo for: {company_name}")
    
    # Try different domain variations
    company_slug = company_name.lower().replace(' ', '')
    domains_to_try = [
        f"{company_slug}.com",
        f"{company_slug}.org",
        f"{company_slug}.net",
        f"{company_slug}.io",
        f"{company_slug}.co"
    ]
    
    # Try each domain variation
    for domain in domains_to_try:
        logo_url = f"https://logo.clearbit.com/{domain}"
        try:
            response = requests.head(logo_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Found logo: {logo_url}")
                return logo_url
        except Exception as e:
            print(f"⚠️ Error fetching logo for {domain}: {e}")
    
    # If no logo found with company name, try common alternatives
    if "technologies" in company_name.lower():
        alt_name = company_name.lower().replace("technologies", "tech")
        alt_url = get_company_logo_url(alt_name)
        if alt_url:
            return alt_url
    
    # Return a default logo or None if all attempts fail
    print(f"⚠️ No logo found for {company_name}")
    return None




def run():
    """
    Run the crew pipeline and generate the final PDF with custom colors for header, footer, border.
    """
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Process PDF into formatted case study")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    parser.add_argument("--company", help="Company name (defaults to PDF filename)")
    
    # Color options
    parser.add_argument("--border-color", default="000080", help="Border color in hex (default: navy blue)")
    parser.add_argument("--header-color", default="4472C4", help="Header color in hex (default: blue)")
    parser.add_argument("--footer-color", help="Footer color in hex (defaults to header color)")
    parser.add_argument("--heading1-color", default="2F5597", help="Heading 1 color in hex (default: dark blue)")
    parser.add_argument("--heading2-color", default="5B9BD5", help="Heading 2 color in hex (default: medium blue)")
    parser.add_argument("--accent-color", default="70AD47", help="Accent color for graphs (default: green)")
    
    args = parser.parse_args()
    pdf_path = args.pdf
    date_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Extract company name from filename if not provided
    # if args.company:
    company_name = args.company
    # else:
    #     company_name = extract_company_name_from_filename(pdf_path)
    
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
    if args.footer_color:
        colors['footer'] = args.footer_color
    else:
        colors['footer'] = args.header_color
    
    # Print color settings for confirmation
    print(f"🎨 Using color scheme:")
    print(f"   - Border: #{colors['border']}")
    print(f"   - Header: #{colors['header']}")
    print(f"   - Footer: #{colors['footer']}")
    print(f"   - Heading 1: #{colors['heading1']}")
    print(f"   - Heading 2: #{colors['heading2']}")
    print(f"   - Accent: #{colors['accent']}")
    
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
        return
    

    logo_url = get_company_logo_url(company_name) 
    
    # Step 4: Generate the formatted case study document with the extracted content, logo, and custom colors
    try:
        output_file = f"output/case_study_{company_name.replace(' ', '_')}_{date_now}.pdf"
        create_formatted_case_study(structured_text, logo_url, output_file, colors)
        print(f"✅ Final PDF saved at {output_file}")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()