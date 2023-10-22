pragma solidity ^0.4.17;

contract Inbox {
    string public message;

    function Inbox(String initialMessage) public {
        message = initialMessage;
    }

    function setMessage(string newMessage) public{
        message=newMessage;
    }
}