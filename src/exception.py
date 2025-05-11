

class CyberSystemException(Exception):
    def __init__(self, details: str, status: int,*args):
        self.details = details
        self.status = status
        super().__init__(*args)