from openai import OpenAI
import sys


def process_input(fname: str) -> list[str]:
    """
    Takes in a file name and outputs the inventory contents present in that file as a string. 
    Parameters: 
        fname: the name of a file
    Returns: 
        list of inventory items
    """
    with open(fname, 'r', encoding='utf-8') as f:
        file_text = f.read() 
        return file_text.split('---')


def ollama_batch(items: list[str], n: int, search: str) -> list[str]:
    """
    A helper function which makes an API call to gpt-4o-mini model given a specific batch of inventory.
    Parameters: 
        items: list of inventory items
        n: integer for how many items to return
        search: the query given by the user
    Returns: 
        list of items selected by the LLM 
    """
    all_items = "\n".join(items)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are Craig, the manager of a used marketplace "
                "and customers want to ask you for items that fit their specific needs.\n"
                "You must recommend to them the top {:d} items from "
                "the list of items you have in store. The items you have in store "
                "are as follows:\n{:s}"
                "\n\nWhen the user tells you what they are looking for, "
                "respond with only the top {:d} items delimited with the line '---' between them.".format(n, all_items, n)
            },
            {
                "role": "user",
                "content": "The item I am looking for is {:s}".format(search)
            }
        ]
    )

    items = [
        item.strip()
        for item in completion.choices[0].message.content.split("---")
        if item != ""
    ]
    return items


def ollama_reduce(items: list[str], n: int, search: str) -> list[str]:
    """
    Utilizing the ollama_batch, this function splits up the entire inventory into batches so that the user's query does
    not exceed the context size limits of the model. After running the users query on each batch it returns the top 'n' options.
    Parameters: 
        items: list of inventory items
        n: integer for how many items to return
        search: the query given by the user
    Returns: 
        list of items selected by the LLM 
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
    client = OpenAI()
    craig(sys.argv[1])
