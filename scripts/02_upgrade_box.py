from scripts.helpful_scripts import get_account, encode_function_data, upgrade  
from brownie import Contract, network, Box, ProxyAdmin, TransparentUpgradeableProxy, BoxV2  

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    # implementation contract
    box = Box.deploy({"from": account}, publish_source=True)

    #Hooking up a proxy to our implementation contract
    proxy_admin = ProxyAdmin.deploy({"from": account})
    #initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy =  TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account, "gas_limit": 1000000})

    print(f"Proxy deployed to  {proxy}, you can now upgarde to V2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(f"Here is the initial value in the Box: {proxy_box.retrieve()}")
    # Upgrade to new contract
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin_contract = proxy_admin)
    upgrade_transaction.wait(1)
    print("Proxy has been updated!!..")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi )
    proxy_box.increment({"from": account})
    print(f"Here is the value in the Box: {proxy_box.retrieve()}, after upgrade")
