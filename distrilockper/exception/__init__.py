class ArgumentError(BaseException):
    def __init__(self, message="Not enough input arguments"):
        self.__message = message

    def __str__(self):
        return self.__message
