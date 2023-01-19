// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

//On devra d'abord importer le package fourni par Chainlink
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
//On va importer la librairie SafeMath de Chainlink
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

//On cree un contrat capable de recevoir de l'argent
contract FundMe {
    //Pour utiliser la librairie SafeMath on utilise le mot cle "using"
    using SafeMathChainlink for uint256;
    //On fait un mapping de l'adresse qui a envoye les fonds
    mapping(address => uint256) public addressToAmountFunded;
    //On intancie un array qui stocke l'addresse de ceux qui ont envoyes des fonds
    address[] public funders;

    //On instancie l'addresse du proprietaire
    address public owner;
    //On instancie une fonction globale
    AggregatorV3Interface public priceFeed;

    //On cree un "constructor" pour defenir le proprietaire du contrat
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    //On instancie la fonction de paiement avec le mot cle "payable"
    function fund() public payable {
        //On peut parametrer le prix de notre fonction fund sur n'importe quel prix que l'on souhaite en dollar (50$)
        //Maintenant on mettre un un seuil de reception de fonds en dollar (ici le seuil minimum est de 50$)
        uint256 minimumUSD = 50 * 10**18; /*mais en Wei*/
        //La fonction "require" va verifier si le montant recu est superieur a 50$ en Wei
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "Tu as besoin d'envoyer plus d'Etherum !"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        //On met l'addresse de ceux qui ont envoyes les fonds dans l'array
        funders.push(msg.sender);
        //Quel est le taux de conversion entre ETH et USD et comment l'avoir dans le smart contrat ?
    }

    //On cree une fonction qui recupere la version a partir du contrat externe
    function getVersion() public view returns (uint256) {
        //AggregatorV3Interface /*le type de l'interface*/ fluxPrix = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e/*l'addresse ou l'on trouve les donnees du prix*/);
        return
            //fluxPrix.version(); /*on renvoi la version de l'interface utilise*/
            priceFeed.version(); /*on renvoi la version de l'interface utilise*/
    }

    //Maintenant on cree une fonction qui recupere et nous renvoie le dernier prix
    function getPrice() public view returns (uint256) {
        //AggregatorV3Interface fluxPrix = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        //On peut juste garder la variable answer, en mettant rien sur les autres variables de retour pour eviter les erreurs de compilation
        //(, int256 answer, , , ) = fluxPrix.latestRoundData();
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return
            uint256(
                answer * 10000000000 /*pour obtenir le prix en Wei*/
            ); /*sera le prix qu'on va convertir par un type casting en unit256*/
    }

    //On cree une fonction qui est en mesure de convertir la somme recu en Etherum en Dollar
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 prixEth = getPrice();
        uint256 ethAmountInUsd = (prixEth * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
        // le resultat donne = 1279603316090 et en le convertissant en dollar on a : 0,000001279603316090 le prix d'un Gwei en Dollar
    }

    //On cree une fonction qui recupere les frais d'entrees
    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    //Les "modifiers"
    modifier onlyOwner() {
        //On souhaite que seul le proprietaire du contrat puisse retirer les fonds
        require(msg.sender == owner);
        _;
    }

    //On instancie la fonction de retrait avec mot cle payable
    function withdraw() public payable onlyOwner {
        //la fonction native "tranfer" permet d'envoyer des ethers d'une adresse a un autre
        msg.sender.transfer(
            address(
                this /*represente le contrat dans lequel nous sommes*/
            ).balance /*pour envoyer tous les fonds recus*/
        );
        //un fois que les fonds sont retires on va remettre l'array des envoyeurs de fonds a zero
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //On va mettre l'adresse des envoyeurs de fonds dans un nouveau array
        funders = new address[](0);
    }
}
