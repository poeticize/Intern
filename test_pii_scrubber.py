from pii_scrubber import scrub_pii

def test_scrub_names_and_vendors():
    # 1. The Setup (The raw, dangerous data)
    raw_data = "Scott spent $1,200 at The Home Depot for construction materials."
    
    # 2. The Execution
    clean_data = scrub_pii(raw_data)
    
    # 3. The Assertions (The absolute rules the Intern must follow)
    assert "Scott" not in clean_data, "🚨 PII LEAK: User name found in output!"
    assert "Home Depot" not in clean_data, "🚨 PII LEAK: Vendor name found in output!"
    assert clean_data != raw_data, "🚨 FAILURE: The text was not modified at all!"