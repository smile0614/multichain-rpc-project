# src/simple_rpc/listener.py
import os
import time
from web3 import Web3
from web3.exceptions import TransactionNotFound
from dotenv import load_dotenv
from .transaction_handler import send_eth_transaction

load_dotenv()

class BlockListener:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(
            f"https://sepolia.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
        ))
        self.block_counter = 0
        self.required_confirmations = 2

    def start(self):
        print("Starting Ethereum block listener...")
        latest_block = self.w3.eth.block_number
        while True:
            try:
                current_block = self.w3.eth.block_number
                if current_block > latest_block:
                    self.block_counter += current_block - latest_block
                    latest_block = current_block
                    print(f"New block: {current_block}")

                    if self.block_counter >= 10:
                        self._trigger_transaction()
                        self.block_counter = 0
                
                time.sleep(15)
            except Exception as e:
                print(f"Connection error: {str(e)}")
                time.sleep(60)

    def _trigger_transaction(self):
        try:
            tx_hash = send_eth_transaction(
                self.w3,
                Web3.to_checksum_address(os.getenv('SENDER_ADDRESS')),
                os.getenv('PRIVATE_KEY'),
                Web3.to_checksum_address(os.getenv('RECEIVER_ADDRESS')),
                self.w3.to_wei(0.001, 'ether')
            )
            print(f"Transaction sent: {tx_hash.hex()}")
        except Exception as e:
            print(f"Transaction failed: {str(e)}")

if __name__ == "__main__":
    listener = BlockListener()
    listener.start()