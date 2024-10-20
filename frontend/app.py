from client import get_articles, send_email
import streamlit as st
import pandas as pd
from datetime import datetime

articles = get_articles()

created_date = datetime.strptime(articles[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
created_date_time = created_date.strftime("%Y-%m-%d %H:%M:%S")
created_date_weekday = created_date.strftime("%A")
days_ago = (datetime.today() - created_date).days
created_date_extra_string = ""
if days_ago == 0:
    created_date_extra_string = "(Today)"
else:
    created_date_extra_string = f"({created_date_weekday}), which is {days_ago} days ago"

st.title('News Summarizer')
st.write(f"Retrieved {created_date_time} {created_date_extra_string}")

articles_df = pd.DataFrame(articles)
articles_display_df = articles_df[["id", "title", "category", "bullet_points"]].copy()
articles_display_df['include'] = False

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


