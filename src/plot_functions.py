"""
plots.py

This module contains functions for generating visualizations of the global film industry dataset.

Each function supports customization of labels.
"""

import plotly.graph_objects as go
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from ipywidgets import interact, IntRangeSlider
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot
from itertools import combinations
import networkx as nx
from adjustText import adjust_text
import os
import requests
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display
from scipy.stats import gaussian_kde



##################################################

############## Various plots #####################

##################################################

def plot_interactive_ethnicity_donut(df, column, ethnicities):
    """
    Creates an interactive donut chart for the distribution of specified ethnicities.

    Parameters:
    - df (DataFrame): The DataFrame containing ethnicity data.
    - column (str): The column to analyze.
    - ethnicities (list): The list of ethnicities to include in the plot.

    Returns:
    - None
    """
    # Filter the dataset to include only the specified ethnicities
    filtered_df = df[df[column].isin(ethnicities)]

    # Get the value counts of the specified ethnicities
    ethnicity_counts = filtered_df[column].value_counts()

    # Create the interactive donut chart using Plotly
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=ethnicity_counts.index,
        values=ethnicity_counts.values,
        hole=0.4,
        marker=dict(colors=sns.color_palette('Set2', len(ethnicity_counts)).as_hex()),
        textinfo='percent+label',
        insidetextfont=dict(size=10, color='black'),
        hoverinfo='label+percent+value'
    ))

    # Update layout for better presentation
    fig.update_layout(
        title_text='Distribution of Specified Ethnicities',
        title_x=0.5,
        annotations=[dict(text='Ethnicities', x=0.5, y=0.5, font_size=16, showarrow=False)],
        legend=dict(
            title='Ethnicities',
            x=1.05,
            y=0.5,
            font=dict(size=9)
        ),
        margin=dict(l=20, r=20, t=40, b=20)  # Reduce margins for better fitting
    )

    # Show the plot
    fig.show()

#######

def plot_interactive_genre_sunburst(df, column, min_count_threshold=400):
    """
    Creates an interactive sunburst chart for the distribution of genres in movies.

    Parameters:
    - df (DataFrame): The DataFrame containing genre data.
    - column (str): The column to analyze.
    - min_count_threshold (int): The minimum count of movies per genre to include in the plot.

    Returns:
    - None
    """
    # Count the number of movies per genre
    genre_counts = df[column].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    # Filter genres to include only those with count greater than or equal to the threshold
    filtered_genre_counts = genre_counts[genre_counts['Count'] >= min_count_threshold]

    # Create a sunburst chart using Plotly
    fig = px.sunburst(
        filtered_genre_counts,
        path=['Genre'],
        values='Count',
        title='Distribution of Genres in Movies',
        color='Count',
        color_continuous_scale='RdBu',
    )

    # Customize layout for better readability
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(title="Number of Movies"),
    )

    # Show the plot
    fig.show()

######

def plot_interactive_gender_distribution(df, column):
    """
    Creates an interactive grouped bar chart for the distribution of male and female characters.

    Parameters:
    - df (DataFrame): The DataFrame containing gender data.
    - column (str): The column to analyze.

    Returns:
    - None
    """
    # Get the count of male and female characters
    gender_counts = df[column].value_counts()

    # Create the interactive grouped bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Male', x=['Male'], y=[gender_counts.get('M', 0)], marker=dict(color='skyblue')),
        go.Bar(name='Female', x=['Female'], y=[gender_counts.get('F', 0)], marker=dict(color='orange'))
    ])

    fig.update_layout(
        title_text='Distribution of Male and Female Characters',
        title_x=0.5,
        barmode='group',  # Grouped bar chart to show the gender comparison
        xaxis_title='Gender',
        yaxis_title='Number of Characters',
        legend=dict(
            title='Gender',
            x=1.05,
            y=0.5,
            font=dict(size=10)
        ),
        xaxis=dict(
            tickvals=['Male', 'Female'],
            tickfont=dict(size=12)
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        yaxis=dict(
            tickformat=',',  # Add comma as a thousands separator if the numbers are large
            title_standoff=10  # Reduces space between axis and title
        ),
        width=700,
        height=500
    )
    # Show the plot
    fig.show()

########

def plot_interactive_language_treemap(df, column):
    """
    Creates an interactive treemap chart for the distribution of languages in movies.

    Parameters:
    - df (DataFrame): The DataFrame containing language data.
    - column (str): The column to analyze.

    Returns:
    - None
    """
    # Count the occurrences of each language
    language_counts = df[column].value_counts().reset_index()
    language_counts.columns = ['Language', 'Count']

    # Create a treemap using Plotly
    fig = px.treemap(
        language_counts,
        path=['Language'],
        values='Count',
        title='Language Representation in Movies',
        color='Count',
        color_continuous_scale='RdBu',
    )

    # Customize layout for better readability
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        coloraxis_colorbar=dict(title="Number of Movies"),
    )

    # Show the plot
    fig.show()

#########

