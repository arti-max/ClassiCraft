from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self):
        super().__init__()
        self.__is_freeze = False
        self.__position_before_freeze = None

    # def freeze(self):
    #     self.__is_freeze = True
    #     self.gravity = 0

    # def unfreeze(self):
    #     self.__is_freeze = False
    #     self.gravity = 1

    # def update(self):
    #     if self.__is_freeze:
    #         self.position = self.__position_before_freeze
