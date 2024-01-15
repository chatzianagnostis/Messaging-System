# Messaging System

## Introduction
This project implements a simple messaging system with a server and client in Python. The system allows users to create accounts, send messages, and manage their inbox.

## Files
- `server.py`: Contains the implementation of the messaging server.
- `client.py`: Implements a client to interact with the messaging server.

## Classes

### `Account`
Represents a user account with a username and authentication token.

### `MessagingServer`
Implements the messaging server, allowing account creation, message sending, and inbox management.

### `MessagingClient`
A client interface to interact with the messaging server. Provides methods to create accounts, send messages, and manage the inbox.

## Usage

### Running the Server
To run the server, use the following command:
```bash
python server.py <port_number>
```
Replace <port_number> with the desired port.

### Running the Server
- Create Account (Function ID: 1)
```bash
python client.py <server_ip> <server_port> 1 <username>
```
Creates an account for the user with the specified username and returns a unique authentication token.
- Show Accounts (Function ID: 2)
```bash
python client.py <server_ip> <server_port> 2 <authToken>
```
Displays a list of all accounts in the system.
- Send Message (Function ID: 3)
```bash
python client.py <server_ip> <server_port> 3 <authToken> <recipient> <message_body>
```
Sends a message to the specified recipient.
- Show Inbox (Function ID: 4)
```bash
python client.py <server_ip> <server_port> 4 <authToken>
```
Displays a list of all messages in the user's inbox.
- Read Message (Function ID: 5)
```bash
python client.py <server_ip> <server_port> 5 <authToken> <message_id>
```
Displays the content of a specific message and marks it as read.
- Delete Message (Function ID: 6)
```bash
python client.py <server_ip> <server_port> 6 <authToken> <message_id>
```
Deletes a specific message from the user's inbox.

## Examples

### Server
```bash
python server.py 5000
```

### Client
Create Account
```bash
python client.py localhost 5000 1 demouser
```
Show Accounts
```bash
python client.py localhost 5000 2 <authToken>
```
Send Message
```bash
python client.py localhost 5000 3 <authToken> friend "Hello, friend!"
```
Show Inbox
```bash
python client.py localhost 5000 4 <authToken>
```
Read Message
```bash
python client.py localhost 5000 5 <authToken> 1
```
Delete Message
```bash
python client.py localhost 5000 6 <authToken> 1
```
Make sure to replace `<server_ip>`, `<server_port>`, `<authToken>`, `<username>`, `<recipient>`, `<message_body>`, and `<message_id>` with the appropriate values.

## Notes
- Ensure that the server is running before attempting to use the client.
- The provided examples assume the server is running on localhost and port 5000. Adjust the parameters accordingly based on your setup.
