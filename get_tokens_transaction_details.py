import requests

def get_transaction_details(signature, address_):
    endpoint = "https://mainnet.helius-rpc.com/?api-key="
    
    subscription_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            signature,
            {
                "encoding": "json",
                "maxSupportedTransactionVersion": 0
            }
        ]
    }
    
    response = requests.post(endpoint, json=subscription_message)
    result = response.json()


    if result['result'] is None:
        print(f"Transaction non trouvée : {signature}")
        return None

    transaction = result['result']
    instructions = transaction['meta']['logMessages']
    
    
    if "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success" in instructions:
        print("Token")
        PostTokenBalances = transaction["meta"]["postTokenBalances"]
        PreTokenBalances = transaction["meta"]["preTokenBalances"]
        trade = analyze_movement(PreTokenBalances, PostTokenBalances, address_)
        
        return trade
    else:
        print("pas Token")
        return None
        


def analyze_movement(pre_data, post_data, address_):
    movements = []
    
    for pre, post in zip(pre_data, post_data):
        if pre['owner'] == address_ and post['owner'] == address_:
            mint = pre['mint']
            pre_amount = int(pre['uiTokenAmount']['amount'])
            post_amount = int(post['uiTokenAmount']['amount'])
            change_amount = post_amount - pre_amount
            if change_amount != 0:
                movements.append({
                    'mint': mint,
                    'change': change_amount / (10 ** pre['uiTokenAmount']['decimals'])
                })
    
    return movements

if __name__ == "__main__":
    signature = "2n1Y3pabiDup3BCUMtZczahZSF9rurTVccT4nmxicnXjtCWvfipFcJLcXeppL7BbsxWS6uc9ik8YwTyUFwjiFCTH"
    address = "sbxidwwBhkpBAGjcR3FhxzL2pbazF2xppTK249EKKtA"
    
    get_transaction_details(signature, address)
    
    

    
