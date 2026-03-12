def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text[:3000]