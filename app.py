import streamlit as st
import pandas as pd
import processModule
from PIL import Image
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt
import plotly.graph_objs as go
from plotly.offline import plot


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
image = Image.open("olympic_rings.png")
image_f = Image.open("home_page_footer.png")
#Processing Data
df_main = processModule.processing(df, region_df)
df_summer,df_winter = processModule.process_summer_winter(df, region_df)


 #---------------------------------------------------------------------------------------------------------------------------------------------     

#Side Menu
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Home','Medal Dashboard', 'Country-wise Analysis', 'Athlete wise Analysis', 'Overall Analysis')
)

 #---------------------------------------------------------------------------------------------------------------------------------------------     
    
if user_menu == 'Medal Dashboard':
    st.sidebar.header("Medal Overview")
    
    #Get list of years and country for options
    years, country = processModule.country_year_list(df_main)

    selected_country = st.sidebar.selectbox("Select Country", country)
    
    
    #Get the filtered df
    selected_years='All Countries'
    # medal_tally_df = processModule.fetch_medal_count(df, selected_years, selected_country)
    medal_tally_df_summer = processModule.fetch_medal_count(df_summer, selected_years, selected_country)
    medal_tally_df_winter = processModule.fetch_medal_count(df_winter, selected_years, selected_country)
    
    if selected_years == 'All Countries' and selected_country == 'All Countries':
        st.title("All Countries Tally")
    if selected_years != 'All Countries' and selected_country == "All Countries":
        st.title("Medal tally in " + str(selected_years) + " Olympics")
    if selected_years == 'All Countries' and selected_country != "All Countries":
        st.title("Medal tally of " + str(selected_country))
    if selected_years != 'All Countries' and selected_country != "All Countries":
        st.title("Medal tally of " + str(selected_country) + " in " + str(selected_years) + " Olympics")
        
        
    olympics_df = df.merge(region_df)
    olympics_df=olympics_df.rename(columns = {'region':'Country'})

    tmp = olympics_df.groupby(['Country', 'Season'])['Year'].nunique()
    df = pd.DataFrame(data={'Editions': tmp.values}, index=tmp.index).reset_index()
    
    dfS = df[df['Season']=='Summer']
    dfW = df[df['Season']=='Winter']
    fig_s=processModule.draw_map(dfS, 'Olympic countries (Summer games)', "Reds")
    fig_w =processModule.draw_map(dfW, 'Olympic countries (Winter games)', "Blues")
    
    st.plotly_chart(fig_s)
    st.plotly_chart(fig_w)

    
    col1,col2=st.columns(2)
    
    
    with col1:
        st.title("Summer")
        
        if len(medal_tally_df_summer) and selected_years == 'All Countries' and selected_country != 'All Countries'  :
            fig, ax = plt.subplots()
            medal_tally_df_summer.plot.barh(x='Year', ax=ax)
            st.pyplot(fig)
        if len(medal_tally_df_summer)==0:
            st.write("No Games Played")
        else:
            st.table(medal_tally_df_summer)
        
        
    with col2:
        st.title("Winter")

            
        if len(medal_tally_df_winter) and selected_years == 'All Countries' and selected_country != 'All Countries':
        
            fig, ax = plt.subplots()
            medal_tally_df_winter.plot.barh(x='Year', ax=ax)
            st.pyplot(fig)
        if len(medal_tally_df_winter)==0:
            st.write("No Games Played") 
        else:
            st.table(medal_tally_df_winter)


 #---------------------------------------------------------------------------------------------------------------------------------------------     


