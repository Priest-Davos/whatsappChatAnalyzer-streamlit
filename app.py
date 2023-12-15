import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
from imojify import imojify
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer 💥")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['USER'].unique().tolist()
    user_list.remove("Group notification")
    user_list.sort()
    user_list.insert(0, "OVERALL")

    selected_user = st.sidebar.selectbox("Show analysis ", user_list)

    st.dataframe(helper.show_all_messages(selected_user, df))

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_of_links = helper.fetch_stats(selected_user, df)
        st.title("TOP STATISTICS")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_of_links)

        # Monthly timeline
        st.title("MONTHLY TIMELINE")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['TIME'], timeline["MESSAGE"], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("DAILY TIMELINE")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['ONLY_DATE'], daily_timeline["MESSAGE"], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map (user most active in which day)
        st.title("ACTIVITY MAP")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values , color="red")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # showing heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(17, 12))
        ax = sns.heatmap(user_heatmap)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # finding the busiest users in the group(Group Leval)
        if selected_user == "OVERALL":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="green")
                plt.xlabel("USERS NAME")
                plt.ylabel("NUMBER OF MESSAGES")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("WORDCLOUD")
        df_wc = helper.create_wordcloud(selected_user, df)  # returns an image
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)

        # most common words
        st.title("MOST COMMON WORDS")
        most_common_words_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words_df[0], most_common_words_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # st.dataframe(most_common_words_df)

        # emoji analysis
        st.title("EMOJI ANALYSIS")
        emoji_df = helper.emoji_helper(selected_user, df)
        if len(emoji_df) != 0:

            def offset_image(cords, emoji, ax):
                img = plt.imread(imojify.get_img_path(emoji))
                im = OffsetImage(img, zoom=0.03)
                im.image.axes = ax
                ab = AnnotationBbox(im, (cords[0], cords[1]), frameon=False, pad=0)
                ax.add_artist(ab)


            col1, col2 = st.columns(2)
            with col2:
                st.text("List of used emojis")
                st.dataframe(emoji_df)
            with col1:
                fig, ax = plt.subplots(figsize=(7, 9))

                ax.bar(range(len(emoji_df[0].head(15))), emoji_df[1].head(15), width=0.6,  align="center")
                ax.set_xticks(range(len(emoji_df[0].head(15))))
                ax.set_xticklabels([])
                ax.tick_params(axis='x', which='major', pad=26)
                ax.set_ylim((0, ax.get_ylim()[1] + 10))

                for i, e in enumerate(emoji_df[0].head(15)):
                    offset_image([i, emoji_df[1].head(15)[i] + 5], e, ax)
                # ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

                st.pyplot(fig)
                st.text("------------- Most used emojis ---------------")
        else:
            st.text("Sorry ! Messages contains no emojis")









