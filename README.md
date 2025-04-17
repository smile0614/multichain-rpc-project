# Multichain RPC Interaction System

A blockchain interaction system handling:
1. Simple Ethereum RPC interactions
2. Cross-chain arbitrage between DEXes
3. Multichain order book system design

## Features
- Ethereum testnet block listener
- Automated transaction every 10 blocks
- Cross-chain arbitrage between Uniswap (Arbitrum) and Curve (Optimism)
- System design for multichain order book

## Requirements
- Python 3.9+
- Web3.py
- python-dotenv
- Ethereum account with testnet ETH

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

## Run
```bash
python -m src.simple_rpc.listener
python -m src.arbitrage_bot.arbitrage
```