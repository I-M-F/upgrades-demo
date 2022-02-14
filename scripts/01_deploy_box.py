from scripts.helpful_scripts import get_account, encode_function_data  
from brownie import Contract, network, Box, ProxyAdmin, TransparentUpgradeableProxy  

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    # implementation contract
    box = Box.deploy({"from": account})

    #Hooking up a proxy to our implementation contract
    proxy_admin = ProxyAdmin.deploy({"from": account})
    #initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy =  TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account, "gas_limit": 1000000})

    print(f"Proxy deployed to  {proxy}, you can now upgarde to V2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"Here is the initial value in the Box: {proxy_box.retrieve()}")
