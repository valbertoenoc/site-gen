def markdown_to_blocks(markdown):
    paragraphs = markdown.split("\n\n")
    striped = list(map(lambda x: x.strip(), paragraphs))
    filtered = list(filter(lambda x: len(x) > 0, striped))
    return filtered