elif user_menu == 'Overall Analysis':
    
    #Get list of years and country for options
    years, country = processModule.country_year_list(df_main)
    html_string = "<h1>Overall Analysis</h1> <p>A flexible analysis page containing different factors to tune with such as seasons, sports, countries and years.</p>"

    st.markdown(html_string, unsafe_allow_html=True)

    seasons = ['All Seasons','Summer', 'Winter']

    selected_country = st.sidebar.selectbox("Select Country", country)
    selected_season = st.sidebar.selectbox("Select Season", seasons)
    all_Season = False
    if(selected_season == "All Seasons"):
        temp_df = df_main
        all_Season=True
    elif(selected_season == "Summer"):
        temp_df = df_summer
    else:
        temp_df = df_winter


    editions = temp_df['Year'].unique().shape[0] - 1
    cities = temp_df['City'].unique().shape[0]
    sports = temp_df['Sport'].unique().shape[0]
    events = temp_df['Event'].unique().shape[0]
    athletes = temp_df['Name'].unique().shape[0]
    nations = temp_df['region'].unique().shape[0]

    st.title("Top Statistics for {}".format(selected_season))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    
    
        
    
        
    
    
    nations_vs_time = processModule.data_over_time(temp_df, 'region')
    fig = px.line(nations_vs_time, x="Edition", y="region", labels={"Edition":"Year", "region":"Number of Countries"})
    
    st.title("Participating Nations over the Years in {}".format(selected_season))
    st.markdown("Here is a line graph depicting number of countries participates in the olympics over the years.")
    if all_Season:
        nations_vs_time_summer = processModule.data_over_time(df_summer, 'region')
        fig1 = px.line(nations_vs_time_summer, x="Edition", y="region", labels={"Edition":"Year", "region":"Number of Countries"})
        fig1.update_traces(line_color='rgb(255, 0, 0)')
        
        nations_vs_time_winter = processModule.data_over_time(df_winter, 'region')
        fig2 = px.line(nations_vs_time_winter, x="Edition", y="region", labels={"Edition":"Year", "region":"Number of Countries"})
        
        fig3 = go.Figure(data=fig1.data + fig2.data)
        st.plotly_chart(fig3)
        
    else:
        st.plotly_chart(fig)

           
            
            
        
    
    if selected_country == "All Countries":
        events_vs_time = processModule.data_over_time(temp_df, 'Event')
    else:
        events_vs_time = processModule.data_over_time(temp_df[temp_df['region'] == selected_country], 'Event')  


    st.title("Events over the Year for {}".format(selected_country))
    st.markdown("Here is a line graph depicting number of events that took place in every olympic game over the years.")
    try:
        fig = px.line(events_vs_time, x="Edition", y="Event", labels={"Edition":"Year", "Event":"Number of Events"})
        st.plotly_chart(fig)
    except ValueError:
        st.write("No Data found")

    if(selected_country == "All Countries"):
        athlete_vs_time = processModule.data_over_time(temp_df, 'Name')
    else:
        athlete_vs_time = processModule.data_over_time(temp_df[temp_df['region'] == selected_country], 'Name')
    st.title("Athletes over the Year for {}".format(selected_country))
    st.markdown("Here is a line graph depicting number of athletes participated in every olympic game over the years.")
    try:
        fig = px.line(athlete_vs_time, x="Edition", y="Name", labels={"Edition":"Year", "Name":"Number of Athletes"})
        st.plotly_chart(fig)
    except ValueError:
        st.write("No Data found")


    st.title("No of Events over Time (Every Sport) for {}".format(selected_country))
    st.markdown("Here is a HeatMap depicting number of events segregated by type of sport, that took place in every olympic game over the years.")
    fig, ax = plt.subplots(figsize = (20, 20))
    if(selected_country == "All Countries"):
        x = temp_df.drop_duplicates(['Year', 'Sport', 'Event'])
    else:
        x = temp_df[temp_df['region'] == selected_country].drop_duplicates(['Year', 'Sport', 'Event'])
    try:
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)
    except ValueError:
        st.write("No Data found")
    
      

    st.title("Most successful Athletes from {}".format(selected_country))
    st.markdown("Here is a table for displaying the top athletes with most number of medals, with an option to filter by sport from the checkbox below.")
    sport_list = temp_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    if selected_country == "All Countries":
        x = processModule.most_successful(temp_df, selected_sport)
    else:
        x = processModule.most_successful(temp_df[temp_df['region'] == selected_country], selected_sport)
    try:
        st.table(x)
    except ValueError:
        st.write("No Data found")

 #---------------------------------------------------------------------------------------------------------------------------------------------       

