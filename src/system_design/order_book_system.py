# src/system_design/order_book_system.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List

class ChainID(Enum):
    ETHEREUM = 1
    POLYGON = 137
    ARBITRUM = 42161
    OPTIMISM = 10

class Asset(Enum):
    USDC = "USDC"
    USDT = "USDT"
    ETH = "ETH"

@dataclass
class Order:
    order_id: str
    user_id: str
    base_asset: Asset
    quote_asset: Asset
    base_chain: ChainID
    quote_chain: ChainID
    amount: float
    price: float
    gas_budget: float

class OrderBook:
    def __init__(self):
        self.orders: Dict[tuple(Asset, Asset, ChainID, ChainID), List[Order]] = {}
    
    def add_order(self, order: Order):
        key = (order.base_asset, order.quote_asset, 
               order.base_chain, order.quote_chain)
        if key not in self.orders:
            self.orders[key] = []
        self.orders[key].append(order)
    
    def match_orders(self, taker_order: Order) -> List[Order]:
        # Implement price-time priority matching
        # Consider cross-chain settlement
        return []