def plot_interactive_ethnicity_genre_heatmap(df, genres_column, ethnicity_column, ethnicities, num_top_genres=10):
    """
    Creates an interactive heatmap for character ethnicity representation across top genres.

    Parameters:
    - df (DataFrame): The DataFrame containing genres and ethnicity data.
    - genres_column (str): The column containing genres.
    - ethnicity_column (str): The column containing ethnicity labels.
    - ethnicities (list): The list of ethnicities to include in the plot.
    - num_top_genres (int): The number of top genres to include in the heatmap.

    Returns:
    - None
    """
    # Filter the dataset to include only specified ethnicities
    filtered_df = df[df[ethnicity_column].isin(ethnicities)]

    # Get the top genres by count
    top_genres = filtered_df[genres_column].value_counts().head(num_top_genres).index

    # Filter the dataset to only include the top genres
    top_genres_filtered = filtered_df[filtered_df[genres_column].isin(top_genres)]

    # Group by genres and ethnicities and count the occurrences
    ethnicity_genre_counts = (
        top_genres_filtered
        .groupby([genres_column, ethnicity_column])
        .size()
        .reset_index(name='Count')
    )

    # Create an interactive heatmap using Plotly Express
    fig = px.density_heatmap(
        ethnicity_genre_counts,
        x=ethnicity_column,
        y=genres_column,
        z='Count',
        color_continuous_scale='Viridis',
        title='Character Ethnicity Representation Across Top Genres'
    )

    # Customize layout for better readability
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )

    # Show the plot
    fig.show()

######

def interactive_pie_plot(regions, title='Ethnicities Distribution', category_col='actor_ethnicity_label', num_top=10):
    """
    Generates an interactive pie plot for categorical data across regions

    Parameters:
    - regions (list of tuples): A list of tuples containing region names and corresponding datasets
    - title (str): Title
    - category_col (str): Column name for categorical data (pie plots)
    - num_top (int): Number of top categories to include in the plot (pie plots)

    Returns:
    - None
    """
    fig = go.Figure()

    for idx, (region_name, df) in enumerate(regions):
        # Filter out unknown categories
        filt_df = df[df[category_col] != 'Unknown']
        # Get top ethnicities
        top_categories = filt_df[category_col].value_counts().nlargest(num_top)
        
        fig.add_trace(go.Pie(
            labels=top_categories.index,
            values=top_categories.values,
            name=region_name,
            opacity=0.7,
            visible=True if idx == 0 else False  # Only make the first region visible initially
        ))

    # Add dropdown
    fig.update_layout(
        title=f"Top {num_top} {title} - Europe",
        template='plotly_white',
        updatemenus=[
            dict(
                type="dropdown",
                buttons=[
                    dict(label=region_name,
                         method="update",
                         args=[{"visible": [True if i == idx else False for i in range(len(regions))]},
                              {"title": f"Top {num_top} {title} - {region_name}"}])
                    for idx, (region_name, _) in enumerate(regions)
                ],
                direction="down",
                showactive=True
            )
        ]
    )

    fig.show()


def interactive_histogram_plot(regions, title='Age Distribution by Gender', age_col='age_at_release', gender_col='actor_gender', bins=20):
    """
    Generates an interactive histogram plot for age distribution by gender across regions

    Parameters:
    - regions (list of tuples): A list of tuples containing region names and corresponding datasets
    - title (str): Title of the plot
    - age_col (str): Column name for age data
    - gender_col (str): Column name for gender data
    - bins (int): Number of bins for the histogram

    Returns:
    - None
    """
    
    fig = go.Figure()

    pastel_colors = {'M': 'blue', 'F': 'pink'}

    visibility_indices = []

    for region_idx, (region_name, df) in enumerate(regions):
        indices = []
        for gender in ['M', 'F']:
            age_filtered = df[(df[age_col] >= 0) & (df[age_col] <= 100)]
            filtered_df = age_filtered[age_filtered[gender_col] == gender]

            trace = go.Histogram(
                x=filtered_df[age_col],
                name=f'{region_name} - {gender}',
                opacity=0.6,
                nbinsx=bins,
                marker=dict(color=pastel_colors[gender]),
                visible=True if region_idx == 0 else False
            )

            # Add trace to the figure
            fig.add_trace(trace)
            indices.append(len(fig.data) - 1)

        visibility_indices.append(indices)


    # Add dropdown
    fig.update_layout(
        title=title,
        xaxis_title='Age at Release',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white',
        updatemenus=[
            dict(
                type="dropdown",
                buttons=[
                    dict(label="Europe",
                         method="update",
                         args=[{"visible": [True if i in visibility_indices[0] else False for i in range(len(fig.data))]},
                               {"title": "Age Distribution by Gender - Europe"}]),
                    dict(label="East Europe",
                         method="update",
                         args=[{"visible": [True if i in visibility_indices[1] else False for i in range(len(fig.data))]},
                               {"title": "Age Distribution by Gender - East Europe"}]),
                    dict(label="West Europe",
                         method="update",
                         args=[{"visible": [True if i in visibility_indices[2] else False for i in range(len(fig.data))]},
                               {"title": "Age Distribution by Gender - West Europe"}]),
                    dict(label="Nordic Europe",
                         method="update",
                         args=[{"visible": [True if i in visibility_indices[3] else False for i in range(len(fig.data))]},
                               {"title": "Age Distribution by Gender - Nordic Europe"}]),
                ],
                direction="down",
                showactive=True
            )
        ]
    )   
    fig.show()
