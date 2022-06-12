from datetime import datetime


class Execution:
    success = None
    ended_at = None
    message = None
    data = None

    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.ended_at = datetime.now().strftime("%c")
        if data is not None:
            self.data = data
        else:
            self.data = {}
