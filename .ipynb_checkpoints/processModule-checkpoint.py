import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def processing(df, region_df):

    #merge with region_df
    df = df.merge(region_df, on = "NOC", how = "left")
    #droping duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding 
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)
    return df

def process_summer_winter(df, region_df):
    
    #Filter Summer and Winter Olymppics
    df_summer = df[df['Season'] == "Summer"]
    df_winter = df[df['Season'] == "Winter"]
    
    #Merging with region_df
    df_summer = df_summer.merge(region_df, on = "NOC", how = "left")
    df_winter = df_winter.merge(region_df, on = "NOC", how = "left")
    
    #Drop duplicates
    df_summer.drop_duplicates(inplace=True)
    df_winter.drop_duplicates(inplace=True)
    
    
    #one hot encoding 
    df_summer = pd.concat([df_summer, pd.get_dummies(df_summer["Medal"])], axis=1)
    df_winter = pd.concat([df_winter, pd.get_dummies(df_winter["Medal"])], axis=1)
    

    
    return df_summer,df_winter


def get_medal_count(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'All Countries' and country == 'All Countries':
        temp_df = medal_df
    if year == 'All Countries' and country != 'All Countries':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'All Countries' and country == 'All Countries':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'All Countries' and country != 'All Countries':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def get_country_year(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'All Years')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'All Countries')

    return years, country




def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def medal_count_yearWise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return  final_df


def get_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x



def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


def draw_map(dataset, title, colorscale, reversescale=False):
    trace = go.Choropleth(
                locations = dataset['Country'],
                locationmode='country names',
                z = dataset['Editions'],
                text = dataset['Country'],
                autocolorscale =False,
                reversescale = reversescale,
                colorscale = colorscale,
                marker = dict(
                    line = dict(
                        color = 'rgb(0,0,0)',
                        width = 0.5)
                ),
                colorbar = dict(
                    title = 'Editions',
                    tickprefix = '')
            )

    data = [trace]
    layout = go.Layout(
        title = title,
        geo = dict(
            showframe = True,
            showlakes = False,
            showcoastlines = True,
            projection = dict(
                type = 'orthographic'
            )
        )
    )
    fig = dict( data=data, layout=layout )
    
    return fig