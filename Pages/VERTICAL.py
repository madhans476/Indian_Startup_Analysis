import streamlit as st
import pandas as pd
from functions import DataFrame, Barplot, bar_line_and_df

st.set_page_config(layout='wide', page_title="Major Startup Verticals In India")

df = pd.read_csv("startup_funding.csv")

def funding_bar_plot(n, choice):
    gk = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).reset_index()
    gk = gk.iloc[0:n]
    if choice == "Barplot":
        Barplot(n, gk, 'amount', 'vertical', 1)
    else:
        DataFrame(n, gk, amount=True)

def funding_bar_plot_2(n, choice):
    gk = df.groupby('vertical')['amount'].sum().sort_values(ascending=True).reset_index()
    gk = gk.iloc[0:n]
    if choice == "Barplot":
        Barplot(n, gk, 'amount', 'vertical', 1, False, True)
    else:
        DataFrame(n, gk, amount=True)

# @st.cache_data    
def year_wise(year, check,n):
    gk = df.groupby(['vertical', 'year'])['startup'].count().reset_index(name='count')
    gk = gk[gk['year'] == year].sort_values(by='count', ascending=check).iloc[0:n]
    gk = gk.reset_index(drop=True)
    gk.index = gk.index + 1
    default_option = 'BarPlot' if gk['count'][n] > gk['count'][1] else 'DataFrame'
    if check == True:
        choice = st.selectbox("Type: ", ("Barplot", "DataFrame"), key="id_2" ,index=['BarPlot','DataFrame'].index(default_option))
    else:
        choice = st.selectbox("Type: ", ("Barplot", "DataFrame"), key="id_5")
    if choice == "Barplot":
        Barplot(n, gk, 'count', 'vertical', 1, False, check)
    else:
        DataFrame(n, gk)

# @st.cache_data      
def vertical_analysis(choice, selection):
    df_filtered = df[df['vertical'] == choice]
    data2 = df_filtered['year'].value_counts()
    bar_line_and_df(data2, selection, "count")

def funding_analysis(choice, selection):
    gk = df[df['vertical'] == choice].groupby(['year'])['amount'].sum()
    bar_line_and_df(gk, selection, 'Amount Funded')

## Tab 1

# Barplot based on sum funding
st.title("Analysis Based On Verticals")
st.markdown("""---""")
st.header("Amount Based Analysis")
st.subheader("Most Funded Verticals")
choice1 = st.selectbox("Type: ", ("Barplot", "DataFrame"))
df.columns = df.columns.str.replace(" ", "", regex=False)
n = st.slider("Select n:", 2, 45, 5)
funding_bar_plot(n, choice1)
st.write("\n")

# Least funded
st.subheader("Least Funded Verticals")
choice1 = st.selectbox("", ("Barplot", "DataFrame"), key='id_3')
df.columns = df.columns.str.replace(" ", "", regex=False)
n = st.slider("Select n:", 2, 45, 5, key="id_4")
funding_bar_plot_2(n, choice1)
st.write("\n")

st.markdown("""---""")

# Barplot based on number of startups in every vertical per year
st.header("Year Wise Analysis")
choice = st.selectbox("Select a year:", [x for x in range(2015, 2022)])
st.subheader(f"Top Verticals In {choice}")
n = st.slider("Select n:", 2, 20, 5, key="id_8")
st.write("\n")
year_wise(choice, False,n)

# Least Verticals in a year

# choice = st.selectbox("Select a year:", [x for x in range(2015, 2021)], key="id_6")
st.subheader(f"Least Verticals In {choice}")
# n = st.slider("Select n:", 2, 20, 5, key="id_9")
# choice2 = st.selectbox("Type: ", ("Barplot", "DataFrame"), key="id_5")
st.write("\n")
year_wise(choice, True,n)

st.markdown("""---""")
st.write("\n")
st.header("Vertical Analysis")
gk = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).reset_index()
choice = st.selectbox("Select a vertical:", gk['vertical'])
data = df[df['vertical'] == choice]
ct =data['startup'].count()
st.subheader(f"# Startups from :orange-background[{choice}] : {ct}")

st.subheader('Year Wise Analysis:')
col1, col2 = st.columns(2)
with col1:
    # Vertical Wise Analysis
    st.subheader("Number Of Fundings Year Wise")
    selection = st.selectbox("Options", ['Lineplot','Treemap', 'Barplot', 'DataFrame'], key='selectbox2')
    vertical_analysis(choice, selection)
    st.write("\n")

with col2:
    # Funding analysis
    st.subheader("Amount Funded Year Wise")
    selection = st.selectbox("Options", ['Lineplot','Treemap', 'Barplot', 'DataFrame'], key='selectbox1')
    funding_analysis(choice, selection)

#! -------------------------------------------------------------------------------------------------------------------

st.subheader(f"Major Hubs Of {choice}")
df['city'] = df['city'].str.replace(" ", "", regex=False)

fk = df[df['vertical'] == choice]
citi = pd.read_csv('cities.csv')
citi['city'] = citi['city'].str.replace(" ", "", regex=False)
merged_data = citi[citi['city'].isin(fk['city'])]

if 'lat' in merged_data.columns and 'lon' in merged_data.columns:
    st.map(merged_data[['lat', 'lon']], color='#86FD02')
else:
    st.error("The city data is missing 'latitude' and 'longitude' columns.")


st.markdown("""---""")
st.header('Compare Verticaals')
vertical_names = sorted(list(df['vertical'].unique()))
selected_vertical = st.multiselect('Select the states:', vertical_names, default=[vertical_names[i] for i in [8, 11]])
from functions import grouped_bar, lollipop, grouped_df

st.subheader("Amount Funded")
type1 = st.selectbox('Type:',['Lollipop Plot', 'BarPlot','DataFrame'], key='ver61')
if type1 == 'BarPlot':
    grouped_bar(selected_vertical,df,'vertical','amount')
elif type1 == "Lollipop Plot":
    lollipop(selected_vertical, df, 'vertical', 'amount')
else: 
    grouped_df(selected_vertical, df, 'vertical', 'amount')


st.subheader("# Fundings")
type2 = st.selectbox('Type:',['Lollipop Plot', 'BarPlot', 'DataFrame'], key='ver62')
if type2 == 'BarPlot':
    grouped_bar(selected_vertical,df,'vertical','count')
elif type2 == "Lollipop Plot":
    lollipop(selected_vertical, df, 'vertical', 'count')
else: 
    grouped_df(selected_vertical, df, 'vertical', 'count')

st.markdown("""---""")
