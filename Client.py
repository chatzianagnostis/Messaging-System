import socket
import pickle
import sys

class MessagingClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.auth_token = None

    def send_request(self, action, data=None):
        if data is None:
            data = {}
        request = {'action': action, 'auth_token': self.auth_token, **data}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_ip, self.server_port))
            client_socket.send(pickle.dumps(request))
            response_data = client_socket.recv(1024)
            response = pickle.loads(response_data)
        return response

    def create_account(self, username):
        response = self.send_request(1, {'username': username})
        if response['status'] == 'success':
            self.auth_token = response['auth_token']
            print(f"Account created successfully. Your Auth Token is: {self.auth_token}")
        else:
            print(f"Error: {response['message']}")

    def show_accounts(self):
        response = self.send_request(2)
        if response['status'] == 'success':
            print("List of Accounts:")
            for idx, username in enumerate(response['usernames'], start=1):
                print(f"{idx}. {username}")
        else:
            print(f"Error: {response['message']}")

    def send_message(self, recipient, message_body):
        response = self.send_request(3, {'recipient': recipient, 'message_body': message_body})
        print(f"Response: {response['message']}")

    def show_inbox(self):
        response = self.send_request(4)
        if response['status'] == 'success':
            print("Inbox Messages:")
            for msg in response['inbox_messages']:
                status_indicator = "*" if not msg['isRead'] else ""
                print(f"{msg['message_id']}. from: {msg['from']} {status_indicator}")
        else:
            print(f"Error: {response['message']}")

    def read_message(self, message_id):
        response = self.send_request(5, {'message_id': message_id})
        if response['status'] == 'success':
            print(f"({response['message']['sender']}) {response['message']['body']}")
        else:
            print(f"Error: {response['message']}")

    def delete_message(self, message_id):
        response = self.send_request(6, {'message_id': message_id})
        print(f"Response: {response['message']}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python Client.py <server_ip> <server_port> <function_id> <additional_args>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    function_id = int(sys.argv[3])
    additional_args = sys.argv[4:]

    client = MessagingClient(server_ip, server_port)

    if function_id == 1:
        client.create_account(additional_args[0])
    elif function_id == 2:
        client.show_accounts()
    elif function_id == 3:
        client.send_message(additional_args[0], additional_args[1])
    elif function_id == 4:
        client.show_inbox()
    elif function_id == 5:
        client.read_message(int(additional_args[0]))
    elif function_id == 6:
        client.delete_message(int(additional_args[0]))
    else:
        print("Invalid function_id. Supported function_ids: 1, 2, 3, 4, 5, 6")
