import numpy as np
import pandas as pd
import nest_asyncio
import asyncio
from zksync_sdk import HttpJsonRPCTransport, ZkSyncProviderV01, network
nest_asyncio.apply()
from web3 import Web3

alchemy_websocket_std = 'wss://eth-mainnet.g.alchemy.com/v2/11-aYh7etWt7W82Zi3FpGKAZAnG7bkHl'
w3_eth = Web3(Web3.WebsocketProvider(alchemy_websocket_std))
print(w3_eth.isConnected())

alchemy_websocket_polygon = 'wss://polygon-mainnet.g.alchemy.com/v2/RbMCgMlLWtWabcF4F9wU-_unsZtBr3qO'
w3_poly = Web3(Web3.WebsocketProvider(alchemy_websocket_polygon))
print(w3_poly.isConnected())

quicknode_websocket_rinkeby = 'wss://icy-virulent-night.rinkeby.discover.quiknode.pro/fc192a56a5dc88784ec22fa4be3576ced955a213/'
w3_rk = Web3(Web3.WebsocketProvider(alchemy_websocket_polygon))
print(w3_rk.isConnected())

provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.mainnet))

def get_address_info(eth_mainnet,eth_testnet,eth_polygon,eth_zksync):
    information_eth_mainnet ={
        'address':[],
        'balance_in_eth':[],
        'txn_count':[]
        }

    information_eth_rinkeby ={
    'address':[],
    'balance_in_eth':[],
    'txn_count':[]
    }

    information_polygon ={
    'address':[],
    'balance_in_eth':[],
    'txn_count':[]
    }

    for i in eth_mainnet:
        checksum_address = Web3.toChecksumAddress(i)
        no_transactions = w3_eth.eth.get_transaction_count(checksum_address)
        current_balance = w3_eth.eth.get_balance(checksum_address)
        information_eth_mainnet['address'].append(i)
        information_eth_mainnet['balance_in_eth'].append(current_balance/(10**18))
        information_eth_mainnet['txn_count'].append(no_transactions)

    for i in eth_testnet:
        checksum_address = Web3.toChecksumAddress(i)
        no_transactions = w3_eth.eth.get_transaction_count(checksum_address)
        current_balance = w3_eth.eth.get_balance(checksum_address)
        information_eth_rinkeby['address'].append(i)
        information_eth_rinkeby['balance_in_eth'].append(current_balance/(10**18))
        information_eth_rinkeby['txn_count'].append(no_transactions)
    
    for it in eth_polygon:
        checksum_address = Web3.toChecksumAddress(it)
        no_transactions = w3_poly.eth.get_transaction_count(checksum_address)
        current_balance = w3_poly.eth.get_balance(checksum_address)
        information_polygon['address'].append(it)
        information_polygon['balance_in_eth'].append(current_balance/(10**18))
        information_polygon['txn_count'].append(no_transactions)
    
    async def account_info_zksync(zk_addresses):
        information_zksync ={
            'address':[],
            'balance_in_eth':[],
            'txn_count':[]
            
            }

        for i in zk_addresses:
            eth = 'ETH'
            nonce = await provider.get_account_nonce(address=i)
            account_state = (await provider.get_state(i))
            information_zksync['address'].append(i)
            if eth in account_state.verified.balances.keys():
                balance = account_state.verified.balances['ETH']
                amount = balance/ 10**18
                information_zksync['balance_in_eth'].append(amount)
            else:
                information_zksync['balance_in_eth'].append(0)
            information_zksync['txn_count'].append(nonce)

        account_statements_zksync = pd.DataFrame(information_zksync)
        return account_statements_zksync

    
    account_statement_eth_mainnet = pd.DataFrame(information_eth_mainnet)

    account_statement_rinkeby = pd.DataFrame(information_eth_rinkeby)
    
    account_statement_poly = pd.DataFrame(information_polygon)

    address_info_mergeing = pd.concat([account_statement_eth_mainnet,account_statement_rinkeby,account_statement_poly,asyncio.run(account_info_zksync(eth_zksync))])
    address_info_mergeing.to_csv('address_info.csv', index = None)





