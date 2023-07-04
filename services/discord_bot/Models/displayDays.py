from Models.oneDayModel import oneDay
from typing import List

class DisplayShedul:

    def one_day_display(data:List[oneDay]):
        for day in data:

            yield f"Tu as cours a {day.date_start.split()[1]} de **{day.course}** avec {day.teacher} a {day.classroom}"

