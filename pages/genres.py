import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests

url = "https://drive.google.com/uc?id=15chzeZyWPzFOmVsTZzUlVqXU91deZhog&export=download"


response = requests.get(url)
if response.status_code == 200:
    with open("games_prepped.csv", "wb") as f:
        f.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")



st.title("Genres, Categories and playtime analysis")


tab1, tab2  = st.tabs(["Playtime across Genres and Categories", "Top 10 Genres with most playtime and number of games"])

df = pd.read_csv('games_prepped.csv', low_memory=False)
data = df[df['year'] != 2024]


#grouping some data
genre1_playtime = data.groupby('Genre_1')['average_playtime_forever_in_hours'].sum().sort_values(ascending=False)
genre2_playtime = data.groupby('Genre_2')['average_playtime_forever_in_hours'].sum().sort_values(ascending=False)
genre3_playtime = data.groupby('Genre_3')['average_playtime_forever_in_hours'].sum().sort_values(ascending=False)
genre4_playtime = data.groupby('Genre_4')['average_playtime_forever_in_hours'].sum().sort_values(ascending=False)


combined_data = {
    'Genre': list(genre1_playtime.keys()) + list(genre2_playtime.keys()) +
             list(genre3_playtime.keys()) + list(genre4_playtime.keys()),
    'Playtime': list(genre1_playtime.values) + list(genre2_playtime.values) +
                list(genre3_playtime.values) + list(genre4_playtime.values)
}

df_combined = pd.DataFrame(combined_data)
major_genres = ["Action", "Indie", "RPG", "Adventure", "Simulation", "Casual", "Strategy"]
df_combined['Genre'] = df_combined['Genre'].apply(lambda x: x if x in major_genres else 'Others')
df_final = df_combined.groupby('Genre', as_index=False).agg({'Playtime': 'sum'})




#grouping some more data
genre_columns = ['Genre_1', 'Genre_2', 'Genre_3', 'Genre_4']


grouped_list = []


for genre_column in genre_columns:
    grouped = data.groupby([genre_column, 'required_age','AppID','average_playtime_forever_in_hours','positive','negative','pct_pos_total','num_reviews_total'], as_index=False)['average_playtime_forever_in_hours'].sum()

    grouped.rename(columns={
        genre_column: 'Genre',
        'required_age': 'Age Restriction',
        'average_playtime_forever_in_hours': 'Average Playtime (Forever)'
    }, inplace=True)

    grouped_list.append(grouped)


combined_grouped = pd.concat(grouped_list, ignore_index=True)


final_grouped = combined_grouped.groupby(['Genre', 'Age Restriction'], as_index=False)['Average Playtime (Forever)'].sum()

total_playtime_by_genre = final_grouped.groupby('Genre', as_index=False)['Average Playtime (Forever)'].sum()

top_10_genres = total_playtime_by_genre.sort_values(by='Average Playtime (Forever)', ascending=False).head(10)

final_grouped_top_10 = final_grouped[final_grouped['Genre'].isin(top_10_genres['Genre'])]




genre_summary = combined_grouped.groupby('Genre').agg(
    num_games=('AppID', 'count'),
    avg_playtime=('Average Playtime (Forever)', 'sum'),
    avg_positive_reviews=('positive', 'mean'),
    avg_negative_reviews=('negative', 'mean'),
    avg_reviews=('num_reviews_total', 'sum'),
    percentage_positive_reviews=('pct_pos_total', 'mean'),
).sort_values(by='num_games', ascending=False)


top_genres = genre_summary.head(10)




df['categories'] = df['categories'].str.strip("[]").str.replace("'", "")
df['categories_split'] = df['categories'].str.split(', ')
df['categories_top5'] = df['categories_split'].apply(lambda x: ', '.join(x[:5]) if isinstance(x, list) else None)

categories_exploded = df[['AppID', 'categories', 'average_playtime_forever_in_hours', 'price', 'num_reviews_total']].copy()
categories_exploded['categories'] = categories_exploded['categories'].str.split(', ')
categories_exploded = categories_exploded.explode('categories')


