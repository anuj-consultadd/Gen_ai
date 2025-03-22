# src/pedo/cli.py
#!/usr/bin/env python3

import argparse
import sys
import os
from pedo.main import run

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
    
    # Pass arguments to run function
    run()

if __name__ == "__main__":
    main()