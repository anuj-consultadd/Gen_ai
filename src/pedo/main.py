#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from pedo.crew import Pedo
from pedo.document_generator import create_formatted_case_study
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def get_company_logo_url(company_name):
    """Fetch a company logo URL using Clearbit Logo API with fallbacks."""
    print(f"🔍 Searching for logo for: {company_name}")
    
    company_slug = company_name.lower().replace(' ', '')
    domains_to_try = [
        f"{company_slug}.com",
        f"{company_slug}.org",
        f"{company_slug}.net",
        f"{company_slug}.io",
        f"{company_slug}.co"
    ]
    
    for domain in domains_to_try:
        logo_url = f"https://logo.clearbit.com/{domain}"
        print(f"🔗 Trying: {logo_url}")
        # https://logo.clearbit.com/
        try:
            response = requests.head(logo_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Found logo: {logo_url}")
                return logo_url
        except Exception as e:
            print(f"⚠️ Error fetching logo for {domain}: {e}")
    
    print(f"⚠️ No logo found for {company_name}")
    return None

def choose_theme_color():
    """Opens a simple dialog for selecting a main theme color."""
    root = tk.Tk()
    root.withdraw()  # Hide main window

    color_options = {
        "Navy Blue": "000080",
        "Dark Gray": "232F3E",
        "Light Blue": "5B9BD5",
        "Green": "70AD47",
        "Orange": "FF9900",
        "Purple": "800080",
        "Red": "FF0000"
    }

    theme_color_name = simpledialog.askstring(
        "Main Theme Color",
        f"Choose a main theme color ({', '.join(color_options.keys())}):",
        initialvalue="Navy Blue"
    )

    return color_options.get(theme_color_name, "000080")  # Default to Navy Blue if invalid

def customize_colors(theme_color):
    """Opens a Tkinter window for selecting different colors for each element."""
    color_window = tk.Toplevel()
    color_window.title("Customize Colors")
    
    selected_colors = {}
    
    # Default color variable
    default_color = tk.StringVar(value=theme_color)

    def update_colors():
        """Update all color selections if 'Set as Default' is checked."""
        if default_checkbox_var.get():
            for key in selected_colors:
                selected_colors[key].set(default_color.get())

    # Labels for different sections
    color_labels = ["Border", "Header", "Footer", "Heading 1", "Heading 2", "Accent"]
    
    for idx, label in enumerate(color_labels):
        tk.Label(color_window, text=f"{label} Color:").grid(row=idx, column=0, sticky="w")
        
        selected_colors[label.lower()] = tk.StringVar(value=default_color.get())
        row_frame = tk.Frame(color_window)
        row_frame.grid(row=idx, column=1, sticky="w")

        for color_name, hex_value in {
            "Navy Blue": "000080",
            "Dark Gray": "232F3E",
            "Light Blue": "5B9BD5",
            "Green": "70AD47",
            "Orange": "FF9900",
            "Purple": "800080",
            "Red": "FF0000"
        }.items():
            rb = tk.Radiobutton(row_frame, text=color_name, variable=selected_colors[label.lower()], value=hex_value)
            rb.pack(side="left")

    # "Set as Default" checkbox
    default_checkbox_var = tk.BooleanVar()
    default_checkbox = tk.Checkbutton(color_window, text="Set as Default for all", variable=default_checkbox_var, command=update_colors)
    default_checkbox.grid(row=len(color_labels), columnspan=2)

    # Submit button
    def submit_colors():
        color_window.destroy()

    submit_button = tk.Button(color_window, text="Submit", command=submit_colors)
    submit_button.grid(row=len(color_labels) + 1, columnspan=2)

    color_window.wait_window()  

    return {key: var.get() for key, var in selected_colors.items()}

def get_user_input():
    """Opens a Tkinter dialog for selecting a file and inputting details."""
    root = tk.Tk()
    root.withdraw()  # Hide main window

    pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        print("❌ No PDF file selected. Exiting.")
        exit()

    company_name = simpledialog.askstring("Company Name", "Enter the company name:")
    if not company_name:
        company_name = "Unknown Company"

    # Choose main theme color
    theme_color = choose_theme_color()

    # Ask if user wants to manually customize colors
    customize = messagebox.askyesno("Customize Colors?", "Would you like to choose different colors for each section?\nClick 'No' to apply the same color everywhere.")

    if customize:
        colors = customize_colors(theme_color)
    else:
        colors = {key: theme_color for key in ["border", "header", "footer", "heading1", "heading2", "accent"]}

    return pdf_path, company_name, colors

def run():
    """Runs the CrewAI pipeline with user-selected inputs."""
    pdf_path, company_name, colors = get_user_input()
    date_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    print(f"🚀 Processing {pdf_path} for company: {company_name}")
    print(f"🎨 Selected Colors: {colors}")

    try:
        pdf_crew = Pedo()
        crew_output = pdf_crew.crew().kickoff(inputs={"pdf_path": pdf_path})

        structured_text = str(crew_output) if not isinstance(crew_output, str) else crew_output

        os.makedirs("output", exist_ok=True)

        debug_structured_text_path = "output/debug_structured_text.txt"
        with open(debug_structured_text_path, "w", encoding="utf-8") as f:
            f.write(structured_text)

        print(f"✅ Extracted text saved to {debug_structured_text_path}")
    
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return

    logo_url = get_company_logo_url(company_name)

    try:
        output_file = f"output/{inputs['date_now']}.pdf"
        create_formatted_case_study(structured_text, inputs["logo_url"], output_file)
        print(f"✅ Final PDF saved at {output_file}")

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()


# 1.change the logo fetch api
# 2.increase the font size

# 3.structure a format for  this 
# *Exhibit 2 (cont.)**  
# Amazon.com, Inc. Balance Sheets ($ Millions)  
# December 31,  
# |                     | 2016   | 2015   | 2014   |
# |---------------------|--------|--------|--------|
# | Current assets:     |        |        |        |
# | Cash and cash equivalents | 19,334 | 15,890 | 14,557 |
# | Marketable securities | 6,647  | 3,918  | 2,859  |
# | Inventories         | 11,461 | 10,243 | 8,299  |
# | Accounts receivable, net and other | 8,339  | 5,654  | 5,612  |
# | Total current assets | 45,781 | 35,705 | 31,327 |
# | Property and equipment, net | 29,114 | 21,838 | 16,967 |
# | Goodwill            | 3,784  | 3,759  | 3,319  |
# | Other assets        | 4,723  | 3,445  | 2,892  |
# | Total assets        | 83,402 | 64,747 | 54,505 |
# | Current liabilities: |        |        |        |
# | Accounts payable     | 25,309 | 20,397 | 15,459 |
# | Accrued expenses and other | 13,739 | 10,372 | 9,807  |
# | Unearned revenue    | 4,768  | 3,118  | 1,823  |
# | Total current liabilities | 43,816 | 33,887 | 28,089 |
# | Long-term debt      | 7,694  | 8,227  | 8,265  |
# | Other long-term liabilities | 12,607 | 9,249  | 7,410  |
# | Stockholders’ equity: |       |        |        |
# | Common stock        | 5      | 5      | 5      |
# | Treasury stock, at cost | (1,837) | (1,837) | (1,837) |
# | Additional paid-in capital | 17,186 | 13,394 | 11,135 |
# | Accumulated other comprehensive loss | (985) | (723) | (511) |
# | Retained earnings    | 4,916  | 2,545  | 1,949  |
# | Total stockholders’ equity | 19,285 | 13,384 | 10,741 |
# | Total liabilities and stockholders’ equity | 83,402 | 64,747 | 54,505 |
# | **Source:** Amazon.com, Inc. 10-Ks, December 31, 2015-16. 

# 4.regular expression for "Sorce:"
# see why bolding is also not working here
# ## 6. SAMPLES FRAMEWORKS AND APPLICATION
# ### Potential Frameworks
# - **4P’s**
#     - Price
#     - Promotion
#     - Place
# - **Porter’s Five Forces**
# - **SWOT Analysis**

# 5. page end after heading type 1

# 6.add graphs

# 7. do something for headers and footer 
# 8. change font typr to accenture pdf and also match font settings to it
    # find accenture text font and use it 
#9 do something about that header and the footer


