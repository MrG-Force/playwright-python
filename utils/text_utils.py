def normalize_text(text:str) -> str:
    """
    Normalizes the given text by stripping leading and trailing whitespace,
    replacing ",\n" with a space, and removing extra spaces.

    Parameters:
    text (str): The input text to normalize.

    Returns:
    str: The normalized text.
    """
    text = text.strip()
    text = text.replace(",\n", " ").replace("  ", " ")
    return text
