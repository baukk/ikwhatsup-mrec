import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji

import pandas as pd


def fetch_stats(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    # msg_count
    msg_count = df.shape[0]

    # word count
    words = []
    for message in df['message']:
        words.extend(message.split())
    word_count = len(words)
    #  media count
    media_count = df[df['message'] == '<Media omitted>\n'].shape[0]
    return msg_count, word_count, media_count


def most_msg(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    newdf = df[df["message"].str.contains("null\n") == False]
    newdf1 = newdf[newdf["message"].str.contains("<Media omitted>\n") == False]
    max_msg = newdf1["message"].value_counts().idxmax()
    freq = newdf1["message"].value_counts()[0]
    return max_msg, freq


def most_active(selected_user, df):
    x = df["user"].value_counts()
    percdf = round(df["user"].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={"index": "Name", "user": "Percentage"})
    percdf.index += 1

    return x, percdf


def createwordcloud(selected_user, df):
    if selected_user != "Group Analysis":
        df = df[df["user"] == selected_user]
    newdf = df[df["message"].str.contains("null\n") == False]
    newdf1 = newdf[newdf["message"].str.contains("<Media omitted>\n") == False]
    wc = WordCloud(width=500, height=500, min_font_size=5, max_font_size=70, background_color="black")
    df_wc = wc.generate(newdf1["message"].str.cat(sep=" "))
    return df_wc

    # Common words


def common_words(selected_user, df):
    if selected_user != "Group Analysis":
        df = df[df["user"] == selected_user]
    words = []
    for message in df['message']:
        if message != '<Media omitted>\n':
            words.extend(message.split())
    commonwords_df = pd.DataFrame(Counter(words).most_common(20))
    commonwords_df.columns = ['Word', 'Frequency']
    commonwords_df.index += 1
    return commonwords_df


def emoji_count(selected_user, df):
    if selected_user != "Group Analysis":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['Emoji', 'Frequency']
    emoji_df.index += 1
    return emoji_df.head(5)


def monthly_timeline(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    print(timeline)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity(selected_user, df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
