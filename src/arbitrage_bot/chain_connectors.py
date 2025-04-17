# src/arbitrage_bot/chain_connectors.py
from web3 import Web3
import os

class BlockchainConnector:
    def __init__(self, rpc_url, chain_id):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.chain_id = chain_id
        
    def get_balance(self, address, token_contract=None):
        if token_contract:
            return token_contract.functions.balanceOf(address).call()
        return self.w3.eth.get_balance(address)

class ArbitrumConnector(BlockchainConnector):
    def __init__(self):
        super().__init__(
            os.getenv('ARBITRUM_RPC'),
            int(os.getenv('ARBITRUM_CHAIN_ID'))
        )

class OptimismConnector(BlockchainConnector):
    def __init__(self):
        super().__init__(
            os.getenv('OPTIMISM_RPC'),
            int(os.getenv('OPTIMISM_CHAIN_ID'))
        )