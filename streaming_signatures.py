import os
import dotenv

import asyncio
import websockets
import json



import utils
import get_tokens_transaction_details



dotenv.load_dotenv()


async def monitor_address(address):
    url = f"wss://rpc.helius.xyz/?api-key={os.getenv('HELIUS_API_KEY')}"
    print(f"Abonnement aux logs pour {address}")
    
    while True:
        try:
            async with websockets.connect(url) as websocket:
                subscription_message = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [
                        {
                            "mentions": ["all"]
                        },
                        {
                            "commitment": "finalized"
                        }
                    ]
                }

                await websocket.send(json.dumps(subscription_message))
                print(f"Abonné aux logs pour {address}")
                
                while True:
                    response = await websocket.recv()
                    data = json.loads(response)
                    if data.get("params") is not None and data["params"]["result"]["value"]["err"] is None:
                        print(f"Nouveau log de transaction pour {address} :", data["params"]["result"]["value"]["signature"])
                        signature = data["params"]["result"]["value"]["signature"]
                        trade = get_tokens_transaction_details.get_transaction_details(signature, address)
                        print(trade)
        
        except websockets.exceptions.ConnectionClosedError:
            print(f"Connexion fermée pour l'adresse {address}. Tentative de reconnexion...")
            await asyncio.sleep(5)
        
        except Exception as e:
            print(f"Erreur pour l'adresse {address}: {e}")
            break

async def monitor_transactions():
    tasks = [monitor_address(address) for address in utils.load_addresses()]
    await asyncio.gather(*tasks)

asyncio.run(monitor_transactions())