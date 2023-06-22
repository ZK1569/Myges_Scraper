from pymongo import MongoClient
from pprint import pprint

class MongoConnect():
    def __init__(self):
        client = MongoClient("mongodb://root:passwordRoot@localhost:27017/")
        self.db =  client.mimir_knowledge
        self.users = self.db.Users          # Users Collection 

    def getUserLogin(self, user_id: str):
        """
            Returns saved user information ( email and password )

            Return : 
                type(Tuple) => idx[0] = email, 
                               idx[1] = password
        """
        userInfo = self.users.find_one({"user_id" : user_id})
        return (userInfo["email"], userInfo["password"])

    def isUserSaved(self, username: str):
        """
            Checks if the user exists in the database
            
            Return : 
                type(boolean)
        """
        userInfo = self.users.find_one({"user_id" : username})
        if userInfo : return True
        
        return False

    def saveLogin(self, user_id: str, email: str, password: str):
        """ 
            Save user information in database (username, email, password)
        """
        user = {
            "user_id" : user_id,
            "email" : email,
            "password" : password
        }

        self.users.insert_one(user).inserted_id


if __name__ == "__main__":
    db = MongoConnect()
    # db.saveLogin("zk1569", "test@mail.com", 'password234')
    # print(db.getUserLogin("zk1569"))
