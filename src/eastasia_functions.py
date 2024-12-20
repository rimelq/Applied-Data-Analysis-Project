##############################################
#                                            #
#      East Asia Analysis Python Script      #
#                                            #
##############################################


import os
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from ipywidgets import interact, interactive, Output
import plotly.graph_objects as go
from IPython.display import display
from scipy.stats import gaussian_kde
import plotly.express as px

DATA_FOLDER = './data/final/'


# FUNCTIONS--------------------------------:


def var_loader(DATA_FOLDER, mode='hollywood'):
    results = []
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"{mode}_data.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"{mode}_data_ethnicity.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"{mode}_ethnic_realworld.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"male_{mode}_realworld_averages.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"female_{mode}_realworld_averages.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"bothsexes_{mode}_realworld_averages.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"male_{mode}_realworld_proportions.csv"))
    results.append(pd.read_csv(DATA_FOLDER + f"{mode}/"+ f"female_{mode}_realworld_proportions.csv"))
    return results

# Charging the East-Asia datasets in their respective dataframes
eastasia_data, eastasia_data_ethnicity, eastasia_ethnic_realworld, \
male_eastasia_realworld_averages, female_eastasia_realworld_averages, \
bothsexes_eastasia_realworld_averages, male_eastasia_realworld_proportions, \
female_eastasia_realworld_proportions = var_loader(DATA_FOLDER, mode="eastasia")


###############################################################


def prepare_ethnicity_proportion_data(cinema_data, real_world_data, output_path, period='1996-2012'):
    """
    Prepare a dataset comparing cinema representation and real-world proportions for specified ethnicities over a given period.
    """
    
    # Cinema Data Processing
    cinema_df = cinema_data['actor_ethnicity_classification'].value_counts().reset_index()
    cinema_df.columns = ['Ethnicity', 'Movies_Produced']

    # Desired ethnicities for analysis
    desired_ethnicities = ['Chinese', 'Japanese', 'Koreans', 'Taiwanese', 'Other Asians']
    cinema_df = cinema_df[cinema_df['Ethnicity'].isin(desired_ethnicities)]
    
    # Real-World Data Processing
    real_world_period = real_world_data[real_world_data['new_period'] == period]
    real_world_period = real_world_period.rename(columns={'group': 'Ethnicity', 'size': 'RealWorld_Proportion'})
    
    real_world_period = real_world_period[real_world_period['Ethnicity'].isin(desired_ethnicities)]
    
    # Normalize to percentage
    real_world_period['RealWorld_Proportion (%)'] = (
        real_world_period['RealWorld_Proportion'] / real_world_period['RealWorld_Proportion'].sum()
    ) * 100
    
    data_merged = pd.merge(
        cinema_df,
        real_world_period[['Ethnicity', 'RealWorld_Proportion (%)']],
        on='Ethnicity',
        how='outer'
    )
    
    # Add Cinema Proportion as a percentage
    data_merged['Cinema_Proportion (%)'] = (
        data_merged['Movies_Produced'] / data_merged['Movies_Produced'].sum()
    ) * 100
    
    # Fill potential NaN values
    data_merged.fillna(0, inplace=True)
    
    period_data = []
    for _, row in data_merged.iterrows():
        period_data.append({
            'Ethnicity': row['Ethnicity'],
            'Category': 'Real-World',
            'Percentage': row['RealWorld_Proportion (%)']
        })
        period_data.append({
            'Ethnicity': row['Ethnicity'],
            'Category': 'Cinema',
            'Percentage': row['Cinema_Proportion (%)']
        })
    
    period_df = pd.DataFrame(period_data)
    
    period_df.to_csv(output_path, index=False)
    
    print(f"Data saved to: {output_path}")
    return period_df


###############################################################


