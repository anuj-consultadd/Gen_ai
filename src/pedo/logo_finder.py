import requests

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