# Smart Fair Exchange

<p>This repository contains the implementation of a Fair Exchange protocol. The main component is a Solidity smart contract that implements a Public Bulletin Board (PBB).</p>

## How to Execute

> In this example, we will use the [Remix IDE](https://remix.ethereum.org).

### Upload

- Go to the "File Explorer" section.
- Open the contracts folder.
- Press the "Open from your file system" button and upload the [pbb.sol](./pbb.sol) file.

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

> Use the `release` method to view the current state of the smart contract
