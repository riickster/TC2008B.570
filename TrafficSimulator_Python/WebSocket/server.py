import logging
from websocket_server import WebsocketServer

# Function to handle incoming messages from clients
def message_received(client, server, message):
    print("Client %d sent: %s" % (client['id'], message))
    server.send_message_to_all(message)

# Create a WebSocket server on localhost, port 9001
server = WebsocketServer(port=1123, host='localhost', loglevel=logging.INFO)

# Set the function to handle incoming messages
server.set_fn_message_received(message_received)

# Start the server
server.run_forever()
