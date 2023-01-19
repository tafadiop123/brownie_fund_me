from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

# On definit nos environnements de developpement
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
# On definit nos environnements forke
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

## On peut mettre les valeurs statiques sur le haut du CODE
DECIMALS = 8
STARTING_PRICE = 200000000000

## On definit une fonction qui verifie si on est dans un reseau de developpement ou de test ou de fork
def get_account():
    # if network.show_active() == "development":
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


## on instancie une fonction pour le deploiement d'un Mock
def deploy_mocks():
    # Si on est en lacal on deploie un Mock pour l'addresse d'approvisionnement des donnees du prix
    print(f"Le reseau actif est {network.show_active()}")
    print("Deploiement du Mock....")
    # Pour eviter qu'il ait plusieurs Mock qui sont deployes en utilisant celui qui est actif
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            # 18, 2000000000000000000000, {"from": account}
            # On peut diminuer ce nombre qui se trouve en haut
            ##La fonction .toWei va ajouter 18 zeros a 2000
            DECIMALS,
            STARTING_PRICE,
            {"from": get_account()},
        )
    print("La maquette est deploye!!!")
