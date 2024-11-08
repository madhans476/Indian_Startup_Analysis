import streamlit as st
import pandas as pd
import geopandas as gpd 

st.set_page_config(layout='wide',page_title="Cities")

df = pd.read_csv("startup_funding.csv")
st.title("Analysis Based On Location")

st.markdown("""---""")
color1 = 'Orange'
color2 = 'Blue'

# df1 = df['state'].value_counts().reset_index()
# df1 = df1.drop(index=3)
# india_shape = gpd.read_file('india_st.shp')

# india_shape['States'] = india_shape['STATE'].astype(str)  # Update accordingly

# df1['state'] = df1['state'].str.lower().str.strip()
# india_shape['States'] = india_shape['States'].str.lower().str.strip()

# # Merge the dataframes
# merged = india_shape.set_index('States').join(df1.set_index('state'))

# # # Check the merged data
# # print(merged[['Count']])  # Should show counts now

# fig, ax = plt.subplots(1, 1, figsize=(12, 10))  # Adjust size as needed
# merged.plot(
#     column='count', 
#     cmap='coolwarm',  # Use a more contrasting color map
#     linewidth=0.8, 
#     ax=ax, 
#     edgecolor='0.8',
#     legend=True, 
#     missing_kwds={'color': 'lightgrey', 'label': 'No Data'}
# )

# # Set title and remove axis
# ax.set_title('State-wise Heatmap (Count)', fontsize=16)
# ax.set_axis_off()

# # Display the plot in Streamlit
# st.pyplot(fig)

#! function imports
from functions import Barplot
from functions import DataFrame


st.subheader('Statewise Startup Count')
state_names = sorted(list(df['state'].unique()))
ct = len(state_names)

n = st.slider("Select n:",2,ct,5, key='loc7')
data = df['state'].value_counts().reset_index().sort_values(by=['count', 'state'], ascending=[False, True])
# data = data.drop(index=3)

data = data[:n]
data = data.reset_index(drop=True)
data.index = data.index + 1
type1 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc1')
if type1=='BarPlot':
    Barplot(n,data, 'count', 'state',1)
else:
    DataFrame(n,data)

st.markdown("""---""")

#! -------------------------------------------------------------------------------------------------------------------
st.subheader('Statewise Amount Funded')

n = st.slider("Select n:",2,ct,5, key='loc8')
data = df.groupby('state')['amount'].sum().sort_values(ascending=False).reset_index()
# data = data.drop(index=3)

data = data[:n]
data = data.reset_index(drop=True)
data.index = data.index + 1
type1 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc6')
if type1=='BarPlot':
    Barplot(n,data, 'amount', 'state',1)
else:
    DataFrame(n,data, True)

st.markdown("""---""")
#! -------------------------------------------------------------------------------------------------------------------


st.header('Statewise Analysis')

state = st.selectbox('Select the State:', state_names, index = 8)
# state = 'Tamil Nadu'
sample = df[df['state']==state]
ct = sample['startup'].count()
#! -------------------------------------------------------------------------------------------------------------------

st.subheader(f"# Startups from :orange-background[{state}] : {ct}",)

#! function imports
from functions import bar_line_and_df

st.subheader('Year Wise Analysis:')
col1, col2 = st.columns(2)

with col1:
    year_wise = 'Amount Funded'
    st.subheader("Amount Funded Year Wise")
    subtype = st.selectbox("Subtype",['Barplot','Lineplot','Treemap','DataFrame'], key='loc2')
    data = sample.groupby(by='year')['amount'].sum()
    bar_line_and_df(data, subtype, year_wise)


with col2:
    year_wise = '# Fundings'
    st.subheader("Number of Fundings Year Wise")
    subtype = st.selectbox("SubType",['Barplot','Lineplot','Treemap','DataFrame'], key='loc3')
    data = sample['year'].value_counts()
    bar_line_and_df(data, subtype, year_wise)

#! -------------------------------------------------------------------------------------------------------------------


st.subheader('Vertical Wise Analysis:')
total = sample['vertical'].nunique()
initial = 5
if initial > total:
    initial = total

check = False
if total>7:
    check = True
    total = min(15, total)

if total>5:
    n2 = st.slider("Select :",2,total,initial)
else: 
    n2 = total