category_analysis = categories_exploded.groupby('categories').agg(
    num_games=('AppID', 'count'),
    total_playtime=('average_playtime_forever_in_hours', 'sum'),
    average_playtime=('average_playtime_forever_in_hours', 'mean'),
    total_reviews=('num_reviews_total', 'sum'),
    average_price=('price', 'mean')
).sort_values(by='num_games', ascending=False)
category_analysis.reset_index()
top_categories = category_analysis.reset_index().head(10)



#first plot
fig1 = px.pie(
    df_final, 
    names='Genre', 
    values='Playtime', 
    title="Average Playtime Distribution Across Genres (Others combination of smaller genres)",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig1.update_traces(textposition='inside', textinfo='percent+label',textfont={'size': 22})
fig1.update_xaxes(
    showgrid=True, gridcolor='lightgray', gridwidth=1
)
fig1.update_yaxes(
    showgrid=True, gridcolor='lightgray', gridwidth=1)
fig1.update_layout(
    height=700,
    title={
        'text': 'Average Playtime Distribution Across Genres (Others combination of smaller genres)',
        'font': {'size': 30}},
    legend= {
        'title': {'text': 'Total Playtime', 'font': {'size': 32}},
        'font': {'size': 28}}
    
)

#second graph
fig2 = px.bar(
    final_grouped_top_10, 
    y='Genre', 
    x='Average Playtime (Forever)', 
    color='Age Restriction', 
    barmode='stack',  
    title='Top Genres by average playtime and age restriction',
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig2.update_layout(
    xaxis_title='Average Playtime Hours Sum', 
    yaxis_title='Genre',
    legend_title='Age Restriction',
    height=700,
        title={
        'text': 'Top Genres by average playtime and age restriction',
        'font': {'size': 30}},
    legend= {'title': {'text': 'Total Playtime', 'font': {'size': 32}},
    'font': {'size': 30}}
)
fig2.update_xaxes(categoryorder='total descending',
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    title={'text': 'Average Playtime Hours Sum', 'font': {'size': 28}},
                  tickfont={'size': 26} 
)
fig2.update_yaxes(categoryorder='total ascending',
    showgrid=True, gridcolor='lightgray', gridwidth=1,
        title={'text': 'Genre', 'font': {'size': 28}},
                  tickfont={'size': 26} )




#fourth figure
fig4 = px.bar(
    top_categories,
    y='categories',
    x='num_games',
    title='Top 10 Categories by Number of Games',color='total_playtime',
    labels={'categories': 'Category', 'num_games': 'Total number of Games', 'total_playtime':' Total playtime'},
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig4.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=1, 
                  title={'text': 'Total Number of Games', 'font': {'size': 28}},
                  tickfont={'size': 26} 
)
fig4.update_yaxes(categoryorder='total ascending',
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    title={'text': 'Category', 'font': {'size': 28}}, 
    tickfont={'size': 26})
fig4.update_layout(height=700,
        title={
        'text': 'Top 10 Categories by Number of Games',
        'font': {'size': 30}},
        legend= {
        'title': {'text': 'Total Playtime', 'font': {'size': 32}},
        'font': {'size': 30}}
)



#fifth figure
fig5 = px.scatter(
    top_genres.reset_index(),
    y='Genre',
    x='num_games',
    title='Top Genres by number of Games and percentage positive reviews',
    labels={'genres': 'Genre', 'num_games': 'Number of Games','percentage_positive_reviews':'% Positive reviews'},
    color='percentage_positive_reviews',color_discrete_sequence=px.colors.qualitative.Bold
)
fig5.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=1,
                  title={'text': 'Total Number of Games', 'font': {'size': 28}},
                  tickfont={'size': 26} 
)
fig5.update_yaxes(categoryorder='total ascending',
    showgrid=True, gridcolor='lightgray', gridwidth=1,
    title={'text': 'Genre', 'font': {'size': 28}}, 
    tickfont={'size': 26})
fig5.update_layout(legend_title_text='Average review value',height=700,
                title={
        'text': 'Top Genres by number of Games and percentage positive reviews',
        'font': {'size': 30}},
        legend= {'title': {'text': 'Total Playtime', 'font': {'size': 32}},
        'font': {'size': 30}})
fig5.update_traces(marker=dict(size=30))





with tab1:
    st.plotly_chart(fig1)
    st.plotly_chart(fig4)
with tab2:
    st.plotly_chart(fig2)
    st.plotly_chart(fig5)

