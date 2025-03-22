#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from pedo.crew import Pedo  
from pedo.document_generator import create_formatted_case_study  

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew pipeline and generate the final PDF.
    """
    inputs = {
        'pdf_path': 'case_study.pdf',  
        'logo_url': "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg" ,
        'date_now': datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
    }
    
    print("🚀 Starting the Crew Execution...")

    try:
        structured_text = Pedo().crew().kickoff(inputs=inputs)

        if isinstance(structured_text, list):
            structured_text = " ".join(map(str, structured_text))
        elif not isinstance(structured_text, str):
            structured_text = str(structured_text)

        
        os.makedirs("output", exist_ok=True)

        debug_structured_text_path = "output/debug_structured_text.txt"
        with open(debug_structured_text_path, "w", encoding="utf-8") as f:
            f.write(structured_text)


    except Exception as e:
        print(f"❌ An error occurred while running CrewAI: {e}")
        return

    try:
        output_file = f"output/{inputs['date_now']}.pdf"
        create_formatted_case_study(structured_text, inputs["logo_url"], output_file)
        print(f"✅ Final PDF saved at {output_file}")

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")

if __name__ == "__main__":
    run()