col_1, col_2 = st.columns(2)
with col_1:
    st.subheader("Amount Funded")
    # type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc4')
    data = sample.groupby('vertical')['amount'].sum().reset_index().sort_values(by=['amount', 'vertical'], ascending=[False, True])
    data = data[:n2]
    data = data.reset_index(drop=True)
    data.index = data.index + 1
    default = 'BarPlot' if data['amount'][n2] < data['amount'][1] else 'DataFrame'
    type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc4',index=['BarPlot','DataFrame'].index(default))
    if type2 == 'BarPlot' :
        Barplot(n2,data,'amount', 'vertical', 1.5)
    else: 
        DataFrame(n2,data, True)
    

with col_2:
    st.subheader("# Fundings")
    data = sample.groupby('vertical')['Sr No'].count().reset_index().sort_values(by=['Sr No', 'vertical'], ascending=[False, True])
    data.columns = ['vertical', 'count']
    data = data[:n2]
    data = data.reset_index(drop=True)
    data.index = data.index + 1
    default_option = 'BarPlot' if data['count'][n2] < data['count'][1] else 'DataFrame'
    type3 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc5',index=['BarPlot','DataFrame'].index(default_option))
    if type3 == 'BarPlot' :
        Barplot(n2,data,'count', 'vertical', 1.5)
    else: 
        DataFrame(n2, data)

#! -------------------------------------------------------------------------------------------------------------------
if(check):
    c_1, c_2 = st.columns(2)
    with c_1:
        st.subheader("Amount Funded")
        # type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc42',)
        data = sample.groupby('vertical')['amount'].sum().reset_index().sort_values(by=['amount', 'vertical'], ascending=[True, True])
        data = data[:n2]
        data = data.reset_index(drop=True)
        data.index = data.index + 1
        default = 'BarPlot' if data['amount'][n2] > data['amount'][1] else 'DataFrame'
        type2 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc42',index=['BarPlot','DataFrame'].index(default))
        if type2 == 'BarPlot' :
            Barplot(n2,data,'amount', 'vertical', 1.5, least=True)
        else: 
            DataFrame(n2,data, True)
        

    with c_2:
        st.subheader("# Fundings")
        data = sample.groupby('vertical')['Sr No'].count().reset_index().sort_values(by=['Sr No', 'vertical'], ascending=[True, True])
        data.columns = ['vertical', 'count']
        data = data[:n2]
        data = data.reset_index(drop=True)
        data.index = data.index + 1
        default_option = 'BarPlot' if data['count'][n2] > data['count'][1] else 'DataFrame'
        type3 = st.selectbox('Type:',['BarPlot', 'DataFrame'], key='loc52',index=['BarPlot','DataFrame'].index(default_option))
        if type3 == 'BarPlot' :
            Barplot(n2,data,'count', 'vertical', 1.5,least=True)
        else: 
            DataFrame(n2, data)


# st.subheader(f"Hubs in {state}:")
# data2 = pd.read_csv('cities.csv')
# data2 = data2[data2['state']==state]
# # data2 = data2.iloc[:,2:4]
# # s_df = df['city'].value_counts().reset_index()
# # size = list(s_df['count'])
# data2['count'] = data2['count']*20

# st.map(data2,  color = '#F09102', size='count')

st.markdown("""---""")
st.header('Compare States')
selected_states = st.multiselect('Select the states:', state_names, default=[state_names[i] for i in [8, 11]])
from functions import grouped_bar, lollipop, grouped_df

st.subheader("Amount Funded")
type1 = st.selectbox('Type:',['Lollipop Plot', 'BarPlot', 'DataFrame'], key='loc61')
if type1 == 'BarPlot':
    grouped_bar(selected_states,df,'state','amount')
elif type1 == "Lollipop Plot":
    lollipop(selected_states, df, 'state', 'amount')
else: 
    grouped_df(selected_states,df,'state','amount')


st.subheader("# Fundings")
type2 = st.selectbox('Type:',['Lollipop Plot', 'BarPlot', 'DataFrame'], key='loc62')
if type2 == 'BarPlot':
    grouped_bar(selected_states,df,'state','count')
elif type2 == "Lollipop Plot":
    lollipop(selected_states, df, 'state', 'count')
else: 
    grouped_df(selected_states,df,'state','count')


