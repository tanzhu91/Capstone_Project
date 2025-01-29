import streamlit as st
import plotly.express as px
import pandas as pd



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





st.title("Platform and Ratings analysis")
st.markdown("")

tab1, tab2 , tab3, tab4 = st.tabs(["Platform popularity", "Top rated games", "Top publishers and genres" ,"Top 10 prices and playtime"])


df = data[data['year'] != 2024]


#first
platform_counts = df[['windows', 'mac', 'linux']].sum().reset_index(name='count')
platform_counts.columns = ['platform', 'count']


#second
platform_data = df.melt(id_vars=['price', 'recommendations', 'average_playtime_forever'],
                        value_vars=['windows', 'mac', 'linux'],
                        var_name='platform', value_name='is_supported')
platform_data = platform_data[platform_data['is_supported'] == 1]
platform_features = platform_data.groupby('platform')[['price', 'recommendations', 'average_playtime_forever']].sum().reset_index()



#third
df['platform_combination'] = (
    df['windows'].astype(int).map({1: 'Windows', 0: ''}) +
    df['mac'].astype(int).map({1: '+Mac', 0: ''}) +
    df['linux'].astype(int).map({1: '+Linux', 0: ''})
).str.strip('+')


platform_combinations = df['platform_combination'].value_counts().reset_index()
platform_combinations.columns = ['platform_combination', 'count']

#fourth
cross_platform_features = df.groupby('platform_combination')[['positive','recommendations','negative']].sum().reset_index()


features_melted = cross_platform_features.melt(id_vars='platform_combination', 
                                               var_name='Feature', 
                                               value_name='Average')



#fifth
meta = df[df['metacritic_score'] > 92].reset_index()
meta = meta.loc[490, 'name'] = "The Elder Scrolls IV: Oblivion"
meta_agg = meta[['name', 'metacritic_score','required_age','Genre_1']].sort_values(by='metacritic_score', ascending=False).head(10)


user_score = df[df['user_score'] > 92]

user_agg = user_score[['name', 'user_score','metacritic_score','required_age','Genre_1','Genre_2']].sort_values(by='user_score', ascending=False).head(10)



df['publishers'] = df['publishers'].str.strip("[]").str.replace("'", "")
publishers_summary = df.groupby('publishers').agg(
    num_games=('AppID', 'count'),
    total_playtime=('average_playtime_forever_in_hours', 'sum'),
    average_playtime=('average_playtime_forever_in_hours', 'mean'),
    total_revenue=('estimated_revenue', 'sum')
).sort_values(by='total_revenue', ascending=False)


top_publishers = publishers_summary.head(10).reset_index()





fig3 = px.bar(platform_combinations, 
             x='platform_combination', 
             y='count',
             title='Platform Combination and number of games ',
             labels={'platform_combination': 'Platform Combination', 'count': 'Number of Games'},
             color='platform_combination',
             color_discrete_sequence=px.colors.qualitative.Bold)
