
# LendMaker

This is the python Backend of a dApp backend that handles the transactions on the provided contract url (Loan Contract) , it uses firebase for authentication and mongodb to store the public address of user's metamask account , currently the project uses Ganache's Test Net tokens for both lending and borrowing.
This is platform where you can register, add friends and request loans




## Dependencies:
- MongoDB
- Firebase Authentication
- Ganache
- Trufle
- Metamask

Make sure you have Ganache/CLI installed, setup a firebase Authentication app and use its service account key json file in the project. You also need to have trufle installed to deploy the contract

Then you need to setup the enviornment variables.
## Enviornment Variables
Create a .env file and add the following variables:
- SECRET_KEY for jwt authentication
- FIREBASE_CRADENTIALS 
Path to your service account json file which you can get by creating a firebase app, go to Authentication and enable it and select providers as google and got to settings then download the serviceAccount.json file
- GANACHE URL
- CONTRACT_ADDRESS
The contract address should be the public address of the deployed contract when you deploy the contract the public key should appear in the terminal/console.
- CONTRACT_ABI_PATH
To get the contract address you have to deploy the contract and use the path of a file name LoanContract.json from the blockchain folder

## How to run this project:
- First deploy the contract using truffle (Make sure you are inside the folder named Blockchain)
    ```bash
    npm install truffle
    truffle compile
    truffle migrate 
- Then setup the env and install the requirements using:
    ```bash
    pip install -r requirements.txt
- Now simply run the project using:
    ```bash
    uvicorn app.main:app --reload