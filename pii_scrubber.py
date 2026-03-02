def scrub_pii(raw_text: str) -> str:
    """
    Takes raw text and scrubs personal identifiers.
    Replaces known entities with sanitized placeholder tags.
    """
    # 1. Copy the raw text to a new variable so we can modify it
    clean_text = raw_text
    
    # 2. Scrub the User Name
    clean_text = clean_text.replace("Scott", "[USER_A]")
    
    # 3. Scrub the Vendor Name
    clean_text = clean_text.replace("The Home Depot", "[VENDOR_1]")
    clean_text = clean_text.replace("Home Depot", "[VENDOR_1]")
    
    return clean_text