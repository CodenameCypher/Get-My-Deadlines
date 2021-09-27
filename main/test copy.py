from datetime import datetime
from pytz import timezone
import pytz

date_str = "2009-05-05 22:28:15"
datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.timezone('Asia/Dhaka'))
print(datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
