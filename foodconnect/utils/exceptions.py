class AppException(Exception):
    def __init__(self, message, status):
        super(AppException, self).__init__(message)
        
        self.status = status