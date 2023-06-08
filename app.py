import streamlit as st
from matplotlib import pyplot as plt

import preprocessor,funs
import matplotlib.pyplot
st.sidebar.title("Whatsapp Chat Analyzer")
st.title("IK What's UP")
st.header("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)


    user_list= df['user'].unique().tolist()

    if "group_notification" in df['user']:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0, "Group Analysis")

    selected_user=st.sidebar.selectbox("Select user to Perform analysis", user_list)

    if st.sidebar.button("Perform Analysis"):
        max_msg,freq=funs.most_msg(selected_user,df)
        msg_count, word_count,media_count=funs.fetch_stats(selected_user, df)
        st.title("Base Statistics :")
        col1, col2, col3, col4= st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(msg_count)
        with col2:
            st.header("Total Words")
            st.subheader(word_count)
        with col3:
            st.header("Total Media Shared")
            st.subheader(media_count)
        with col4:
            st.header("Most sent Message")
            st.subheader(f"{max_msg} ({freq} times)")
# monthly timeline
        st.title('Activity Map')
        st.header("Monthly Timeline")
        timeline = funs.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline.time, timeline.message, color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.header("Daily Timeline")
        daily_timeline = funs.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #   Weekly activity
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=funs.week_activity(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
                st.header("Most Busy Month")
                busy_month = funs.month_activity(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        if selected_user=="Group Analysis":
            st.title("Most Active Users")
            x,percdf = funs.most_active(selected_user, df)
            fig, ax = plt.subplots()

            col5,col6=st.columns(2)

            with col5:
                ax.bar(x.index,x.values,color="#32d4e4")
                ax.set_facecolor("black")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col6:
                st.dataframe(percdf)
        #  word cloud
        st.title("Word Cloud")

        df_wc=funs.createwordcloud(selected_user,df)
        fig, ax=plt.subplots()
        # fig.set_size_inches(20, 10)
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)
        # Most common words

        st.title("Most Commonly Used Words ")
        commonwords_df = funs.common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(commonwords_df.Word, commonwords_df.Frequency, color="#32d4e4")
        col7,col8=st.columns(2)
        plt.xticks(rotation='vertical')
        with col7:
            st.pyplot(fig)
        with col8:
            st.dataframe(commonwords_df)

        st.title("Most Commonly Used Emojis ")
        emoji_df = funs.emoji_count(selected_user, df)
        fig, ax = plt.subplots()
        ax.pie(emoji_df.Frequency, labels=emoji_df.Emoji,autopct="%0.2f")
        col9, col10 = st.columns(2)
        plt.xticks(rotation='vertical')
        with col9:
            st.pyplot(fig)
        with col10:
            st.dataframe(emoji_df)


