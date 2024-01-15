import socket
import threading
import pickle

class Account:
    def __init__(self, username, auth_token):
        self.username = username
        self.auth_token = auth_token

class MessagingServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.accounts = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def handle_client(self, client_socket):
        request_data = client_socket.recv(1024)
        request = pickle.loads(request_data)

        if request['action'] == 'create_account':
            username = request['username']
            auth_token = hash(username)  # Simulating authentication token generation
            account = Account(username, auth_token)
            self.accounts.append(account)
            response = {'status': 'success', 'auth_token': auth_token}
        elif request['action'] == 'show_accounts':
            accounts_list = [acc.username for acc in self.accounts]
            response = {'status': 'success', 'accounts': accounts_list}
        elif request['action'] == 'send_message':
            auth_token = request['auth_token']
            recipient = request['recipient']
            message_body = request['message_body']
            
            sender_account = next((acc for acc in self.accounts if acc.auth_token == auth_token), None)
            recipient_account = next((acc for acc in self.accounts if acc.username == recipient), None)

            if sender_account and recipient_account:
                message = {'sender': sender_account.username, 'receiver': recipient, 'body': message_body, 'isRead': False}
                recipient_account.messageBox.append(message)
                response = {'status': 'success', 'message': 'Message sent successfully'}
            else:
                response = {'status': 'error', 'message': 'Invalid sender or recipient'}

        elif request['action'] == 'show_inbox':
            auth_token = request['auth_token']
            account = next((acc for acc in self.accounts if acc.auth_token == auth_token), None)

            if account:
                inbox_messages = [{'message_id': idx, 'from': msg['sender'], 'body': msg['body'], 'isRead': msg['isRead']} for idx, msg in enumerate(account.messageBox, start=1)]
                response = {'status': 'success', 'inbox_messages': inbox_messages}
            else:
                response = {'status': 'error', 'message': 'Invalid auth token'}

        elif request['action'] == 'read_message':
            auth_token = request['auth_token']
            message_id = request['message_id']
            account = next((acc for acc in self.accounts if acc.auth_token == auth_token), None)

            if account and 0 < message_id <= len(account.messageBox):
                message = account.messageBox[message_id - 1]
                message['isRead'] = True
                response = {'status': 'success', 'message': message}
            else:
                response = {'status': 'error', 'message': 'Invalid auth token or message ID'}

        elif request['action'] == 'delete_message':
            auth_token = request['auth_token']
            message_id = request['message_id']
            account = next((acc for acc in self.accounts if acc.auth_token == auth_token), None)

            if account and 0 < message_id <= len(account.messageBox):
                del account.messageBox[message_id - 1]
                response = {'status': 'success', 'message': 'Message deleted successfully'}
            else:
                response = {'status': 'error', 'message': 'Invalid auth token or message ID'}
        else:
            response = {'status': 'error', 'message': 'Invalid action'}

        client_socket.send(pickle.dumps(response))
        client_socket.close()

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python Server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = MessagingServer('localhost', port)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
