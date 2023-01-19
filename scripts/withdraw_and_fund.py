from brownie import FundMe
from scripts.helpful_scripts import get_account

# On defini une fonction pour le financement
def fund():
    # Le plus recent contrat deploye
    fund_me = FundMe[-1]
    account = get_account()
    # La variable pour les frais d'entree
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"Les frais d'entree courantes sont : {entrance_fee}")
    print("Financement...")
    fund_me.fund({"from": account, "value": entrance_fee})


# On defini une fonction pour les retraits
def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
