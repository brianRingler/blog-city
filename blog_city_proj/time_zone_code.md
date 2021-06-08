# Time Zone Code
* [Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
* [strftime Directives](https://strftime.org/)
* [Date-Time Tutorial](https://www.tutorialspoint.com/How-to-convert-date-and-time-with-different-timezones-in-Python)

## Time Zone Scratch Pad
    print('----++++++++------++++++++---------')
    # Comment Date Before Converting 
    print(f'Comment Date before converted: {comm_created_at}\n')

    # Django returns date with lowercase am/pm convert to uppercase
    converted_time = comm_created_at.replace('a.m.', 'AM').replace('p.m.', 'PM')
    print(f'Converted am/pm to AM/PM: {converted_time}\n')

    # Need to convert comm_create_at from string to datetime obj
    comment_date = datetime.strptime(converted_time, '%B %d, %Y, %I:%M %p')  
    print(f'New Comment Date Format: {comment_date}')
    print(f'New Date Type: {type(comment_date)}')
    print()

    # What is the active_user time zone
    active_user = User.objects.get(id=request.session['active_user_id'])
    print(f'The Active User Time Zone is: {active_user.timezone}')
    updated_tz = pytz.timezone(active_user.timezone)
    print(f'User Time Zone Type: {type(updated_tz)}')
    print(f'User Time Zone is: {updated_tz}\n')
    
    # This should convert UTC time to EST time but it does NOT
    comment_date_aware = comment_date.astimezone(pytz.timezone(str(updated_tz)))
    print(comment_date_aware)
    print()

    print(f'What is the data type? ==> {type(comment_date_aware)}\n')
    print(comment_date_aware.tzinfo)
    print(comment_date_aware)
    print('---------------------------')
    print(comment_date_aware.tzinfo)
    print('---------------------------')
    



    # To compare with Django datetime and check if I have correct object types 
    date_now = datetime.now()
    print(type(date_now))
    print(date_now.tzinfo)

    # Convert date_now from naive to aware 
    print('+++++++++++++++++++++++++++++')
    date_now_aware = updated_tz.localize(date_now)
    print(date_now_aware)
    print('++++++++++++++++++++++++\n')
    print(f'Date Time NOW => {date_now_aware}')
    print(f'Date Time Comment => {comment_date_aware}')
    diff_seconds = date_now_aware - comment_date_aware
    print(diff_seconds)
***
## Random Testing Code 
***
* active_user = User.objects.get(id=request.session['active_user_id'])
* updated_tz = pytz.timezone(active_user.timezone)
* updated_comm_create_at = comment_date.astimezone(updated_tz)
* print(f'Update Comment Date/Time: {updated_comm_create_at}')  
* print(f'User-id {topic_id}, Com-id {comment_id}, Top-id {topic_id}, * Com-create {converted_time}')

## Random code testing 
```
# print('++++++++++++++++++++++++++++++++++++++++++++++++++++')

# # convert string to datetime object
# comment_date = datetime.strptime(converted_time, '%B %d, %Y, %H:%M')
# # convert datetime object to 24 hours - takes datetime obj returns string 
# comment_24 = datetime.strftime(comment_date, '%Y/%m/%d %H:%M:%S')
# print(f'Comment 24 hour format: {comment_24}')
# print(type(comment_24))

# updated_time = comment_24.astimezone(updated_tz)
# print(f'The updated time: {updated_time}')

# now = datetime.now()
# now_24 = now.strftime('%Y/%m/%d %H:%M:%S')

# print(f'Comment Date 24?? >>> {comment_date}')
# print(f'NOW >>> {now_24}\n')

# duration = datetime.now() - comment_date
# duration_sec = duration.total_seconds()

# # 30 minutes is 1800 seconds 
# print(duration_sec / 60)
# if duration_sec > 1800:
#     print('Not able to delete')
# else:
#     print('You are DELETED')

# tz = time_zone()
# for t in tz:
#     print(t)
```

## Useful Sites:
* [strftime Directives](https://strftime.org/)