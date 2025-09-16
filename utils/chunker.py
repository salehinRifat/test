def chunk_text(text: str, max_chars: int = 3000):
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        sep = text.rfind('\n', start, end)
        if sep == -1:
            sep = text.rfind(' ', start, end)
        if sep == -1:
            sep = end
        chunks.append(text[start:sep].strip())
        start = sep
    return chunks
