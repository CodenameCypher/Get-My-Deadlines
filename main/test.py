import datetime

string = '2021-06-29 17:59:00+00:00'
hours = datetime.timedelta(hours=6)
my_time = datetime.datetime.strptime(string, '%Y-%m-%d  %H:%M:00+00:00')
new_time = (my_time+hours).strftime("%A %d %B, %I:%M%p")
print(datetime.datetime.now())
print((my_time+hours))
print((my_time+hours) < datetime.datetime.now())