if user_menu == 'Country-wise Analysis':

    #Get list of years and country for options
    years, country = processModule.country_year_list(df_main)

    seasons = ['All Seasons', 'Summer', 'Winter']
    # selected_years = st.sidebar.selectbox("Select Years", years)
    # selected_country = st.selectbox("Select Country", country)
    selected_season = st.sidebar.selectbox("Select Season", seasons)

    if (selected_season == "All Seasons"):
        temp_df = df_main
    elif (selected_season == "Summer"):
        temp_df = df_summer
    else:
        temp_df = df_winter


    country_list = temp_df['region'].dropna().unique().tolist()
    country_list.sort()
    # country_list.insert(0, 'All Countries')
    # selected_country = st.sidebar.selectbox('Select Country', country_list)

    selected_country = st.sidebar.selectbox('Select Country', country_list)
    st.sidebar.title('Country wise Analysis for {} '.format(selected_season))

    country_df = processModule.yearwise_mdeal_tally(temp_df, selected_country)
 
    st.title(selected_country + " Medal Tally over the Year")
    
    if len(country_df) ==0:
        st.markdown("<br><p style='text-align: center;'>This country has not won any medals during the time span</p>", unsafe_allow_html=True)
    else: 
        fig = px.line(country_df, x="Year", y="Medal")
        
        st.plotly_chart(fig)

        st.title(selected_country + " excels in the following sports")
        pt = processModule.country_event_heatmap(temp_df, selected_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        try:
            ax = sns.heatmap(pt, annot=True)
            st.pyplot(fig)
        except:
            st.title('Please select a country to have a look at visualization')


        st.title("Top 10 athletes of " + selected_country)
        top10_df = processModule.most_successful_countrywise(temp_df, selected_country)
        st.table(top10_df)

    
    
 #---------------------------------------------------------------------------------------------------------------------------------------------   



elif user_menu == 'Home':
    st.image(image, use_column_width=True)

    st.markdown("<br><p style='text-align: center;'>Team 3 is presenting the final project on <b>OLYMPICS - SUMMER AND WINTER </b>Games for ITCS 4122/5122 - Rahul Govindkumar, Radha Krishna Balaji Ponnuru, Revanth Seethamraju, Govinda Satyanarayana Bandaru </p>", unsafe_allow_html=True)

    #About Info
    st.markdown("<b><p style='text-align: center; font-size:150%;'> About<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>The Olympics is a major event that hosts the apex athletes from countries around the globe. We want to explore on various factors that affect the winning of medals like the host countries, athletes age, gender distribution across the whole Olympics, etc. </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>We plan to visualize the insight that arises from these questions of interest, taking on the challenges of data processing and deciding appropriate visualizing methods for better understanding. </p>", unsafe_allow_html=True)

    #About the data
    st.markdown("<b><p style='text-align: center;font-size:150%;'> About the data <p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>For our visualization project, we chose to use the Kaggle dataset, <a href='https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results'>120 years of Olympic history: athletes and results</a> . This is a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016. </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Note: Until 1992, the Winter and Summer Games were held in the same year. After that, they staggered them such that the Winter Games occur on a four-year cycle starting with 1994, then Summer in 1996, then Winter in 1998, and so on.  </p>", unsafe_allow_html=True)

    with st.expander("Dataset Attributes"):
        st.write(


            'The file athlete_events.csv contains 271116 rows and 15 columns. Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). The columns are:'
        )
        data_col1, data_col2, data_col3 = st.columns(3)
        with data_col1:
            """
                Key Categorical Attributes
                * Name - Athlete's name 
                * Gender
                * City - Host Location
                * Team/NOC - Country represented by the respective Athletes
                * Sport
                * Medals
                
            """

        with data_col2:
            """
                Key Quanitative Attributes
                * age
                * height_m/ft
                * weight
       
            """
    with st.expander("Data Cleaning"):

        st.write('Data preprocessing involved converting categorical data, such as Medals columns with Gold, Silver, and Bronze values, to numeric values to use in the code. In order to prepare data for an algorithm and get better predictions, we used One-Hot encoding method where categorical features are mapped with a binary variable containing either 0 or 1. We compiled the dataset based on summer and winter games, then cleaned duplicates, based on games played from 1896 to 2016.   ')

    with st.expander("Target Demographic"):
        st.write("Our visualization provides useful data regarding the trends that Olympic games. Those in the Sport Industry would find the information most useful. A tool such as this could be used by sports athletes and coaches to investigate different factors such as the host country, season, athlete's age, and gender distribution across the whole Games. They can use this to strategize their games to help the country win more medals and promote the game.")


    #Findings
    st.markdown("<b><p style='text-align: center;;font-size:150%;'> Findings<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>More contries participates the Summer Olympics than the Winter Olympics simply because the Summer Olympic Games predate the Winter Olympics. </br>Geographically, Winter Olympics are also more restricted to the Northern Hemisphere, since it must be cold enough for snow and ice to form in February.<br/> The male-to-female ratios are almost the same in both the summer and winter Olympics. Also, the gender distribution shows that there are more males as compared to females in both summer and Winter Olympics </p>", unsafe_allow_html=True)
    st.image(image_f, use_column_width=True)


#---------------------------------------------------------------------------------------------------------------------------------------------


elif user_menu == 'Athlete wise Analysis':

    #Get list of years and country for options
    years, country = processModule.country_year_list(df_main)


#     selected_years = st.selectbox("Select Years", years)
#     selected_country = st.selectbox("Select Country", country)


    athlete_df_summer = df_summer.drop_duplicates(subset=['Name', 'Team'])
    athlete_df_winter = df_winter.drop_duplicates(subset=['Name', 'Team'])

    # x1 = athlete_df['Age'].dropna()
    # x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    # x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    # x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    # st.title("Distribution of Age")
    # st.plotly_chart(fig)

    x_summer = []
    x_winter = []
    name_summer = []
    name_winter = []
    famous_sports_summer = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    famous_sports_winter= ['Alpine Skiing',
 'Alpinism',
 'Biathlon',
 'Bobsleigh',
 'Cross Country Skiing',
 'Curling',
 'Figure Skating',
 'Freestyle Skiing',
 'Ice Hockey',
 'Luge',
 'Military Ski Patrol',
 'Nordic Combined',
 'Short Track Speed Skating',
 'Skeleton',
 'Ski Jumping',
 'Snowboarding',
 'Speed Skating']
    
    famous_sports_summer.sort()
    famous_sports_winter.sort()

    for sport in famous_sports_summer:
        temp_df_summer = athlete_df_summer[athlete_df_summer['Sport'] == sport]
        x_summer.append(temp_df_summer[temp_df_summer['Medal'] == 'Gold']['Age'].dropna())
        name_summer.append(sport)
    for sport in famous_sports_winter:
        temp_df_winter = athlete_df_winter[athlete_df_winter['Sport'] == sport]
        x_winter.append(temp_df_winter[temp_df_winter['Medal'] == 'Gold']['Age'].dropna())
        name_winter.append(sport)


    fig_summer = ff.create_distplot(x_summer, name_summer, show_hist=False, show_rug=False)
    fig_summer.update_layout(autosize=False, width=1000, height=600)

    fig_winter = ff.create_distplot(x_winter, name_winter, show_hist=False, show_rug=False)
    fig_winter.update_layout(autosize=False, width=1000, height=600)

    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.write("Here we are visualizing two charts, one from summer and the other from winter. " +
             "(The charts are interactive. Double click on the names of the sports to see their individual curves)")
    with st.container():
        st.subheader("Summer")
        st.plotly_chart(fig_summer)

        sport_list_summer = df_summer['Sport'].unique().tolist()
        sport_list_summer.sort()
        sport_list_summer.insert(0, 'Overall')

    with st.container():
        st.subheader("Winter")
        st.plotly_chart(fig_winter)

        sport_list_winter = df_winter['Sport'].unique().tolist()
        sport_list_winter.sort()
        sport_list_winter.insert(0, 'Overall')


# Men vs Women Participation
    st.title("Men Vs Women Participation")
    st.write("In this section we are showing gender comparision from both summer and winter olympics " +
             "(The charts are interactive. Double click on the gender to see their individual curves)")


    final_summer = processModule.men_vs_women(df_summer)
    final_winter = processModule.men_vs_women(df_winter)


    with st.container():
            st.subheader("Summer")
            fig = px.line(final_summer, x="Year", y=["Male", "Female"])
            fig.update_layout(autosize=False, width=800, height=500)
            st.plotly_chart(fig)

    with st.container():
            st.subheader("Winter")
            fig = px.line(final_winter, x="Year", y=["Male", "Female"])
            fig.update_layout(autosize=False, width=800, height=500)
            st.plotly_chart(fig)