import json
from datetime import datetime
from hashlib import sha256


class Block:
    def __init__(
        self, index: int, timestamp: str, data: dict, previous_hash: str = ""
    ) -> None:
        """
        Args:
            index (int):Indicates where the block sits on the chain

            timestamp (str): When the block was created

            data (Any): Any type of data that the blocks holds

            previous_hash (str, optional): The hash of the block before this one. Defaults to "".
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """calculate_hash

        Calculates the hash of this block

        Returns:
            str: The has of the block[]
        """
        bindex = self.index.to_bytes()
        btimestamp = self.timestamp.encode()
        bdata = json.dumps(self.data).encode()
        bprevious_hash = self.previous_hash.encode()
        return sha256(bindex + bdata + btimestamp + bprevious_hash).hexdigest()

    def update_hash(self) -> None:
        self.hash = self.calculate_hash()

    def __repr__(self) -> str:
        return str(self.__dict__)


class BlockChain:
    def __init__(self) -> None:
        self.n_blocks: int = 1
        self.chain: list[Block] = [self.__create_genesis_block()]

    def __create_genesis_block(self) -> Block:
        return Block(0, datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), {})

    def addBlock(self, new_block: Block) -> None:
        new_block.previous_hash = self[-1].hash
        new_block.update_hash()
        self.chain.append(new_block)

    def __getitem__(self, index) -> Block:
        return self.chain[index]

    def __repr__(self) -> str:
        return str(self.__dict__)
