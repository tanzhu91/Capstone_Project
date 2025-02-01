import streamlit as st
import pandas as pd
import plotly.express as px




base_url = "https://raw.githubusercontent.com/tanzhu91/Capstone_Project/main/data/"


file_names = [f"chunk_{i}.csv" for i in range(17)]


dataframes = []


for file_name in file_names:
    url = base_url + file_name
    try:
        df = pd.read_csv(url)
        dataframes.append(df)
    except Exception as e:
        print(f"Error loading {file_name}: {e}")


data = pd.concat(dataframes, ignore_index=True)





st.title("Number of games and Revenue analysis")

#tabs
tab1, tab2 = st.tabs(["Yearly Games Released and estimated revenue", "Revenue trendline and monthly releases"])


#Data Frames selection
df = data[(data['year'] != 2024) & (data['year'] >= 2003)]

df_agg = df.groupby(['year']).agg({'estimated_revenue': 'sum'}).reset_index()
filtered_df =df_agg[(df_agg['year'] >= 2009) & (df_agg['year'] <= 2023)]

count_sorted_df=df["month_year"].value_counts().reset_index().sort_values(by='count',ascending=False)
count_sorted_df[["Month","Year"]]=count_sorted_df["month_year"].str.split("-",expand=True)
split_data_df=count_sorted_df[["Month","Year","count"]]
split_data_df.set_index("Month")

yearly_sum=split_data_df.groupby(["Year"])["count"].sum()
monthly_sum=split_data_df.groupby(["Month"])["count"].sum()

monthly_sum_df=monthly_sum.reset_index().rename(columns={"index": "value", 0: "count"})
yearly_sum_df=yearly_sum.reset_index().rename(columns={"index": "value", 0: "count"})

customOrder=["January","February","March","April","May","June","July","August","September","October","November","December"]
monthly_sum_df["Month"]=pd.Categorical(monthly_sum_df["Month"],categories=customOrder,ordered=True)

monthly_sum_df=monthly_sum_df.sort_values(by="Month")
year_sum_df=yearly_sum_df.sort_values(by="Year")








#First graph
fig1 = px.line(year_sum_df, x='Year', y='count',  title='Number of games released between 2003-2023',
               color_discrete_sequence=px.colors.qualitative.Bold,
               labels={'count':'Number of games'})
fig1.update_layout(
    title={'x': 0.5, 'xanchor': 'center', 'text': 'Number of Games Released Between 2003-2023', 
        'font': {'size': 30}},
    showlegend=False,height=700)
fig1.update_xaxes(
    title={'text': 'Year', 'font': {'size': 28}},
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    tickfont={'size': 26},)
fig1.update_yaxes(
    title={'text': 'Number of games released (K for Thousands)' , 'font': {'size': 28}},
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    tickfont={'size': 26})



fig2 = px.line(df_agg, x='year', y='estimated_revenue', title='Estimated revenue between 2003-2023',
               color_discrete_sequence=px.colors.qualitative.Bold,
               labels={'estimated_revenue':'Estimated revenue'})
fig2.update_layout(
    title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 30}},
    showlegend=False,height=700
)
fig2.update_xaxes(
    title={'text': 'Year', 'font': {'size': 28}},
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    tickfont={'size': 26}
)
fig2.update_yaxes(
    title={'text':'Estimated Revenue (B for Billions)','font': {'size': 28}},
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    tickfont={'size': 26}
)



fig3 = px.scatter(filtered_df, x='year', y='estimated_revenue',
                 title='Estimated Revenue between 2009-2023 with trendline',
                 trendline="ols",
                 color_discrete_sequence=px.colors.qualitative.Bold,
                 labels={'estimated_revenue':'Estimated revenue'})
fig3.update_layout(
    xaxis_title='Year',
    yaxis_title='Estimated Revenue (B for Billions)',
    title={'x': 0.5, 'xanchor': 'center','font': {'size': 30}},
    showlegend=False,height=700
)
fig3.update_xaxes(title={'font': {'size': 28}},
    tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1
)
fig3.update_yaxes(title={'font': {'size': 28}},tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1)



fig4 = px.line(monthly_sum_df, x='Month', y='count', title='Number of games released each month between 2003-2023',
               color_discrete_sequence=px.colors.qualitative.Bold,
               labels={'count':'Number of games'})
fig4.update_layout(
    title={'x': 0.5, 'xanchor': 'center','font': {'size': 30}},
    showlegend=False,height=700
)
fig4.update_xaxes(title={'font': {'size': 28}},tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1
)
fig4.update_yaxes(
    title={'text':'Number of games released (Thousands)','font': {'size': 28}}, tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1)







with tab1:
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

with tab2:
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)




