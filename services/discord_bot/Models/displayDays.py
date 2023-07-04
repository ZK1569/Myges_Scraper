from Models.oneDayModel import oneDay
from Models.oneWeekModel import oneWeekModel
from typing import List

class DisplayShedul:

    def one_day_display(data:List[oneDay]):
        for day in data:

            yield f"Tu as cours a {day.date_start.split()[1]} de **{day.course}** avec {day.teacher} a {day.classroom}"

    def one_week_display(data:list[oneWeekModel]):
        for day in data:
            yield f"Le {day.day} a {day.time} tu as **{day.couse}** avec {day.teacher} a {day.classroom} ({day.modality})"