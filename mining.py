import argparse
import logging
import random
import time
from datetime import datetime
from timeit import repeat, timeit

from blockchain import Block, BlockChain


parser = argparse.ArgumentParser(description="BlockChain")

parser.add_argument("-f", "--filename", type=str, default=None, help="Filename to display the log. (default stdout)")

parser.add_argument("-s", "--show", action="store_true",help="Output the final chain in the log")

_args = parser.parse_args()

def get_random_date() -> str:
    return datetime.fromtimestamp(random.uniform(0, time.time())).strftime(
        "%d/%m/%Y, %H:%M:%S"
    )


BLOCKS: list[Block] = [
    Block(
        index=i,
        timestamp=get_random_date(),
        data={
            "dump_data": "data",
        },
    )
    for i in range(1, 11)
]


def test_BlockChain(difficult: int = 2) -> str:
    chain = BlockChain(difficult)
    for block in BLOCKS:
        chain.addBlock(block)
    return str(chain)

if __name__ == "__main__":
    stmt = """
for i in range(1,6):
    test_BlockChain(i)
    """

    logging.basicConfig(
    level=logging.INFO,
    filename=_args.filename,
    filemode="w",
    format="%(asctime)s - %(message)s\n",
    datefmt="%d/%m/%Y %H:%M:%S",
)

    for i in range(1,3):

    # results = repeat(stmt=stmt, number=100, repeat=5, globals=globals())
    # print(results)


# logging.debug("debug")
# logging.info("info")
# logging.warning("warning")
# logging.error("error")
# logging.critical("critical")
