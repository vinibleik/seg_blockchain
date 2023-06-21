import argparse
import logging
import random
import time
from datetime import datetime
from timeit import timeit

from blockchain import Block, BlockChain

parser = argparse.ArgumentParser(description="BlockChain")

parser.add_argument(
    "-f",
    "--filename",
    type=str,
    default=None,
    help="Filename to display the log. (Default = stdout)",
)

parser.add_argument(
    "-t",
    "--time",
    type=float,
    default=300.0,
    help="Maximum time to wait to mine a block in seconds. (Default = 300)",
)

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


def test_BlockChain(difficult: int = 2) -> None:
    chain = BlockChain(difficult)
    for block in BLOCKS:
        chain.addBlock(block)


if __name__ == "__main__":
    if _args.filename is not None:
        with open(_args.filename, mode="w"):
            pass

    logging.basicConfig(
        level=logging.INFO,
        filename=_args.filename,
        filemode="a+",
        format="%(asctime)s - %(message)s\n",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    i = 1
    result = 0
    max_time = _args.time
    while result < max_time:
        result = timeit(
            stmt=f"test_BlockChain({i})",
            number=1,
            globals=globals(),
        )
        log = f"Difficulty: {i}\n"
        log += f"Mean(Insert an block)  (s): {result / 10}"
        log += f"\nMean(Insert 10 blocks) (s): {result}"
        logging.info(log)
        i += 1
