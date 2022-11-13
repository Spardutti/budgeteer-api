from datetime import datetime
import math
from rest_framework_simplejwt.authentication import JWTAuthentication


def week_of_month():
    date = datetime.now()
    week_day = date.weekday()
    month_day = date.day
#   returns the week of the month from 1 - 6
    return math.ceil((month_day + 6 - week_day) / 7)

jwt_auth = JWTAuthentication()
def get_auth_token( request):
        token = jwt_auth.authenticate(request)[0]
        return token
    
