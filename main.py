import os
import ollama
import sys

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
    x = 0
    y = 20
    list_of_items = []
    while y < len(items):
        split_items = items[x:y]
        x = y
        y +=20
        filters = ollama_batch(split_items,n,search)
        list_of_items.extend(filters)
    if len(list_of_items) > n: 
        return ollama_batch(list_of_items, n, search)
    return list_of_items

def craig(inventory_file):
    user_search = input("This is Craig, your friendly neighborhood used marketplace manager. What are you looking for today?") 
    try:
        while user_search != 'q':
            search_size = input("And how many results would you like me to return?")
            matches = ollama_reduce(process_input(inventory_file), int(search_size), user_search)
            print("Here are the best items that match your request:")
            for item in matches: 
                print(item)
            user_search = input("Would you like to search again? ('q' to quit).")
    except ValueError:
        print("User input is invalid. Make sure that your search uses valid characters and that your number of desired results is a positive integer.")

if __name__ == "__main__":
    craig(sys.argv[1])
    pass
