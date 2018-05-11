## Synopsis

Light Line is a proof of concept for using bitcoin to pay for public transportation rides, utilizing payment channels that minimize the cost of sending transactions, while offering incentives to users and reducing costs for public transportation companies.
Our team of engineers created this project during the bitemBassy (bitemBassy.org) hackathon in Tel Aviv, Israel. 
The project utilizes the Lightning Network (http://lightning.network/) which is running on the Bitcoin blockchain and enables lightning fast and low fee transactions. 

## Functionality

### NFC integration
Light Line includes a mobile app written in react native that utilizes NFC scanning to capture ride data once the user gets on a transportation vehicle.
The library "react-native-nfc"

### Server
Light Line Server is built using a powerfull async architecture, ready to scale-up and to handle very large amounts of users.  with the [python][std] [tornado][std2] server we are keeping it open-source, while using proffesional tools. 

### postgresql DB


### c-lightning and lightning-charge
[c-lightning][std] offers a JSON-RPC integration with the Lightning Network to interact with nodes, channels, and payments
[lightning-charge][std2] offers an HTTP API to create requests (invoice) as well as webhooks when a payment channel received payment

[std]:https://github.com/ElementsProject/lightning
[std2]:https://github.com/ElementsProject/lightning-charge
## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License
  
You may use under the terms of GNU - General Public License version 2
