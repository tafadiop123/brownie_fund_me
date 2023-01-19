from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

# on definit une fonction qui verifie si on peut financer et retirer sur un compte
def test_can_fund_and_withdraw():
    # Arranging
    account = get_account()
    # Acting
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # Asserting
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# On definit une fonction pour verifier si seul le proprietaire du compte peut faire des retraits
def test_only_owner_can_withdraw():
    # On defini une condition pour sauter le test quand on n'est pas en local
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Seulement pour les tests en local")
    # Arranging
    # account = get_account()
    # Acting
    fund_me = deploy_fund_me()
    bad_actors = accounts.add()
    # fund_me.withdraw({"from": bad_actors})
    # Gerer les exceptions du test
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actors})