fig3.update_xaxes(categoryorder='total descending',title={'text': 'Platform Combination', 'font': {'size': 28}},
    tickfont={'size': 26}, 
    showgrid=True, gridcolor='lightgray', gridwidth=1
)
fig3.update_yaxes(title={'text': 'Number of Games', 'font': {'size': 28}}, tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1)
fig3.update_layout(title={
        'text': 'Platform Combination and Number of Games',
        'font': {'size': 30}},
    height=700,
    legend={
        'title': {'text': 'Platform Combination', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
    
)

fig4 = px.bar(features_melted, 
             x='platform_combination', 
             y='Average', 
             color='Feature',
             title='Platform Combination vs Positive/Negative reviews and Recommendations',
             labels={'platform_combination': 'Platform Combination', 'Average': 'Sum','num_reviews_total':'number of reviews'},
             barmode='group',
             color_discrete_sequence=px.colors.qualitative.Bold)
fig4.update_xaxes(categoryorder='total descending',title={'text': 'Platform Combination', 'font': {'size': 28}},
    tickfont={'size': 26},
    showgrid=True, gridcolor='lightgray', gridwidth=1
)
fig4.update_yaxes(title={'text': 'Sum', 'font': {'size': 28}},
    showgrid=True, gridcolor='lightgray', gridwidth=1,tickfont={'size': 26},)
fig4.update_layout(title={
        'text': 'Platform Combination vs Positive/Negative reviews and Recommendations',
        'font': {'size': 30}},
    height=700,
    legend={
        'title': {'text': 'Reviews', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
)








fig7 = px.scatter(meta_agg,
                  y='name',
                  x='metacritic_score',
                  color='Genre_1',
                  text='required_age',
                  hover_name="name",
                  labels={'Genre_1': 'Genre', 
                          'metacritic_score':'Metacritic Score'
                          ,'name':'Name','required_age':'Required Age'},
                          title='Top 10 games rated by critics, their Genre and age restriction',
                          color_discrete_sequence=px.colors.qualitative.Vivid_r)
fig7.update_xaxes(title={'text': 'Rating', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig7.update_yaxes(title={'text': 'Game Name', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1,
                  categoryorder='total ascending')
fig7.update_traces(marker=dict(size=50))
fig7.update_layout(title={
        'text': 'Top 10 games rated by critics, their Genre and age restriction',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Genre', 'font': {'size': 26}},
        'font': {'size': 24}
    }
)


fig9 = px.scatter(user_agg,
                  y='name',
                  x='user_score',
                  color='Genre_1',
                  text='required_age',
                  hover_name="name",
                  labels={'Genre_1': 'Genre', 
                          'user_score':'User Score'
                          ,'name':'Name','required_age':'Required Age'},
                          title='Top 10 games rated by users, their Genre and age restriction',
                          color_discrete_sequence=px.colors.qualitative.Vivid_r)
fig9.update_xaxes(title={'text': 'Rating', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig9.update_yaxes(title={'text': 'Game Name', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1,
                  categoryorder='total ascending')
fig9.update_traces(marker=dict(size=50))
fig9.update_layout(title={
        'text': 'Top 10 games rated by users, their Genre and age restriction',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Genre', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
)





top_10_playtime = df[['name', 'average_playtime_forever_in_hours','price','Genre_1']].sort_values(by='average_playtime_forever_in_hours', ascending=False).head(10)


fig8 = px.bar(top_10_playtime, 
             y='name', 
             x='average_playtime_forever_in_hours', 
             title='Top 10 games with most playtime, their Genre and price',
             color='Genre_1', text='price',
             labels={'name': 'Games', 'average_playtime_forever_in_hours': 'Average Playtime (Hours)','Genre_1': 'Genre'},
             color_discrete_sequence=px.colors.qualitative.Bold
            )

fig8.update_xaxes(title={'text': 'Average Playtime (Hours)', 'font': {'size': 28}},
                  tickfont={'size': 24},
                  categoryorder='total descending',
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig8.update_yaxes(title={'text': 'Game Name', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  categoryorder='total ascending',
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig8.update_layout(title={
        'text': 'Top 10 games with most playtime, their Genre and price',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Genre', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
)




fig11 = px.bar(
    top_publishers, 
    y='publishers', 
    x='total_revenue', 
    title='Top Publishers by playtime and revenue',
    labels={'publishers': 'Publisher',
             'total_revenue': 'Total Revenue',
             'total_playtime':'Average playtime (hours)','num_games':'Number of games'},
    color='total_playtime',color_discrete_sequence=px.colors.qualitative.Bold
)
fig11.update_xaxes(title={'text': 'Total Revenue', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig11.update_yaxes(title={'text': 'Publisher', 'font': {'size': 28}},
                   tickfont={'size': 26},categoryorder='total ascending',
                   showgrid=True, gridcolor='lightgray', gridwidth=1)
fig11.update_layout(title={
        'text': 'Top Publishers by playtime and revenue',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Average playtime (hours)', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
)



price = df[df['price'] > 190].nlargest(10, 'price')
price_grouped = price.groupby(['name','price','year'], as_index=False)['Genre_1'].agg(list)
price_grouped['Genre_1'] = price_grouped['Genre_1'].apply(lambda x: ', '.join(x))



fig10 = px.bar(
    price_grouped, 
    y='name', 
    x='price', 
    color='Genre_1',
    labels={'name': 'Name',
             'price': 'Price','Genre_1': 'Genre','year': 'Year'},
    barmode='stack',
    title='Top 10 priced Games, their primary Genre and release year',
    hover_name="Genre_1",
    text='year',color_discrete_sequence=px.colors.qualitative.Bold
)
fig10.update_xaxes(title={'text': 'Price ($)', 'font': {'size': 28}},
                  tickfont={'size': 26},
                  showgrid=True, gridcolor='lightgray', gridwidth=1)
fig10.update_yaxes(title={'text': 'Game Name', 'font': {'size': 28}},
                   tickfont={'size': 26},categoryorder='total ascending',
                   showgrid=True, gridcolor='lightgray', gridwidth=1)
fig10.update_layout(title={
        'text': 'Top 10 priced Games, their primary Genre and release year',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Genre', 'font': {'size': 26}},
        'font': {'size': 24} 
    }
)






genre_columns = ['Genre_1', 'Genre_2', 'Genre_3', 'Genre_4']
grouped_list = []

for genre_column in genre_columns:
    grouped = data.groupby([genre_column, 'estimated_revenue'], as_index=False)['average_playtime_forever_in_hours'].sum()

    grouped.rename(columns={
        genre_column: 'Genre',
        'estimated_revenue': 'Revenue',
        'average_playtime_forever_in_hours': 'Average Playtime (Forever)'
    }, inplace=True)

    grouped_list.append(grouped)
combined_grouped = pd.concat(grouped_list, ignore_index=True)
final_summary = combined_grouped.groupby('Genre').agg(
    total_revenue=('Revenue', 'sum'),
    avg_playtime=('Average Playtime (Forever)', 'sum')
)
top_10 = final_summary.sort_values(by='avg_playtime', ascending=False).reset_index().head(10)



fig12 = px.bar(
    top_10, 
    y='Genre', 
    x='total_revenue', 
    barmode='stack',
    labels={'Genre': 'Genre',
             'total_revenue': 'Revenue','avg_playtime': 'Total playtime sum'},
    title='Top Genres by revenue and playtime',color= 'avg_playtime',color_discrete_sequence=px.colors.qualitative.Bold
)
fig12.update_xaxes(title={'text': 'Revenue', 'font': {'size': 28}},
                  tickfont={'size': 26},showgrid=True, gridcolor='lightgray', gridwidth=1)
fig12.update_yaxes(title={'text': 'Genre', 'font': {'size': 28}},
                  tickfont={'size': 26},categoryorder='total ascending',
                   showgrid=True, gridcolor='lightgray', gridwidth=1)
fig12.update_layout(title={
        'text': 'Top Genres by revenue and playtime',
        'font': {'size': 30}},
    height=700, legend={
        'title': {'text': 'Total playtime sum', 'font': {'size': 26}},
        'font': {'size': 24}}
)


with tab1:
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
                    
with tab2:
    st.plotly_chart(fig7)
    st.plotly_chart(fig9)


with tab3:
    st.plotly_chart(fig11)
    st.plotly_chart(fig12)

with tab4:
    st.plotly_chart(fig10)
    st.plotly_chart(fig8)
