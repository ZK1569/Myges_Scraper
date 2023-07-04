from typing import List

class GradesModel:
    def __init__(self, course:str, teacher:str, coef:str, ects:str, grades:List[str]):
        self.course = course
        self.teacher = teacher
        self.coef = coef
        self.ects = ects
        self.grades = grades