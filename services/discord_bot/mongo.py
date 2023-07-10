from pymongo import MongoClient
from pprint import pprint
from typing import List

from Models.studentModel import Student

import os 
from dotenv import load_dotenv

load_dotenv()

class MongoConnect():
    def __init__(self):
        client = MongoClient(str(os.getenv('MONGO_URL')))
        self.db =  client.mimir_knowledge
        self.users = self.db.Users          # Users Collection 
        self.homework = self.db.Homework
        self.students = self.db.Students

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
        if userInfo : return userInfo
        
        return False

    def saveLogin(self, user_id: str, id: str, password: str):
        """ 
            Save user information in database (username, id, password)
        """
        user = {
            "user_id" : user_id,
            "id" : id,
            "password" : password,
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
    
    def addHomework(self,user_discord_id, date, text):
        try:
            user_db_id = self.isUserSaved(user_discord_id)

            if user_db_id:
                self.homework.insert_one({
                    "user_id" : user_db_id['_id'],
                    "date": date,
                    "description": text
                }).inserted_id
            else: return False
        except Exception as e:
            return False

        return True 
    
    def getHomework(self, user_discord_id, date):
        
        try:
            user_db_id = self.isUserSaved(user_discord_id)

            return self.homework.find({"user_id": user_db_id['_id'], "date": date})

        except Exception as e:
            return False
        
    def areStudentsSaved(self):

        nbr_student = self.students.count_documents({})

        return True if nbr_student > 0 else False
    
    def getAllStudents(self) -> List[Student]:
        students = []
        try:
            db_students = self.students.find({})
            for student in db_students:
                students.append(Student(
                    student["image"],
                    student["first_name"],
                    student["last_name"]
                ))
            return students
        except Exception as e:
            return False
    
    def findStudent(self, name):

        try:
            student = self.students.find_one({
                "$or": [
                    {"first_name": name.upper()},
                    {"last_name": name.upper()}
                ]
            })
            return Student(student['image'], student['first_name'], student['last_name'])
        except:
            return False

        
    def saveStudents(self, students:List[Student]):

        if self.areStudentsSaved(): return True
        try:
            for student in students:
                self.students.insert_one({
                    "image" : student.image,
                    "first_name" : str.upper(student.first_name),
                    "last_name" : str.upper(student.last_name)
                })
            return True
        except Exception as e:
            return False
        
        
if __name__ == "__main__":
    db = MongoConnect()
    # db.saveLogin("zk1569", "test@mail.com", 'password234')
    # print(db.getUserLogin("zk1569"))
