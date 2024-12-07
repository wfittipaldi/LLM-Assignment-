import os
def process_input(fname: str) -> list[str]:
    """
    Levi
    """
    with open(fname, 'r', encoding='utf-8') as f:
        file_text = f.read() 
        return file_text.split('\n---\n')

def ollama_batch(items: list[str], n: int, search: str) -> list[str]:
    """
    Curtis
    """
    pass


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
    return list_of_items




        print(output_results)
        pass

