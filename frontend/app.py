from client import get_articles, send_email
import streamlit as st
import pandas as pd
from datetime import datetime

articles = get_articles()
today_date = datetime.today().strftime('%Y-%m-%d')
today_weekday = datetime.today().strftime('%A')

st.title(f'News Summarizer: {today_weekday} {today_date}')

articles_df = pd.DataFrame(articles)
articles_display_df = articles_df[["id", "title", "category", "bullet_points"]].copy()
articles_display_df['include'] = False

#summary_df = edited_df[edited_df["include_in_summary"]]
#ids = articles_df.loc[summary_df.index, "id"].tolist()

ids = []

for index, row in articles_display_df.iterrows():
    container = st.container(border=True)
    container.write(f"{row["title"]}")

    bullet_points_list = row["bullet_points"].split("|")
    for point in bullet_points_list:
        container.text(f"* {point.strip()}\n")

    st.checkbox("Interested", key=row["id"])

title = st.text_input("Receiver mail", "")

ids = st.session_state
ids =  [key for key, value in ids.items() if value]

st.write(f"You are interested in {ids}")

if st.button('Send summary', type="primary"):
    send_email(ids, title)
    st.success('Mail sendt - Gi den 1-2 min og sjekk søppelpost', icon="✅")