def plot_temporal_trends(cinema_pivot, output_path):
    """
    Plots temporal trends for East Asian Cinema Representation with annotations.
    """
    
    custom_colors = {
        'Chinese': '#5c1165',
        'Japanese': '#39b185',
        'Koreans': '#9ccb86',
        'Taiwanese': '#cf597e',
        'Other Asians': '#eeb479'
    }
    
    y_max = cinema_pivot.max().max()
    y_range = [0, y_max + 10]  # Add 10% padding for readability

    # Creating the timeline plot
    fig = go.Figure()

    # Add one line for each ethnicity
    for ethnicity, color in custom_colors.items():
        fig.add_trace(go.Scatter(
            x=cinema_pivot.index, 
            y=cinema_pivot[ethnicity], 
            mode='lines+markers', 
            name=ethnicity,
            line=dict(color=color, width=3),
            marker=dict(size=8)
        ))

    # Adjusting annotations for better visibility
    annotations = [
        dict(
            x='1950–1965',
            y=y_max * 0.55,  
            text="Golden Age of Japanese Cinema",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-60,
            font=dict(size=12, color="black"),
            align='center'
        ),
        dict(
            x='1966–1980',
            y=y_max * 0.55,
            text="Rise of Martial Arts Films",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-60,
            font=dict(size=12, color="black"),
            align='center'
        ),
        dict(
            x='1981–1995',
            y=y_max * 0.4,
            text="Studio Ghibli's Success",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-60,
            font=dict(size=12, color="black"),
            align='center'
        ),
        dict(
            x='1996–2012',
            y=y_max * 0.7,
            text="Korean Wave",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(size=12, color="black"),
            align='center'
        )
    ]

    fig.update_layout(
        title={
            'text': "<b>Temporal Trends in East Asian Cinema Representation</b><br><span style='font-size:14px;'>(Period: 1950–2012)</span>",
            'x': 0.5, 
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': 'black'}
        },
        xaxis=dict(
            title="Time Periods",
            tickmode='array',
            tickvals=list(cinema_pivot.index),
            ticktext=list(cinema_pivot.index),
            titlefont=dict(size=12, color="black")
        ),
        yaxis=dict(
            title="Representation Proportion (%)",
            range=y_range,  
            titlefont=dict(size=12, color="black")
        ),
        legend=dict(
            title=dict(text="Ethnicities", font=dict(size=12, color="black")),
            font=dict(size=11, color="black"),
            x=1,
            y=1
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  
        paper_bgcolor="#F2F0F0",  
        font=dict(color="black"),  
        margin=dict(t=120), 
        annotations=annotations  
    )
    fig.show()

    # Save the plot as an HTML file
    fig.write_html(output_path)
    print(f"Plot saved to {output_path}")


###############################################################


def create_gender_radar_chart(eastasia_data, radar_html_path):
    """
    Creates a radar chart showing the gender gap in cinema genres and saves output files.
    """
    
    # Map gender values
    eastasia_data['actor_gender'] = eastasia_data['actor_gender'].map({'M': 'Male', 'F': 'Female'})

    # Aggregate data by gender and genre
    gender_genre_data = (
        eastasia_data
        .groupby(['main_genre', 'actor_gender'])
        .size()
        .reset_index(name='Count')
    )
    gender_genre_data['Proportion'] = (
        gender_genre_data
        .groupby('main_genre')['Count']
        .transform(lambda x: x / x.sum() * 100)
    )

    #  Pivot data for radar chart
    radar_data = (
        gender_genre_data
        .pivot(index='main_genre', columns='actor_gender', values='Proportion')
        .fillna(0)
        .reset_index()
    )

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=radar_data['Male'],
        theta=radar_data['main_genre'],
        fill='toself',
        name='Male',
        line=dict(color='#009392')  # Male color
    ))

    fig.add_trace(go.Scatterpolar(
        r=radar_data['Female'],
        theta=radar_data['main_genre'],
        fill='toself',
        name='Female',
        line=dict(color='#7c1d6f')  # Female color
    ))

    # Update layout for better visualization
    fig.update_layout(
        polar=dict(
            bgcolor="#F8F7F7",  
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title={
            'text': "<b>Gender Gap Radar Chart by Genre</b><br><span style='font-size:16px;'>(All Periods)</span>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'black'}  
        },
        legend_title={
            'text': "Gender",
            'font': {'color': 'black', 'size': 14}  
        },
        template="plotly_white",
        paper_bgcolor="#F2F0F0", 
        font=dict(color='black'),
        margin=dict(t=120)
    )

    fig.write_html(radar_html_path)
    print(f"Radar chart saved at: {radar_html_path}")

    # Show the radar chart
    fig.show()


###############################################################


def create_age_distribution_violin_plots(female_realworld, male_realworld, eastasia_data,
    male_output_path, female_output_path):
    """
    Creates violin plots comparing the age distributions of male and female actors in East Asian cinema to real-world population data.
    """
    
    # Melt the real-world data for females and males
    female_realworld_long = female_realworld.melt(
        id_vars=['Time Period'], var_name='Age', value_name='Proportion'
    )
    female_realworld_long['Gender'] = 'Female'

    male_realworld_long = male_realworld.melt(
        id_vars=['Time Period'], var_name='Age', value_name='Proportion'
    )
    male_realworld_long['Gender'] = 'Male'

    # Combine male and female real-world data
    real_world_data = pd.concat([female_realworld_long, male_realworld_long])

    # Add "Real-World" as the source for real-world data
    real_world_data['Source'] = 'Real-World'

    # Create release periods in cinema data
    eastasia_data['release_period'] = pd.cut(
        eastasia_data['release_y'],
        bins=[1950, 1965, 1980, 1995, 2012],
        labels=['1950–1965', '1966–1980', '1981–1995', '1996–2012']
    )

    # Prepare cinema data
    cinema_data = eastasia_data[['age_at_release', 'actor_gender', 'release_period']].rename(
        columns={'age_at_release': 'Age', 'actor_gender': 'Gender', 'release_period': 'Source'}
    )

    # Adjust real-world age column
    real_world_data['Age'] = real_world_data['Age'].replace('100+', '100').astype(int)

    # Combine real-world and cinema data
    cinema_data['Proportion'] = 1  # Placeholder for cinema proportions
    combined_data = pd.concat(
        [real_world_data[['Age', 'Proportion', 'Gender', 'Source']],
         cinema_data[['Age', 'Proportion', 'Gender', 'Source']]],
        ignore_index=True
    )

    # Define custom colors for the sources
    source_colors = {
        'Real-World': "#7c1d6f",  
        '1950–1965': "#39b185",  
        '1966–1980': "#cf597e",   
        '1981–1995': "#e9e29c",  
        '1996–2012': "#eeb479",  
    }

    # Filter data for males and females
    male_data = combined_data[combined_data['Gender'] == 'Male']
    female_data = combined_data[combined_data['Gender'] == 'Female']

    # Create and customize the male violin plot
    fig_male = px.violin(
        male_data, x='Age', color='Source', points='all', box=True,
        title=("<b style='color: black;'>East Asian Cinema vs Real World Population: Age Distribution Comparison for Males</b>"
               "<br><span style='font-size: 16px; color: black;'>(Period: 1950–2012)</span>"),
        labels={'Age': 'Age', 'Source': 'Data Source'},
        template='plotly_white', color_discrete_map=source_colors
    )
    fig_male.update_layout(
        legend_title="<span style='color: black;'>Data Source</span>",
        legend=dict(
            font=dict(color="black"),
            y=0.7,  
            x=1.0,   
            xanchor='right'  
        ),
        height=800, plot_bgcolor="#F2F0F0", paper_bgcolor="#F2F0F0",
        title=dict(y=0.92, x=0.5, xanchor='center', font=dict(size=20, family="Arial"))
    )

    # Create and customize the female violin plot
    fig_female = px.violin(
        female_data, x='Age', color='Source', points='all', box=True,
        title=("<b style='color: black;'>East Asian Cinema vs Real World Population: Age Distribution Comparison for Females</b>"
               "<br><span style='font-size: 16px; color: black;'>(Period: 1950–2012)</span>"),
        labels={'Age': 'Age', 'Source': 'Data Source'},
        template='plotly_white', color_discrete_map=source_colors
    )
    fig_female.update_layout(
        legend_title="<span style='color: black;'>Data Source</span>",
        legend=dict(
            font=dict(color="black"),
            y=0.7, 
            x=1.0,  
            xanchor='right' 
        ),
        height=800, plot_bgcolor="#F2F0F0", paper_bgcolor="#F2F0F0",
        title=dict(y=0.92, x=0.5, xanchor='center', font=dict(size=20, family="Arial"))
    )

    # Save the plots as HTML
    fig_male.write_html(male_output_path)
    fig_female.write_html(female_output_path)

    # Show the plots
    fig_male.show()
    fig_female.show()

    print(f"Male violin plot saved at: {male_output_path}")
    print(f"Female violin plot saved at: {female_output_path}")


###############################################################


def prepare_flourish_bar_race(eastasia_data, output_path):
    """
    Prepares data for a Flourish bar race visualization.
    """
    
    # Filter data for the years 1950-2012
    filtered_data = eastasia_data[(eastasia_data['release_y'] >= 1950) & (eastasia_data['release_y'] <= 2012)]

    # Defining smaller periods (5-year intervals)
    filtered_data['release_period'] = pd.cut(
        filtered_data['release_y'],
        bins=[1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2012],
        labels=[
            '1950', '1955', '1960', '1965', '1970', '1975',
            '1980', '1985', '1990', '1995', '2000', '2005',
            '2010'
        ]
    )

    # Grouping by genre, gender, and release period
    gender_genre_time = filtered_data.groupby(['main_genre', 'actor_gender', 'release_period']).size().reset_index(name='Count')
    gender_genre_time['Proportion'] = gender_genre_time.groupby(['release_period', 'actor_gender'])['Count'].transform(lambda x: x / x.sum() * 100)

    # Filter for female data only
    female_data = gender_genre_time[gender_genre_time['actor_gender'] == 'Female']

    # Pivot data for Flourish bar race format
    flourish_format = female_data.pivot(index='main_genre', columns='release_period', values='Proportion').fillna(0).reset_index()
    flourish_format.rename(columns={'main_genre': 'Genre'}, inplace=True)

    # Save to CSV
    flourish_format.to_csv(output_path, index=False)
    print(f"Data saved successfully at: {output_path}")
