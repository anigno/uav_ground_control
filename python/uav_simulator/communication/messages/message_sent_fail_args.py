from python.uav_simulator.communication.messages.message_base import MessageBase

class MessageSentFailsArgs:
    def __init__(self, exception: Exception = None, message: MessageBase = None, text=''):
        self.exception = exception
        self.message = message
        self.text = text
