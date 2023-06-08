import re
import pandas as pd

def preprocess(data):
    pattern = '[0-9]{2}/[0-9]{2}/[0-9]{2},\s[0-9]{1,2}:[0-9]{1,2}\s[a-zA-Z]{2}\s-\s'


    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    datereplace = []

    for i in dates:
        ireplace = i.replace('\u202f', ' ')
        datereplace.append(ireplace)

    df = pd.DataFrame({'user_message': messages, 'message_date': datereplace})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M %p - ')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])


    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], axis='columns', inplace=True)
    df["year"] = df["message_date"].dt.year
    df["month"] = df["message_date"].dt.month_name()
    df["date"] = df["message_date"].dt.day
    df["hour"] = df["message_date"].dt.hour
    df['only_date'] = df['message_date'].dt.day
    df["minute"] = df["message_date"].dt.minute
    df['day_name'] = df['message_date'].dt.day_name()
    df['month_num'] = df['message_date'].dt.month

    return df