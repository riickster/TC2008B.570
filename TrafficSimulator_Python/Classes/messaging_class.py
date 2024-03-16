
#* Defines a class for Agent Messaging Broadcast
class MessageBroker():
    def __init__(self):
        self.message_list = list() # Generates the list in which the messsages are being saved

    def add_message(self, message): # Function that adds a new message to the message_list
        self.message_list.append(message)

    def read_messages(self): # Funtion that retrieves all the messages of the message_list
        return self.message_list
    
    def clean_messages(self): # Function that deletes every message in the message_list
        self.message_list = list()