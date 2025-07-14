# Smart Fair Exchange

This repository contains a fair exchange implementation between two parties: Alice and Bob. It includes their applications ([appA](./appA/) for Alice, [appB](./appB/) for Bob) and attestable services ([attA](./attA/) for Alice, [attB](./attB/) for Bob). The core component is a [Solidity smart contract](./pbb.sol) implementing the Public Bulletin Board (PBB) logic.

## How to Execute

> **Note**: This guide focuses on smart contract deployment. For application and attestable setup, see their respective folders.

> **Important**: The synchronization protocol can be validated using only the smart contract, without running applications or attestables.

> **Recommended**: Use [Remix IDE](https://remix.ethereum.org) for testing.

### Upload

1. Navigate to the "File Explorer" section
2. Open the contracts folder
3. Click "Open from your file system" button and upload the [pbb.sol](./pbb.sol) file

### Compile

- Navigate to the "Solidity Compiler" section.
- Compile the uploaded smart contract.

### Deploy

- Go to the "Deploy and Run Transactions" section.
- Select two Ethereum account addresses from the account selector and paste them in the <i>Deploy</i> input field, separated by a comma. Example: `0x5B38Da6a701c568545dCfcB03FcB875f56beddC4,0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2`
- Click the <i>Deploy</i> button to deploy the contract.

### Run

- Under the "Deployed Contracts" section, expand the latest deployment.
- Select an account from the account selector that you used in the "Deploy" step.
- Fill the "accept" input with an "Accept Token". In a production environment, this would be a secret token signed by the attestables. For testing purposes, we can simulate it by using the following convention:
  - SA: Party A accepts the exchange
  - CA: Party A rejects the exchange
  - SB: Party B accepts the exchange
  - CB: Party B rejects the exchange

> **Tip**: Call the `release` method anytime to check the current state of both parties.
