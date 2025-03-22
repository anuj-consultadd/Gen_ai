from crewai.tools import BaseTool
from PyPDF2 import PdfReader

class PdfReaderTool(BaseTool):
    name: str = "PDF_reader_tool" 
    description: str = "Read the content of a PDF file and return the text."

    def _run(self, pdf_path: str) -> str:
        print(f"📂 Reading PDF: {pdf_path}")  
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
            print(f"✅ Extracted {len(text)} characters from PDF.")  
            return text
        except Exception as e:
            print(f"❌ PDF Read Error: {e}")
            return "ERROR: Failed to read PDF."


