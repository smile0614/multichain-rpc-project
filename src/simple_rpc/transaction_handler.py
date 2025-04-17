# src/simple_rpc/transaction_handler.py
from web3 import Web3
from web3.exceptions import TransactionNotFound

def send_eth_transaction(w3, sender, priv_key, receiver, amount):
    try:
        nonce = w3.eth.get_transaction_count(sender)
        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': amount,
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': w3.eth.chain_id
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, priv_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status != 1:
            raise Exception("Transaction reverted")
            
        return tx_hash
    except TransactionNotFound:
        raise Exception("Transaction timeout")
    except Exception as e:
        raise Exception(f"Send transaction failed: {str(e)}")