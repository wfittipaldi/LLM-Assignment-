import ollama


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
    message: list[str] = []
    message.append("I am searching for the following item: {:s}.\n".format(search))
    message.append("This is a list of available items:\n")
    for item in items:
        message.append("item:\n" + item + "\n")
    message.append("\nPlease tell me the top {:d} items which fit the "
                   "description of what I was looking for. "
                   "Please do not generate any other text. "
                   "Please separate each of the top items with the delimiting line '---'.".format(n))
    response = ollama.generate(model="gemma2:2b", prompt="".join(message))
    items = [
        item.strip()
        for item in response.response.split("---")
        if item != ""
    ]
    return items


def ollama_reduce(items: list[str], n: int, search: str) -> list[str]:
    """
    Will
    """
    pass

