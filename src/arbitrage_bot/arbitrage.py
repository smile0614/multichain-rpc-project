# src/arbitrage_bot/arbitrage.py
import os
import time
import threading
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from dotenv import load_dotenv
from .dex_swapper import UniswapSwapper, CurveSwapper

load_dotenv()

class ArbitrageBot:
    def __init__(self):
        # Initialize DEX swappers for both chains
        self.uniswap_swapper = UniswapSwapper()
        self.curve_swapper = CurveSwapper()
        
        # Set up account credentials
        self.sender_address = Web3.to_checksum_address(os.getenv('SENDER_ADDRESS'))
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Trade parameters
        self.trade_amount = 100  # USDC amount in dollars
        self.slippage = 0.005    # 0.5% slippage tolerance

    def execute_trades(self):
        """Execute simultaneous trades on both DEXes using threads"""
        try:
            # Create threads for parallel execution
            uniswap_thread = threading.Thread(
                target=self._execute_uniswap_trade
            )
            curve_thread = threading.Thread(
                target=self._execute_curve_trade
            )

            # Start and wait for both threads
            uniswap_thread.start()
            curve_thread.start()
            
            uniswap_thread.join()
            curve_thread.join()

        except Exception as e:
            print(f"Arbitrage failed: {str(e)}")
            # Add transaction reversal logic here if needed

    def _execute_uniswap_trade(self):
        """Swap USDC to USDT on Uniswap (Arbitrum)"""
        try:
            # Get contract instance
            contract = self.uniswap_swapper.contract
            
            # Build transaction
            tx = contract.functions.swapExactTokensForTokens(
                self.trade_amount,
                int(self.trade_amount * (1 - self.slippage)),
                # [self.uniswap_swapper.USDC_ADDRESS, self.uniswap_swapper.USDT_ADDRESS],
                [Web3.to_checksum_address(os.getenv('USDC_ADDRESS')), Web3.to_checksum_address(os.getenv('USDT_ADDRESS'))],
                self.sender_address,
                int(time.time() + 1200)  # 20 minute deadline
            ).build_transaction({
                'chainId': self.uniswap_swapper.connector.chain_id,
                'gas': 250000,
                'gasPrice': self.uniswap_swapper.connector.w3.eth.gas_price,
                'nonce': self.uniswap_swapper.connector.w3.eth.get_transaction_count(self.sender_address)
            })

            # Sign and send transaction
            signed_tx = self.uniswap_swapper.connector.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.uniswap_swapper.connector.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Wait for confirmation
            receipt = self.uniswap_swapper.connector.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Uniswap trade successful: {tx_hash.hex()}")

        except ContractLogicError as e:
            print(f"Uniswap contract error: {str(e)}")
        except TransactionNotFound:
            print("Uniswap transaction timeout")
        except Exception as e:
            print(f"Uniswap trade failed: {str(e)}")

    def _execute_curve_trade(self):
        """Swap USDT to USDC on Curve (Optimism)"""
        try:
            # Get contract instance
            contract = self.curve_swapper.contract
            
            # Build transaction
            tx = contract.functions.exchange(
                # self.curve_swapper.USDT_POOL_INDEX,
                # self.curve_swapper.USDC_POOL_INDEX,
                2,
                1,
                self.trade_amount,
                int(self.trade_amount * (1 - self.slippage))
            ).build_transaction({
                'chainId': self.curve_swapper.connector.chain_id,
                'gas': 250000,
                'gasPrice': self.curve_swapper.connector.w3.eth.gas_price,
                'nonce': self.curve_swapper.connector.w3.eth.get_transaction_count(self.sender_address)
            })

            # Sign and send transaction
            signed_tx = self.curve_swapper.connector.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.curve_swapper.connector.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Wait for confirmation
            receipt = self.curve_swapper.connector.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Curve trade successful: {tx_hash.hex()}")

        except ContractLogicError as e:
            print(f"Curve contract error: {str(e)}")
        except TransactionNotFound:
            print("Curve transaction timeout")
        except Exception as e:
            print(f"Curve trade failed: {str(e)}")

if __name__ == "__main__":
    bot = ArbitrageBot()
    bot.execute_trades()