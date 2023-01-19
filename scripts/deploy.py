from brownie import FundMe, MockV3Aggregator, network, config

# On importe a partir de notre module
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    #########Morceau de code pour le probleme de la boucle lors du deploiement des contrats
    from brownie.network import gas_price
    from brownie.network.gas.strategies import LinearScalingStrategy

    gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

    gas_price(gas_strategy)
    # On appelle la fonction qui definit le compte en fonction du reseau test ou local
    account = get_account()
    # On deploie le contrat FundMe
    # fund_me = FundMe.deploy({"from": account})

    # Quand on se trouve dans un persistant comme Goerli, on utilise l'addresse fournie ci-dessous,
    # sinon on deploie un Mock
    # On devra passer au fichier FundMe l'addresse de l'approvisionement des prix
    ## Pour deployer ete verifier on ajoute ce parametre
    # if network.show_active() != "development":
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    ## Maintenant on peut deployer en fonction du reseau sur lequel on se trouve, avec publication si on est dans un testnet
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account, "gas_price": gas_strategy},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Le contrat est deploye sur {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
