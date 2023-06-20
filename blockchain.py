import json
from datetime import datetime
from hashlib import sha256
from typing import Any


class ChainException(Exception):
    """
    ChainException

    Class that warns an invalid Chain
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Block:
    """Block Class

    Class to represent an Block in a Blockchain
    """

    def __init__(
        self,
        index: int,
        timestamp: str,
        data: dict[str, Any],
        previous_hash: str = "",
    ) -> None:
        """
        Args:
            index (int):Indicates where the block sits on the chain

            timestamp (str): When the block was created

            data (Any): Any type of data that the blocks holds

            previous_hash (str, optional): The hash of the block before this one. Defaults to "".
        """
        self.index: int = index
        self.timestamp: str = timestamp
        self.data: dict[str, Any] = data
        self.previous_hash: str = previous_hash
        self.nonce: int = 0
        self.hash: str = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculates the hash of this block

        Returns:
            str: The hash of the block
        """
        bindex = self.index.to_bytes()
        btimestamp = self.timestamp.encode()
        bdata = json.dumps(self.data).encode()
        bprevious_hash = self.previous_hash.encode()
        bnonce = self.nonce.to_bytes(length=self.nonce.bit_length())
        return sha256(
            bindex + bdata + btimestamp + bprevious_hash + bnonce
        ).hexdigest()

    def update_hash(self) -> None:
        """
        Update the hash of the block.
        """
        self.hash = self.calculate_hash()

    def mine_block(self, difficult: int) -> None:
        """
        Update the block's hash until it start with the number of zeros
        determined by difficult.

        Args:
            difficult (int): Number of difficultity to mine the block.

        Raises:
            ValueError: Raises ValueError if the difficult is less than 0.
        """
        if difficult <= 0:
            raise ValueError("difficult must be greater than 0!")

        prefix = "0" * difficult
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.update_hash()

        # Sometimes when the loop finishes, if the hash is recauculates differs from the actual hash ??????
        if self.hash != self.calculate_hash():
            self.update_hash()
            self.mine_block(difficult)

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)


class BlockChain:
    """BlockChain Class

    Class to represent an Blockchain
    """

    def __init__(self, difficult: int = 2) -> None:
        """
        Args:
            difficult (int, optional): Initial difficult to add a new Block in the BlockChain. Defaults to 2.
        """
        self.difficult = difficult
        self.chain: list[Block] = [self.__create_genesis_block()]

    def __create_genesis_block(self) -> Block:
        """
        Creates the first Block of the BlockChain

        Returns:
            Block: The first Block of the chain
        """
        return Block(0, datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), {})

    def addBlock(self, new_block: Block) -> None:
        """
        Adds a new Block in the BlockChain mining the new Block with the BlockChain difficult.

        Args:
            new_block (Block): The Block to be added in the chain
        """
        if not self.isChainValid():
            print(self)
            raise ChainException("Invalid BlockChain!")
        new_block.previous_hash = self[-1].hash
        new_block.mine_block(self.difficult)
        self.chain.append(new_block)

    def isChainValid(self) -> bool:
        """
        Verify if the BlockChain is valid.

        Returns:
            bool: True if the BlockChain is valid False otherwise.
        """
        return all(
            cur.hash == cur.calculate_hash() and cur.previous_hash == prev.hash
            for prev, cur in zip(self.chain[:-1], self.chain[1:])
        )

    def __getitem__(self, index: int) -> Block:
        return self.chain[index]

    def __len__(self) -> int:
        return len(self.chain)

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda x: x.__dict__, indent=4)


if __name__ == "__main__":
    a = Block(
        1,
        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        {"nome": "vinicius", "age": 23},
    )
    b = Block(
        2,
        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        {"nome": "matheus", "age": 54},
    )
    c = Block(
        3,
        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        {"nome": "Vitor", "age": 12},
    )
    chain = BlockChain()
