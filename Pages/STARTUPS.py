import streamlit as st
import pandas as pd
import altair as alt
from functions import Barplot, DataFrame

st.set_page_config(layout='wide',page_title="Startups")

df = pd.read_csv("startup_funding.csv")
st.title("Analysis Based On Startups")

st.markdown("""---""")
color1 = 'Orange'
color2 = 'Blue'

# # Sidebar filters
# st.sidebar.header("Filters")
# selected_year = st.sidebar.selectbox("Select Year", df['year'].unique())
# selected_vertical = st.sidebar.selectbox("Select Vertical", df['vertical'].unique())
# selected_startup = st.sidebar.selectbox("Select Startup", df['startup'].unique())

# # Filter the DataFrame based on selections
# filtered_df = df[(df['year'] == selected_year) & (df['vertical'] == selected_vertical) & (df['startup'] == selected_startup)]

# # Top Funded Startups
# top_funded = df.groupby('startup')['amount'].sum().reset_index().sort_values(by='amount', ascending=False).head(10)

# # Bar chart for Top Funded Startups
# st.subheader("Top Funded Startups")
# top_funded_chart = alt.Chart(top_funded).mark_bar().encode(
#     x=alt.X('amount:Q', title='Total Funding Amount'),
#     y=alt.Y('startup:N', sort='-x', title='Startup'),
#     tooltip=['startup', 'amount']
# ).properties(width=600, height=400)

# st.altair_chart(top_funded_chart, use_container_width=True)

# # Startup Growth Over Time
# growth_over_time = df.groupby(['year', 'startup'])['amount'].sum().reset_index()

# # Line chart for Startup Growth Over Time
# st.subheader("Startup Growth Over Time")
# growth_chart = alt.Chart(growth_over_time).mark_line().encode(
#     x=alt.X('year:O', title='Year'),
#     y=alt.Y('amount:Q', title='Total Funding Amount'),
#     color='startup:N',
#     tooltip=['year', 'startup', 'amount']
# ).properties(width=600, height=400)

# st.altair_chart(growth_chart, use_container_width=True)

# # Funding Distribution
# st.subheader("Funding Distribution by Amount")
# distribution_chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X('amount:Q', bin=True, title='Funding Amount'),
#     y=alt.Y('count():Q', title='Number of Startups'),
#     tooltip=['count()']
# ).properties(width=600, height=400)

# st.altair_chart(distribution_chart, use_container_width=True)

# # Funding Rounds by Startup
# rounds_by_startup = df.groupby('startup')['round'].count().reset_index().sort_values(by='round', ascending=False)

# # Bar chart for Funding Rounds
# st.subheader("Funding Rounds by Startup")
# rounds_chart = alt.Chart(rounds_by_startup).mark_bar().encode(
#     x=alt.X('round:Q', title='Number of Rounds'),
#     y=alt.Y('startup:N', sort='-x', title='Startup'),
#     tooltip=['startup', 'round']
# ).properties(width=600, height=400)

# st.altair_chart(rounds_chart, use_container_width=True)

# # Footer
# st.markdown("Data Source: Your dataset description here")

st.header("Amount Based Analysis")

st.subheader("Top Funded Startups")
n1 = st.slider("Select n:",3,15,5, key='st1')
data1 = df.groupby('startup')['amount'].sum().reset_index().sort_values(by = ['amount','startup'],ascending=[False, True])
# data = data.drop(index=3)
data1 = data1[:n1]
data1 = data1.reset_index(drop=True)
data1.index = data1.index + 1
type1 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st2')
if type1=='BarPlot':
    Barplot(n1,data1, 'amount', 'startup',1)
else:
    DataFrame(n1,data1, True)


st.subheader("Least Funded Startups")
n2 = st.slider("Select n:",3,15,5, key='st3')
temp1 = df[df['amount']>0] 
data2 = temp1.groupby('startup')['amount'].sum().reset_index().sort_values(by = ['amount','startup'],ascending=[True, True])
# data = data.drop(index=3)

data2 = data2[:n2]
data2 = data2.reset_index(drop=True)
data2.index = data2.index + 1
type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st4')
if type2=='BarPlot':
    Barplot(n2,data2, 'amount', 'startup',1, least=True)
else:
    DataFrame(n2,data2, True)


st.markdown("""---""")


st.header("Year Wise Analysis")

years = df['year'].unique()
years.sort()
year = st.selectbox("Select Year:", years, key='st7')
st.subheader(f"Top Funded Startups In {year}")
n3 = st.slider("Select n:",3,15,5, key='st5')
temp2 = df[df["year"]==year]
data3 = temp2.sort_values(by = ['amount','startup'],ascending=[False, True])
data3 = data3[['startup','amount']]
data3 = data3[:n3]
data3 = data3.reset_index(drop=True)
data3.index = data3.index + 1
type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st6')
if type2=='BarPlot':
    Barplot(n3,data3, 'amount', 'startup',1)
else:
    DataFrame(n3,data3, True)


year1 = st.selectbox("Select Year:", years, key='st8')
st.subheader(f"Least Funded Startups In {year1}")
n4 = st.slider("Select n:",3,15,5, key='st9')
temp3 = df[df["year"]==year1]
temp3 = temp3[temp3['amount']>0]
data4 = temp3.sort_values(by = ['amount','startup'],ascending=[True, True])
data4 = data4[['startup','amount']]
data4 = data4[:n4]
data4 = data4.reset_index(drop=True)
data4.index = data4.index + 1
default_option = 'BarPlot' if data4['amount'][n4] > data4['amount'][1] else 'DataFrame'
type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st10',index=['BarPlot','DataFrame'].index(default_option))
# type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st10')
if type2=='BarPlot':
    Barplot(n4,data4, 'amount', 'startup',1, least=True)
else:
    DataFrame(n4,data4, True)

st.markdown("""---""")

st.header("Vertical Wise Analysis")
temp4 = df['vertical'].value_counts().reset_index()
vert = list(temp4['vertical'])

li = st.multiselect("Select Vertical(s): ", vert,[vert[i] for i in [4, 7, 9]])
n5 = st.slider("Select n:",3,15,5, key='st11')
temp5 = df[df['vertical'].isin(li)]
data5 = temp5.sort_values(by = ['amount','startup'],ascending=[False, True])
data5 = data5[['startup','amount', 'vertical']]
data5 = data5[:n5]
data5 = data5.reset_index(drop=True)
data5.index = data5.index + 1
type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='st12')
if type2=='BarPlot':
    Barplot(n5,data5, 'amount', 'startup',1, vertical = True)
else:
    DataFrame(n5,data5, True)

st.markdown("""---""")
