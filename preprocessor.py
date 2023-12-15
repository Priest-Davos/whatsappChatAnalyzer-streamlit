import re
import pandas as pd


def preprocess(data):

    pattern = '\d\d/\d\d/\d\d\d\d,\s\d{1,2}:\d\d\s[a|p]m\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert message data types
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([^:]*):\s', message)
        # print(entry)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group notification')
            messages.append(entry[0])
    df['USER'] = users
    df['MESSAGE'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['YEAR'] = df['date'].dt.year
    df['MONTH'] = df['date'].dt.month_name()
    df['MONTH_NUM'] = df['date'].dt.month
    df['DAY'] = df['date'].dt.day
    df['HOUR'] = df['date'].dt.hour
    df['MINUTE'] = df['date'].dt.minute
    df['ONLY_DATE'] = df['date'].dt.date
    df["DAY NAME"] = df["date"].dt.day_name()

    period = []
    for hour in df[['DAY NAME', 'HOUR']]['HOUR']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['TIME PERIOD'] = period

    return df


