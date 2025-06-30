// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

contract FairExchangePbb {
    enum Status { Accepted, Rejected, Undefined }
    struct Party {
        address account;
        Status status;
    }

    Party public partyA;
    Party public partyB;

    constructor(address _partyA, address _partyB) {
        partyA = Party({
            account: _partyA,
            status: Status.Undefined
        });

        partyB = Party({
            account: _partyB,
            status: Status.Undefined
        });
    }

    function isParty(address _addr) public view returns (bool) {
        return (_addr == partyA.account || _addr == partyB.account);
    }

    modifier onlyParty() {
        require(isParty(msg.sender), "Only parties can call this");
        _;
    }

    modifier notRejected() {
        require(partyA.status != Status.Rejected && partyB.status != Status.Rejected, "The exchange was rejected");
        _;
    }

    function accept() external onlyParty notRejected {
        if (msg.sender == partyA.account) {
            partyA.status = Status.Accepted;
        }

        if (msg.sender == partyB.account) {
            partyB.status = Status.Accepted;
        }
    }

    function reject() external onlyParty notRejected {
        if (msg.sender == partyA.account) {
            partyA.status = Status.Rejected;
        }

        if (msg.sender == partyB.account) {
            partyB.status = Status.Rejected;
        }
    }

    function release() public onlyParty view returns (bool) {
        return (partyA.status == Status.Accepted) && (partyB.status == Status.Accepted);
    }
}