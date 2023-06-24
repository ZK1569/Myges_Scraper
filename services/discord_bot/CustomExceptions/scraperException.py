class idOrPasswordIncorrect(Exception):
    """Exception raised during login if the id or password is incorrect """
    
    def __init__(self, message="ID or password is not valid"):
        self.message = message
        super().__init__(self.message)


class scheduleShowError(Exception):
    """Sometimes myGes does not display the weekly calendar. Please try again """

    def __init__(self, message="MyGes does not display the weekly calendar. Please try again"):
        self.message = message
        super().__init__(self.message)