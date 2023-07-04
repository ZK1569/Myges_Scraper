from typing import List
from Models.gradesModel import GradesModel

class DisplayGrades:

    def displayGrades(data:List[GradesModel]):
        for grade in data:
            yield f"**{grade.course}** => {' | '.join([f'{g}' for g in grade.grades])}"