class MessageBroker():
    def __init__(self):
        self.message_list = list()

    def add_message(self, message):
        self.message_list.append(message)

    def read_messages(self):
        return self.message_list
    
    def clean_messages(self):
        self.message_list = list()