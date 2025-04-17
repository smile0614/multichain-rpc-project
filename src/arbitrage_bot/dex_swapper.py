# src/arbitrage_bot/dex_swapper.py
from web3 import Web3
import json
import os
from .chain_connectors import ArbitrumConnector, OptimismConnector

class DexSwapper:
    def __init__(self, connector, contract_address, abi_path):
        self.connector = connector
        with open(abi_path) as f:
            abi = json.load(f)
        self.contract = connector.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

class UniswapSwapper(DexSwapper):
    def __init__(self):
        super().__init__(
            ArbitrumConnector(),
            # os.getenv('UNISWAP_ADDRESS'),
            Web3.to_checksum_address(os.getenv('UNISWAP_ADDRESS')),
            'abis/uniswap.json'
        )

class CurveSwapper(DexSwapper):
    def __init__(self):
        super().__init__(
            OptimismConnector(),
            # os.getenv('CURVE_ADDRESS'),
            Web3.to_checksum_address(os.getenv('CURVE_ADDRESS')),
            'abis/curve_pool.json'
        )