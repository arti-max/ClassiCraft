import pprint as pp


class Logger:
    def __init__(self, name):
        self.__name = name
    
    def log(self, message):
        try:
            print(f"[{self.__name}] LOG: {message}")
        except Exception as e:
            print(f"[{self.__name}] ERROR: {e}")