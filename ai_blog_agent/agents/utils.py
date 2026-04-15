def extract_text(content):
    """Helper to extract clean text from various potential LLM response formats."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return " ".join([extract_text(c) for c in content]).strip()
    if isinstance(content, dict):
        if 'text' in content:
            return content['text'].strip()
        return str(content).strip()
    return str(content).strip()
