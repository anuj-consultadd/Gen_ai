# #!/usr/bin/env python
# import sys
# import warnings
# import os
# from datetime import datetime
# from pedo.crew import Pedo  
# from pedo.document_generator import create_formatted_case_study  

# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# def run():
#     """
#     Run the crew pipeline and generate the final PDF.
#     """
#     inputs = {
#         'pdf_path': 'case_study.pdf',  
#         'logo_url': "" ,
#         'date_now': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     }
    
#     print("🚀 Starting the Crew Execution...")

#     try:
#         structured_text = Pedo().crew().kickoff(inputs=inputs)

#         if isinstance(structured_text, list):
#             structured_text = " ".join(map(str, structured_text))
#         elif not isinstance(structured_text, str):
#             structured_text = str(structured_text)

        
#         os.makedirs("output", exist_ok=True)

#         debug_structured_text_path = "output/debug_structured_text.txt"
#         with open(debug_structured_text_path, "w", encoding="utf-8") as f:
#             f.write(structured_text)


#     except Exception as e:
#         print(f"❌ An error occurred while running CrewAI: {e}")
#         return

#     try:
#         output_file = f"output/{inputs['date_now']}.pdf"
#         create_formatted_case_study(structured_text, inputs["logo_url"], output_file)
#         print(f"✅ Final PDF saved at {output_file}")

#     except Exception as e:
#         print(f"❌ PDF generation failed: {e}")

# if __name__ == "__main__":
#     run()


# #!/usr/bin/env python
# import sys
# import warnings
# import os
# import requests
# from datetime import datetime
# from pedo.crew import Pedo
# from pedo.document_generator import create_formatted_case_study

# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# def get_company_logo_url(company_name):
#     """Fetch a company logo URL using Clearbit Logo API with fallbacks."""
#     print(f"🔍 Searching for logo for: {company_name}")
    
#     # Primary logo URL attempt
#     logo_url = f"https://logo.clearbit.com/{company_name.lower().replace(' ', '')}.com"
    
#     # Fallback logos in case the company logo isn't found
#     fallback_logos = [
#         f"https://logo.clearbit.com/{company_name.lower().replace(' ', '-')}.com",
#         "https://upload.wikimedia.org/wikipedia/commons/c/c0/Health_care_icon.svg",
#         "https://upload.wikimedia.org/wikipedia/commons/5/58/Instagram-Icon.png",
#         "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"
#     ]
    
#     # Check if logo exists, if not use fallbacks
#     try:
#         response = requests.head(logo_url)
#         if response.status_code == 200:
#             print(f"✅ Successfully found logo at: {logo_url}")
#             return logo_url
            
#         print(f"⚠️ Primary logo URL failed with status {response.status_code}, trying fallbacks...")
#         for fallback in fallback_logos:
#             try:
#                 response = requests.head(fallback)
#                 if response.status_code == 200:
#                     print(f"✅ Found fallback logo at: {fallback}")
#                     return fallback
#             except Exception as e:
#                 print(f"⚠️ Failed to check fallback URL {fallback}: {e}")
#                 continue
#     except Exception as e:
#         print(f"⚠️ Error checking primary logo URL: {e}")
    
#     # If all else fails, use the last fallback
#     print(f"⚠️ All logo attempts failed, using final fallback: {fallback_logos[-1]}")
#     return fallback_logos[-1]

# def run():
#     """
#     Run the crew pipeline and generate the final PDF.
#     """
#     # Extract company name from the case study
#     company_name = "MetroCare Health"
    
#     # Get logo URL
#     logo_url = get_company_logo_url(company_name)
    
#     inputs = {
#         'pdf_path': 'case_study.pdf',
#         'logo_url': logo_url,
#         'date_now': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     }
    
#     print(f"🚀 Starting the Crew Execution with logo URL: {logo_url}")

#     try:
#         structured_text = Pedo().crew().kickoff(inputs=inputs)

#         if isinstance(structured_text, list):
#             structured_text = " ".join(map(str, structured_text))
#         elif not isinstance(structured_text, str):
#             structured_text = str(structured_text)

#         os.makedirs("output", exist_ok=True)

#         debug_structured_text_path = "output/debug_structured_text.txt"
#         with open(debug_structured_text_path, "w", encoding="utf-8") as f:
#             f.write(structured_text)

#     except Exception as e:
#         print(f"❌ An error occurred while running CrewAI: {e}")
#         return

#     try:
#         output_file = f"output/{inputs['date_now']}.pdf"
#         create_formatted_case_study(structured_text, inputs["logo_url"], output_file)
#         print(f"✅ Final PDF saved at {output_file}")

#     except Exception as e:
#         print(f"❌ PDF generation failed: {e}")

# if __name__ == "__main__":
#     run()


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

def extract_company_name_from_text(text):
    """Extract company name from structured text using simple pattern matching."""
    # Try to find patterns like "Company: XYZ" or "Client: XYZ"
    company_patterns = [
        r"Company:\s*([A-Za-z0-9\s]+(?:Inc\.?|LLC|Ltd\.?|GmbH|Corp\.?|Corporation|Company)?)",
        r"Client:\s*([A-Za-z0-9\s]+(?:Inc\.?|LLC|Ltd\.?|GmbH|Corp\.?|Corporation|Company)?)",
        r"Case Study:\s*([A-Za-z0-9\s]+(?:Inc\.?|LLC|Ltd\.?|GmbH|Corp\.?|Corporation|Company)?)",
        r"# ([A-Za-z0-9\s]+(?:Inc\.?|LLC|Ltd\.?|GmbH|Corp\.?|Corporation|Company)?) Case Study"
    ]
    
    for pattern in company_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].strip()
    
    # Fall back to looking for company names with common suffixes
    suffix_pattern = r"([A-Za-z0-9\s]+(?:Inc\.?|LLC|Ltd\.?|GmbH|Corp\.?|Corporation|Company))"
    matches = re.findall(suffix_pattern, text)
    if matches:
        # Return the first occurrence that seems reasonably like a company name
        for match in matches:
            if len(match.split()) <= 5:  # Likely a company name if 5 or fewer words
                return match.strip()
    
    # Final fallback - extract the title which often contains company name
    title_match = re.search(r"# (.*)", text)
    if title_match:
        title = title_match.group(1)
        # Clean up title to extract likely company name
        cleaned_title = re.sub(r"Case Study|Integration|Solution|Implementation", "", title).strip()
        if len(cleaned_title.split()) <= 3:  # Simple heuristic for company names
            return cleaned_title
    
    return "Unknown Company"  # Default fallback

def run():
    """
    Run the crew pipeline and generate the final PDF with Crew Skipper handling logo fetching.
    """
    pdf_path = 'Amazon.pdf'
    date_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Step 1: Run CrewAI to extract and structure the text from the PDF
    print(f"🚀 Starting PDF processing for {pdf_path}")
    
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
    
    # Step 2: Use Crew Skipper (pattern matching) to extract company name
    company_name = extract_company_name_from_text(structured_text)
    print(f"✅ Extracted company name: {company_name}")
    
    # Step 3: Use Crew Skipper to fetch the logo without an agent
    logo_url = get_company_logo_url(company_name) if company_name != "Unknown Company" else None
    
    # Step 4: Generate the formatted case study document with the extracted content and logo
    try:
        output_file = f"output/case_study_{company_name.replace(' ', '_')}_{date_now}.pdf"
        create_formatted_case_study(structured_text, logo_url, output_file)
        print(f"✅ Final PDF saved at {output_file}")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()