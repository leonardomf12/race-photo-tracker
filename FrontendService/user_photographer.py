from dash import html, dcc, Input, Output, State, ctx

class User:
    def __init__(self):
        self.role = None

        # Define this only inside the get_user_info function after successful login
        self.races = ["race1", "race2", "race3", "race4", "race5"]

        # Get role, races,
        #self.get_user_info()

    @staticmethod # Remove this after
    def login(username, password):
        # Send check request here
        return True

    def get_user_info(self):
        # Get user info -> role + races
        # self.races = ["race1", "race2", "race3", "race4", "race5"]
        pass



