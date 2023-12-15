from urlextract import URLExtract   # to extract url from messages
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def show_all_messages(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    return df


def fetch_stats(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    # fetch  number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for message in df['MESSAGE']:
        words.extend(message.split())

    # fetch number of media messages
    num_of_media_messages = df[df['MESSAGE'] == '<Media omitted>\n'].shape[0]

    # fetch number of link shared
    links = []
    for message in df['MESSAGE']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_of_media_messages, len(links)


def most_busy_users(df):
    x = df['USER'].value_counts().head(10)
    df = round((df['USER'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'NAME', 'USER': "MESSAGE %"})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    # stop_words = set(stopwords)
    # stop_words.update(['changed', 'hai', 'security code', 'ho', 'deleted', 'Media', 'omitted', 'omitted Media', 'security code', 'message'])
    # remove notification related words
    temp_df = df[df['USER'] != "Group notification"]
    temp_df = temp_df[temp_df['MESSAGE'] != "<Media omitted>\n"]
    temp_df = temp_df[temp_df['MESSAGE'] != "This message was deleted\n"]
    temp_df = temp_df[temp_df['MESSAGE'] != "You deleted this message\n"]
    wc = WordCloud(stopwords=stop_words, width=600, height=500, min_font_size=7, background_color='white')
    df_wc = wc.generate(temp_df['MESSAGE'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]

    # remove notification related words
    temp_df = df[df['USER'] != "Group notification"]
    temp_df = temp_df[temp_df['MESSAGE'] != "<Media omitted>\n"]
    temp_df = temp_df[temp_df['MESSAGE'] != "This message was deleted\n"]
    temp_df = temp_df[temp_df['MESSAGE'] != "You deleted this message\n"]

    # removing stopwords
    words = []
    for message in temp_df['MESSAGE']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(30))
    return most_common_words_df


def emoji_helper(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]

    emojis = []
    for message in df['MESSAGE']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    timeline = df.groupby(['YEAR', 'MONTH_NUM', 'MONTH']).count()['MESSAGE'].reset_index()
    # merging year and month
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['MONTH'][i] + "-" + str(timeline['YEAR'][i]))
    timeline['TIME'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    daily_timeline = df.groupby('ONLY_DATE').count()['MESSAGE'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    return df['DAY NAME'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "OVERALL":
        df = df[df['USER'] == selected_user]
    return df['MONTH'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'OVERALL':
        df = df[df['USER'] == selected_user]
    user_heatmap = df.pivot_table(index='DAY NAME', columns='TIME PERIOD', values='MESSAGE', aggfunc='count').fillna(0)
    return user_heatmap











    # num_messages = df[df['USER'] == selected_user].shape[0]
    # words = []
    # for message in df[df['USER'] == selected_user]['MESSAGE']:
    #     words.extend(message.split())
    # return num_messages, len(words)


# updated  as if selected user is not overall then update dataframe acc to selected user
    # if selected_user == "OVERALL":
    #     num_messages = df.shape[0]
    #     words = []
    #     for message in df['MESSAGE']:
    #         words.extend(message.split())
    #     return num_messages, len(words)
    #
    # else:
    #     new_df = df[df['USER'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['MESSAGE']:
    #         words.extend(message.split())
    #     return num_messages, len(words)



    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #
    # def create_wordcloud(selected_user, df):
    #     if selected_user != "OVERALL":
    #         df = df[df['USER'] == selected_user]
    #     f = open('stop_hinglish.txt', 'r')
    #     stopwords = f.read()
    #     stop_words = set(stopwords)
    #     stop_words.update(
    #         ['changed', 'hai', 'security code', 'ho', 'deleted', 'Media', 'omitted', 'omitted Media', 'security code',
    #          'message'])
    #     wc = WordCloud(stopwords=stop_words, width=500, height=500, min_font_size=10, background_color='white')
    #     n_wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    #     df_wc = wc.generate(df['MESSAGE'].str.cat(sep=" "))
    #     n_df = n_wc.generate(df['MESSAGE'].str.cat(sep=" "))
    #     if n_df != df_wc:
    #         print("Dead")
    #     return df_wc



