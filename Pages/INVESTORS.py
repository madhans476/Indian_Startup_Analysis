import streamlit as st
import pandas as pd

st.set_page_config(layout='wide',page_title="Investors")

df = pd.read_csv("startup_funding.csv")
st.title("Analysis Based On Investors")

st.markdown("""---""")
color1 = 'Orange'
color2 = 'Blue'

st.header("Year Wise Analysis")

from functions import bar_line_and_df

col_1, col_2 = st.columns(2)

with col_1:
    st.subheader("Number of Investors Year Wise")
    type = st.selectbox("Sub-Type :",['Barplot','Lineplot','Treemap','DataFrame'], key='inves11')
    data = df.groupby('year')['investors'].nunique()
    bar_line_and_df(data, type, 'Count')

with col_2:
    st.subheader("Number of Investments Year Wise")
    type = st.selectbox("Sub-Type :",['Barplot','Lineplot','Treemap','DataFrame'], key='inves12')
    data = df['year'].value_counts()
    bar_line_and_df(data,type, 'Count')

st.markdown("""---""")
st.header("Type of Investment")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Number of Funded Startups")
    subtype = st.selectbox("Sub-Type :",['Barplot','Lineplot','Treemap','DataFrame'], key='inves21')
    data = df[df['amount'] > 0]
    data = data['year'].value_counts()
    bar_line_and_df(data, subtype, 'Count')

with col2:
    st.subheader("Number of Non-Funded Startups")
    subtype = st.selectbox("Sub-Type :",['Barplot','Lineplot','Treemap','DataFrame'], key='inves22')
    data = df[df['amount'] == 0]
    data = data['year'].value_counts()
    bar_line_and_df(data, subtype, 'Count')

st.caption("Non-funding investments include mentorship, marketing, branding, networking opportunities, and resources (workspace, facilities, tools), etc.")
st.markdown("""---""")

st.header("Amount Invested Year Wise")
data = df.groupby(by='year')['amount'].sum()
type = st.selectbox("Sub-Type :",['Lineplot','Treemap','Barplot','DataFrame'], key='inves3')
bar_line_and_df(data,type, 'Amount Funded', ht = 500, bs = 50)
st.markdown("""---""")
