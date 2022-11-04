# import { DateTime } from "luxon";
# export const weekOfMonth = () => {
#     const date = DateTime.now();
#     const dayDate = date.day;
#     const dayWeek = date.weekday;

#     // returns the week of the month from 1 - 6
#     return Math.ceil((dayDate + 6 - dayWeek) / 7);
# };
from datetime import datetime
import math

def week_of_month():
    date = datetime.now()
    week_day = date.weekday()
    month_day = date.day
    return math.ceil((month_day + 6 - week_day) / 7)
    
