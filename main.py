def process_input(fname: str) -> list[str]:
    """
    Levi
    """
    with open(fname, 'r', encoding='utf-8') as f:
        file_text = f.read() 
        return file_text.split('---')

def ollama_batch(items: list[str], n: int, search: str) -> list[str]:
    """
    Curtis
    """
    pass


def ollama_reduce(items: list[str], n: int, search: str) -> list[str]:
    """
    Will
    """
    pass

