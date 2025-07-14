// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

contract FairExchangePbb {
    enum Status { Accepted, Rejected, Undefined }
    struct Party {
        address account;
        string token;
        Status status;
    }

    Party public partyA;
    Party public partyB;

    event ExchangeAccepted(address indexed party, string token);
    event ExchangeRejected(address indexed party, string token);
    event ExchangeCompleted(address indexed partyA, address indexed partyB, string tokenA, string tokenB);

    constructor(address accountA, address accountB) payable {
        require(msg.value == 0, "No ETH allowed");
        require(accountA != address(0), "A: zero address");
        require(accountB != address(0), "B: zero address");
        require(accountA != accountB, "Same addresses");

        partyA.account = accountA;
        partyA.token = "";
        partyA.status = Status.Undefined;

        partyB.account = accountB;
        partyB.token = "";
        partyB.status = Status.Undefined;
    }

    function isParty(address _addr) public view returns (bool) {
        return (_addr == partyA.account || _addr == partyB.account);
    }

    modifier onlyParty() {
        require(isParty(msg.sender), "Not a party");
        _;
    }

    modifier isRejected() {
        require(partyA.status != Status.Rejected && partyB.status != Status.Rejected, "Already rejected");
        _;
    }

    modifier isAccepted() {
        require(!(partyA.status == Status.Accepted && partyB.status == Status.Accepted), "Already accepted");
        _;
    }

    function accept(string memory token) external onlyParty isRejected isAccepted {
        address sender = msg.sender;

        Party storage pa = partyA;
        Party storage pb = partyB;

        if (sender == pa.account && pa.status != Status.Accepted) {
            pa.status = Status.Accepted;
            pa.token = token;
            emit ExchangeAccepted(sender, token);
        }

        if (sender == pb.account && pb.status != Status.Accepted) {
            pb.status = Status.Accepted;
            pb.token = token;
            emit ExchangeAccepted(sender, token);
        }

        if (pa.status == Status.Accepted && pb.status == Status.Accepted) {
            emit ExchangeCompleted(pa.account, pb.account, pa.token, pb.token);
        }
    }

    function reject(string memory token) external onlyParty isRejected isAccepted {
        address sender = msg.sender;

        Party storage pa = partyA;
        Party storage pb = partyB;

        if (sender == pa.account && pa.status != Status.Rejected) {
            pa.status = Status.Rejected;
            pa.token = token;
            emit ExchangeRejected(sender, token);
        }

        if (sender == pb.account && pb.status != Status.Rejected) {
            pb.status = Status.Rejected;
            pb.token = token;
            emit ExchangeRejected(sender, token);
        }
    }

    function release() public onlyParty view returns (Party memory, Party memory) {
        return (partyA, partyB);
    }
}
