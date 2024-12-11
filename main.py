from random import randrange
from time import time
import ollama
import logging

logger = logging.getLogger(__name__)
MODEL = "llama3.1:8b"


class Item:
    def __init__(self, description: str, index: int) -> None:
        self.desc = description
        self.index = index


class ItemPoolException(Exception):
    pass


class ItemPool:
    def __init__(self, items: list[Item]) -> None:
        self.items = items[:]

    def __len__(self) -> int:
        return len(self.items)

    def prune_once(self, search: str) -> "ItemPool":
        if len(self) < 2:
            raise ItemPoolException()

        item1 = self.items.pop(randrange(len(self)))
        item2 = self.items.pop(randrange(len(self)))

        logger.info("ItemPool.prune_once: item1 is '" + item1.desc + "'")
        logger.info("ItemPool.prune_once: item2 is '" + item2.desc + "'")
        
        message = "".join([
            "You are looking for an item that fits the following description:",
            "\n\n{:s}\n\n",
            "You have two choices. The first choice is the following item:",
            "\n\n{:s}\n\n",
            "The second choice is the following item:",
            "\n\n{:s}\n\n",
            "Please give a very short argument for why one or the other better fits",
            " the description you were given. Then, as the last line of your response,",
            " say FIRST if the first item was a better fit and SECOND if the second",
            " was a better fit. Do not output any response after saying FIRST or SECOND."
        ]).format(search, item1.desc, item2.desc)
        logger.info("ItemPool.prune_once: model prompt: '{:s}'".format(message))
        response = ollama.generate(model=MODEL, prompt=message).response
        logger.info("ItemPool.prune_once: model response: '{:s}'".format(response))
        last_line = response.strip().split("\n")[-1]
        if last_line == "FIRST":
            logger.info("ItemPool.prune_once first choice selected.")
            self.items.append(item1)
        elif last_line == "SECOND":
            logger.info("ItemPool.prune_once second choice selected.")
            self.items.append(item2)
        else:
            logger.info("ItemPool.prune_once no choice selected.")
            self.items.append(item1)
            self.items.append(item2)

        return self

    def prune_until(self, search: str, size: int) -> "ItemPool":
        while (len(self) > size):
            self.prune_once(search)
            logger.info("ItemPool.prune_until current pool size: {:d}".format(len(self)))
        return self


def process_input(fname: str) -> list[str]:
    """
    Levi
    """
    logger.info("Processing File Begin: " + fname)
    with open(fname, 'r', encoding='utf-8') as f:
        file_text = f.read() 
        logger.info("Processing File Success: " + fname)
        return [
            entry.strip()
            for entry in file_text.split("---")
        ]


def ollama_batch(items: list[str], n: int, search: str) -> list[str]:
    """
    Curtis
    """
    logger.info("Ollama Batch Started: {:f}".format(time()))
    message: list[str] = []
    message.append("I am searching for the following item: {:s}.\n".format(search))
    message.append("This is a list of available items:\n")
    for item in items:
        message.append("item:\n" + item + "\n")
        logger.info("Ollama Batch Item: " + item)
    message.append("\nPlease tell me the top {:d} items which fit the "
                   "description of what I was looking for. \n"
                   "Please list items in the format (do not actually say item index - just write the number):\n\n"
                   "item description\n"
                   "item index\n\n"
                   "Please separate each of the top items with the delimiting line '---'."
                   "Do not generate any other text asside from the top {:d} items, "
                   "their indices, and the delimiter.".format(n, n))
    response = ollama.generate(model="gemma2:2b", prompt="".join(message))
    logger.info("Ollama Batch Raw Response: '" + response.response + "'")
    try:
        new_items = [
            item.strip()
            for item in response.response.split("---")
            if item.strip() != ""
        ]

        if len(new_items) != n:
            logger.error("Ollama Batch Filter: Bad number of items {:d}".format(len(new_items)))
            raise Exception()
        else:
            logger.info("Ollama Batch Filter: {:d} items".format(len(new_items)))

        for item in new_items:
            logger.info("Ollama Batch Filtered Item: '" + item + "'")
        indices: set[int] = {
            int(item.split("\n")[-1])
            for item in new_items
        }
            
        logger.info("Ollama Batch Finished: {:f}".format(time()))
        return [
            o_item
            for o_item in items
            if int(o_item.split("\n")[0][12:]) in indices
        ]
    except:
        logging.error("Ollama Batch Filter: retrying")
        return ollama_batch(items, n, search)


def ollama_reduce(items: list[str], n: int, search: str) -> list[str]:
    """
    Will
    """
    x = 0
    y = 5
    list_of_items = []
    while y < len(items):
        split_items = items[x:y]
        x = y
        y += 5
        filters = ollama_batch(split_items,n,search)
        list_of_items.extend(filters)
    if len(list_of_items) > n: 
        return ollama_batch(list_of_items, n, search)
    return list_of_items


def chat_interface():
    while True:
        user_query = input(
            "Howdy there! I'm Craig - what can I help you find today?\n"
            "Please give me the name of a file to read items from,\n"
            "and then tell me what you're looking for.\n"
            "Enter 'exit' to exit this conversation.\n"
        )
        if (user_query == "exit"):
            return
        logger.info("Query Received ({:f}): ".format(time()) + user_query)
        parsed_query = ollama.generate(
            model="gemma2:2b",
            prompt=
            "Please parse the following text to get a filename and "
            "an item description of what the user is looking for. "
            "Please do not paraphrase the description of what the user is looking for, "
            "and use their exact words. "
            "Please put just the name of the file on "
            "the first line of your output with no other text "
            "and the description of the item the user is looking for "
            "on the second line of your output with no other text:\n\n" + user_query
        )
        parsed_query = parsed_query.response.split("\n")
        logger.info("Query Filename Parsed: " + parsed_query[0])
        logger.info("Query Search Parsed: " + "\n".join(parsed_query[1:]))

        items = process_input(parsed_query[0])
        item_pool = ItemPool([Item(desc, index) for index, desc in enumerate(items)])
        item_pool.prune_until(parsed_query[1], 3)
        good_items = [i.desc for i in item_pool.items]

        logger.info("Query Answered ({:f})".format(time()))
        print("These are the items I think would be a good match:")
        for item in good_items:
            print(item)

if __name__ == "__main__":
    logging.basicConfig(filename='craig.log', level=logging.INFO)
    logger.info('Craig has awoken...')

    chat_interface()

    logger.info('Craig has gone back to sleep... for now...')

