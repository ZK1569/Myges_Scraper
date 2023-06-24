from pymongo import MongoClient

import os 
from dotenv import load_dotenv

load_dotenv()

class MongoConnect():
    def __init__(self):
        client = MongoClient(str(os.getenv('MONGO_URL')))
        self.db =  client.mimir_knowledge
        self.users = self.db.Users          # Users Collection 

    def getUserLogin(self, user_id: str):
        """
            Returns saved user information ( id and password )

            Return : 
                type(Tuple) => idx[0] = id, 
                               idx[1] = password
        """
        userInfo = self.users.find_one({"user_id" : user_id})
        return (userInfo["id"], userInfo["password"])

    def isUserSaved(self, user_id: str):
        """
            Checks if the user exists in the database
            
            Return : 
                type(boolean)
        """
        userInfo = self.users.find_one({"user_id" : user_id})
        if userInfo : return True
        
        return False

    def saveLogin(self, user_id: str, id: str, password: str):
        """ 
            Save user information in database (username, id, password)
        """
        user = {
            "user_id" : user_id,
            "id" : id,
            "password" : password
        }

        try: 
            self.users.insert_one(user).inserted_id
        except:
            return False

        return True

    def deleteLogin(self, user_id: str):
        """
            Deletes a user from the database 
        """
        try:
            self.users.find_one_and_delete({"user_id" : user_id})
            return True
        except:
            return False 
        
if __name__ == "__main__":
    db = MongoConnect()
    # db.saveLogin("zk1569", "test@mail.com", 'password234')
    # print(db.getUserLogin("zk1569"))
