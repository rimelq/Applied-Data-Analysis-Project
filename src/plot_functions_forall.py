import os
import pandas as pd
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from ipywidgets import interactive, HBox, VBox
import plotly.graph_objects as go
from IPython.display import display
from scipy.stats import gaussian_kde
from plot_functions import *
import os

output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots_html")
os.makedirs(output_folder, exist_ok=True)


DATA_FOLDER = '/Users/zaynebmellouli/MA1/ada-2024-project-advanceddestroyers0fall/data/final/'
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

# Charging the Hollywood datasets in their respective dataframes
hollywood_data, hollywood_data_ethnicity, hollywood_ethnic_realworld, \
male_hollywood_realworld_averages, female_hollywood_realworld_averages, \
bothsexes_hollywood_realworld_averages, male_hollywood_realworld_proportions, \
female_hollywood_realworld_proportions = var_loader(DATA_FOLDER, mode="hollywood")

# Charging the Bollywood datasets in their respective dataframes
bollywood_data, bollywood_data_ethnicity, bollywood_ethnic_realworld, \
male_bollywood_realworld_averages, female_bollywood_realworld_averages, \
bothsexes_bollywood_realworld_averages, male_bollywood_realworld_proportions, \
female_bollywood_realworld_proportions = var_loader(DATA_FOLDER, mode="bollywood")

# Charging the East-Asia datasets in their respective dataframes
eastasia_data, eastasia_data_ethnicity, eastasia_ethnic_realworld, \
male_eastasia_realworld_averages, female_eastasia_realworld_averages, \
bothsexes_eastasia_realworld_averages, male_eastasia_realworld_proportions, \
female_eastasia_realworld_proportions = var_loader(DATA_FOLDER, mode="eastasia")

# Prepare the region data
region_data = {
    'Hollywood': {
        'region_data': hollywood_data,
        'male_real_world_proportions': male_hollywood_realworld_proportions,
        'female_real_world_proportions': female_hollywood_realworld_proportions,
        'male_real_world_averages': male_hollywood_realworld_averages,
        'female_real_world_averages': female_hollywood_realworld_averages,
        'bothsexes_real_world_averages': bothsexes_hollywood_realworld_averages,
        'data_ethnicity': hollywood_data_ethnicity,
        'realworld_ethnicity': hollywood_ethnic_realworld,
        'ethnicities': [
            "African Americans", 
            "American Indians", 
            "Arab Americans", 
            "Asian Americans", 
            "Caucasian Americans", 
            "Jewish Americans", 
            "Latino Americans"
        ]
    },
    
    'Bollywood': {
        'region_data': bollywood_data,
        'male_real_world_proportions': male_bollywood_realworld_proportions,
        'female_real_world_proportions': female_bollywood_realworld_proportions,
        'male_real_world_averages': male_bollywood_realworld_averages,
        'female_real_world_averages': female_bollywood_realworld_averages,
        'bothsexes_real_world_averages': bothsexes_bollywood_realworld_averages,
        'data_ethnicity': bollywood_data_ethnicity,
        'realworld_ethnicity': bollywood_ethnic_realworld,
        'ethnicities': [
            "South_Indian_Ethnicities", 
            "North_Indian_Ethnicities", 
            "Eastern_Indian_Ethnicities", 
            "Western_and_Central_Indian_Ethnicities", 
            "Religious_and_Caste_Groups"
        ]
    },
    
     'Eastasia': {
         'region_data': eastasia_data,
         'male_real_world_proportions': male_eastasia_realworld_proportions,
         'female_real_world_proportions': female_eastasia_realworld_proportions,
         'male_real_world_averages': male_eastasia_realworld_averages,
         'female_real_world_averages': female_eastasia_realworld_averages,
         'bothsexes_real_world_averages': bothsexes_eastasia_realworld_averages,
         'data_ethnicity': eastasia_data_ethnicity,
         'realworld_ethnicity': eastasia_ethnic_realworld,
         'ethnicities': [
             "Chinese", 
             "Taiwanese", 
             "Japanese", 
             "Koreans", 
             "Other Asians"
         ]
     }  
}

# Generate the list of unique regions
regions = list(region_data.keys())
periods = ["All periods", "1950-1965", "1966-1980", "1981-1995", "1996-2012"]


def create_ethnicity_comparison_graph2():

    # Create the initial figure widget
    fig = go.FigureWidget()
   
    # Function to calculate the weighted proportions of actor ethnicities per film
    def calculate_weighted_actor_ethnicities(df, period, genre, ethnicities):
        df = df.copy()
        if period != "All periods":
            start_year, end_year = map(int, period.split('-'))
            df = df[df['release'].between(start_year, end_year)]
        if genre != "All":
            df = df[df['main_genre'] == genre]
        df['casting_size'] = df.groupby('movie_name')['movie_name'].transform('count')
        film_ethnicities = df.groupby(['movie_name', 'actor_ethnicity_classification']).size().unstack(fill_value=0)
        film_ethnicities = film_ethnicities.div(film_ethnicities.sum(axis=1), axis=0)
        film_ethnicities['casting_size'] = df.groupby('movie_name')['casting_size'].first()
        weighted_ethnicities = film_ethnicities.drop(columns='casting_size').multiply(film_ethnicities['casting_size'], axis=0).sum() / film_ethnicities['casting_size'].sum()
        weighted_ethnicities = weighted_ethnicities.reindex(ethnicities, fill_value=0)
        return weighted_ethnicities

    # Function to display the comparison graph with Plotly
    def plot_ethnicity_comparison(region, period="All periods", genre="All"):
        # Get the datasets for the selected region
        datasets = region_data[region]
        data_ethnicity = datasets['data_ethnicity']
        realworld_ethnicity = datasets['realworld_ethnicity']
        ethnicities = datasets['ethnicities']

        if period == "All periods":
            population_ethnicities = realworld_ethnicity.groupby('group')['size'].mean()
        else:
            population_ethnicities = realworld_ethnicity[
                realworld_ethnicity['new_period'] == period
            ].set_index('group')['size']
        actor_ethnicities = calculate_weighted_actor_ethnicities(data_ethnicity, period, genre, ethnicities)
        left_values = population_ethnicities.values * 100
        right_values = actor_ethnicities.values * 100
        ethnicities_labels = population_ethnicities.index

        # Update the traces of the figure widget
        with fig.batch_update():
            fig.data = []  # Clear the existing data
            fig.layout.annotations = []  # Clear the existing annotations
            
            # Real-world population bars
            fig.add_trace(go.Bar(
                x=left_values,
                y=ethnicities_labels,
                orientation='h',
                name="Real-world Population",
                marker=dict(color='teal', opacity=0.8),
                hovertemplate="Real-world: %{x:.1f}%"
            ))

            # Movie industry bars
            fig.add_trace(go.Bar(
                x=[-v for v in right_values],
                y=ethnicities_labels,
                orientation='h',
                name=f"{region} Industry",
                marker=dict(color='purple', opacity=0.8),
                hovertemplate=f"{region} Industry: %{{x:.1f}}%%"  # Escaped curly braces
            ))

            # Update the layout for the figure
            title_text = f"Comparison of {region} Industry Ethnicity Proportions<br>(Period: {period}, Genre: {genre})"
            dynamic_width = max(len(title_text) * 7, 900)  # Approximation: 7 pixels per character, min width of 900

            fig.update_layout(
                title={
                    'text': title_text,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'pad': {'b': 10}  # Add padding below the title
                },
                xaxis_title="Proportion (%)",
                yaxis_title="Ethnicity Group",
                barmode='relative',
                xaxis=dict(
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='gray',
                    title=f"← {region} Industry | Real-world Population →",
                    tickvals=[-50, -25, 0, 25, 50],
                    ticktext=["50", "25", "0", "25", "50"]
                ),
                width=dynamic_width,  # Dynamically set width
                height=600,
                template='plotly_white',
                legend=dict(
                    title="Sources",
                    orientation="h",
                    yanchor="bottom",
                    y=1.0,  # Adjust the legend position
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=125)  # Increase top margin to add more space at the top
            )
            # Add a dynamic central line
            fig.add_shape(
                type="line",
                x0=0, x1=0, y0=-0.5, y1=len(ethnicities_labels) - 0.5,
                line=dict(color="black", width=2, dash="dash")
            )

    # Initialize widgets
    region_widget = widgets.Dropdown(
        options=regions,
        value=regions[0],
        description='Region',
        disabled=False
    )

    period_widget = widgets.Dropdown(
        options=["All periods", "1950-1965", "1966-1980", "1981-1995", "1996-2012"],
        value="All periods",
        description='Period',
        disabled=False
    )

    genres_widget = widgets.Dropdown(
        options=['All'],  # Will update based on selected region
        value='All',
        description='Genre',
        disabled=False
    )

    def update_genres(*args):
        # Get the selected region
        selected_region = region_widget.value
        # Get the genres for the selected region
        selected_data = region_data[selected_region]['data_ethnicity']
        unique_genres = ['All'] + sorted(selected_data['main_genre'].dropna().unique())
        genres_widget.options = unique_genres
        genres_widget.value = 'All'

    # Attach the update_genres function to changes in the region_widget
    region_widget.observe(update_genres, names='value')

    # Initialize genres
    update_genres()

    # Interactive widget
    def plot_ethnicity_comparison_widget(region, period, genre):
        plot_ethnicity_comparison(region, period, genre)

    # Interactive widgets setup
    interactive_plot = interactive(
        plot_ethnicity_comparison_widget,
        region=region_widget,
        period=period_widget,
        genre=genres_widget
    )

    # Display widgets first, then the plot
    display(region_widget, period_widget, genres_widget)
    display(fig)
    output_path = os.path.join(output_folder, "ethnicity_comparison.html")
    try:
        fig.write_html(output_path, full_html=True, include_plotlyjs='cdn')
        print(f"Plot saved successfully to: {output_path}")
    except Exception as e:
        print(f"Error saving plot: {str(e)}")


def create_gender_proportions_graph2():
    # Create the initial figure widget
    fig = go.FigureWidget()

    # Function to prepare real-world data by setting 'Time Period' as the index
    def prepare_real_world_data(male_real_world_df, female_real_world_df):
        if 'Time Period' not in male_real_world_df.columns:
            male_real_world_df.reset_index(inplace=True)
        if 'Time Period' not in female_real_world_df.columns:
            female_real_world_df.reset_index(inplace=True)
        male_real_world_df.set_index('Time Period', inplace=True)
        female_real_world_df.set_index('Time Period', inplace=True)
        return male_real_world_df, female_real_world_df

    # Function to calculate weighted gender proportions per genre and period
    def calculate_weighted_gender_proportions(df, period, genre):
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=['release'])
        df_filtered['release'] = df_filtered['release'].astype(int)
        if period != "All periods":
            start_year, end_year = map(int, period.split('-'))
            df_filtered = df_filtered[df_filtered['release'].between(start_year, end_year)]
        if genre != "All":
            df_filtered = df_filtered[df_filtered['main_genre'] == genre]
        df_filtered = df_filtered.dropna(subset=['actor_gender'])
        if df_filtered.empty:
            return 0, 0
        df_filtered['casting_size'] = df_filtered.groupby('movie_name')['movie_name'].transform('count')
        gender_counts = df_filtered.groupby(['movie_name', 'actor_gender']).size().unstack(fill_value=0)
        for gender_col in ['M', 'F']:
            if gender_col not in gender_counts.columns:
                gender_counts[gender_col] = 0
        gender_proportions = gender_counts.div(gender_counts.sum(axis=1), axis=0)
        gender_proportions['casting_size'] = df_filtered.groupby('movie_name')['casting_size'].first()
        weighted_proportions = (
            gender_proportions[['M', 'F']]
            .multiply(gender_proportions['casting_size'], axis=0)
            .sum()
        ) / gender_proportions['casting_size'].sum()
        male_proportion = weighted_proportions['M']
        female_proportion = weighted_proportions['F']
        total = male_proportion + female_proportion
        if total > 0:
            male_proportion /= total
            female_proportion /= total
        return male_proportion, female_proportion

    # Function to get real-world gender proportions
    def get_real_world_gender_proportions(period, male_real_world_df, female_real_world_df):
        if period == "All periods":
            male_total = male_real_world_df.sum().sum()
            female_total = female_real_world_df.sum().sum()
        else:
            if period not in male_real_world_df.index or period not in female_real_world_df.index:
                male_total = 0
                female_total = 0
            else:
                male_row = male_real_world_df.loc[period]
                female_row = female_real_world_df.loc[period]
                male_total = male_row.sum()
                female_total = female_row.sum()
        total = male_total + female_total
        if total == 0:
            male_proportion = 0.5
            female_proportion = 0.5
        else:
            male_proportion = male_total / total
            female_proportion = female_total / total
        return male_proportion, female_proportion

    # Function to plot gender proportions using the same figure object
    def plot_gender_proportions(region, period, genre):
        datasets = region_data[region]
        region_df = datasets['region_data']
        male_real_world_df = datasets['male_real_world_proportions'].copy()
        female_real_world_df = datasets['female_real_world_proportions'].copy()

        male_real_world_df, female_real_world_df = prepare_real_world_data(male_real_world_df, female_real_world_df)

        genre_list = [genre] if genre != "All" else sorted(region_df['main_genre'].dropna().unique())

        proportions = []
        for genre in genre_list:
            male_prop, female_prop = calculate_weighted_gender_proportions(region_df, period, genre)
            total = male_prop + female_prop
            if total > 0:
                male_prop /= total
                female_prop /= total
            proportions.append({
                "Category": genre,
                "Male": male_prop,
                "Female": female_prop,
                "Type": "Genre"
            })

        male_population, female_population = get_real_world_gender_proportions(period, male_real_world_df, female_real_world_df)
        total_population = male_population + female_population
        if total_population > 0:
            male_population /= total_population
            female_population /= total_population
        proportions.append({
            "Category": "Real-world Population",
            "Male": male_population,
            "Female": female_population,
            "Type": "Real-world"
        })

        proportions_df = pd.DataFrame(proportions)

        fig.data = []  # Clear existing data
        fig.layout.annotations = []  # Clear existing annotations

        male_color = 'teal'
        female_color = 'purple'

        male_legend_added = False
        female_legend_added = False
        for idx, row in proportions_df.iterrows():
            male_pattern = dict(shape='x') if row['Type'] == 'Real-world' else dict()
            female_pattern = dict(shape='x') if row['Type'] == 'Real-world' else dict()

            show_male_legend = not male_legend_added
            if show_male_legend:
                male_legend_added = True
            fig.add_trace(go.Bar(
                x=[row['Category']],
                y=[row['Male']],
                name='Male',
                marker=dict(color=male_color, pattern=male_pattern),
                hovertemplate=f"Male: {row['Male']*100:.1f}%<extra></extra>",
                showlegend=show_male_legend,
                legendgroup='Male',
            ))

            show_female_legend = not female_legend_added
            if show_female_legend:
                female_legend_added = True
            fig.add_trace(go.Bar(
                x=[row['Category']],
                y=[row['Female']],
                name='Female',
                marker=dict(color=female_color, pattern=female_pattern),
                hovertemplate=f"Female: {row['Female']*100:.1f}%<extra></extra>",
                base=[row['Male']],
                showlegend=show_female_legend,
                legendgroup='Female',
            ))

            if row['Male'] > 0:
                fig.add_annotation(
                    x=row['Category'],
                    y=row['Male'] / 2,
                    text=f"{row['Male'] * 100:.1f}%",
                    showarrow=False,
                    font=dict(color='white', size=12),
                    yanchor='middle',
                    xanchor='center'
                )
            if row['Female'] > 0:
                fig.add_annotation(
                    x=row['Category'],
                    y=row['Male'] + row['Female'] / 2,
                    text=f"{row['Female'] * 100:.1f}%",
                    showarrow=False,
                    font=dict(color='white', size=12),
                    yanchor='middle',
                    xanchor='center'
                )

        fig.update_layout(
            title={
                'text': f'Gender Proportions by Genre & Real-world Population in {region}<br>(Period: {period})',
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'pad': {'b': 20}
            },
            autosize=True,
            width=1200,
            height=600,
            xaxis_title='Movie Genres Compared to Real-world Population',
            yaxis_title='Proportion',
            barmode='stack',
            template='plotly_white',
            xaxis_tickangle=-25,
            legend=dict(
                title="Gender",
                orientation="h",
                yanchor="bottom",
                y=0.97,
                xanchor="center",
                x=0.5
            ),
            bargap=0.15,
            bargroupgap=0.0,
            margin=dict(t=100)
        )

    region_widget = widgets.Dropdown(
        options=regions,
        value=regions[0],
        description='Region',
        disabled=False,
    )

    period_widget = widgets.Dropdown(
        options=periods,
        value='All periods',
        description='Period',
        disabled=False,
    )

    genres_widget = widgets.Dropdown(
        options=['All'],  # Initially empty; will update based on selected region
        value='All',
        description='Genre',
        disabled=False,
    )

    def update_genres(*args):
        selected_region = region_widget.value
        selected_data = region_data[selected_region]['region_data']
        unique_genres = sorted(selected_data['main_genre'].dropna().unique())
        unique_genres = ['All'] + unique_genres
        genres_widget.options = unique_genres
        genres_widget.value = 'All'

    region_widget.observe(update_genres, names='value')

    update_genres()

    def plot_gender_proportions_widget(region, period, genre):
        plot_gender_proportions(region, period, genre)

    # Create interactive widgets
    interactive_plot = interactive(
        plot_gender_proportions_widget,
        region=region_widget,
        period=period_widget,
        genre=genres_widget
    )

    # Organize widgets in a vertical box layout
    widgets_box = VBox([
        HBox([region_widget]),
        HBox([period_widget]),
        HBox([genres_widget])
    ])

    # Display widgets first, then the plot
    display(widgets_box)
    display(fig)

    # Initial plot with default values
    plot_gender_proportions(region_widget.value, period_widget.value, genres_widget.value)

    # Save gender comparison plot
    output_path = os.path.join(output_folder, "gender_comparison.html")
    try:
        fig.write_html(output_path, full_html=True, include_plotlyjs='cdn')
        print(f"Plot saved successfully to: {output_path}")
    except Exception as e:
        print(f"Error saving plot: {str(e)}")

def create_age_distribution_graph2():
    # Create the global figure object using FigureWidget
    fig = go.FigureWidget()

    # Function to plot age distribution
    def plot_age_distribution(region, gender='Both', period='All periods', genre='All'):
        # Get the datasets for the selected region
        datasets = region_data[region]
        region_df = datasets['region_data']
        male_real_world_averages = datasets['male_real_world_averages']
        female_real_world_averages = datasets['female_real_world_averages']
        bothsexes_real_world_averages = datasets['bothsexes_real_world_averages']

        # Map the period to start and end years
        period_years = {
            "All periods": (1950, 2012),
            "1950-1965": (1950, 1965),
            "1966-1980": (1966, 1980),
            "1981-1995": (1981, 1995),
            "1996-2012": (1996, 2012)
        }
        start_year, end_year = period_years[period]

        # Get the real population age distribution
        if gender == 'Male':
            df_real = male_real_world_averages.copy()
        elif gender == 'Female':
            df_real = female_real_world_averages.copy()
        else:  # Both
            df_real = bothsexes_real_world_averages.copy()

        # Ensure 'Time Period' is present
        if 'Time Period' not in df_real.columns:
            print("Time Period column not found in real-world data.")
            return

        # Exclude non-age columns
        age_columns = df_real.columns.drop('Time Period', errors='ignore')

        # Convert age columns to numeric
        df_real[age_columns] = df_real[age_columns].apply(pd.to_numeric, errors='coerce')

        # Handle NaN values
        df_real[age_columns] = df_real[age_columns].fillna(0)

        # Aggregate real population data
        if period == "All periods":
            real_age_distribution = df_real[age_columns].sum()
        else:
            filtered_df_real = df_real[df_real['Time Period'] == period]
            if filtered_df_real.empty:
                print(f"No real population data available for the selected period: {period}")
                return
            real_age_distribution = filtered_df_real[age_columns].iloc[0]

        # Normalize the real age distribution
        real_age_distribution = real_age_distribution / real_age_distribution.sum()

        # Clean the index
        real_age_distribution.index = (
            real_age_distribution.index.astype(str)
            .str.replace('+', '', regex=False)
            .astype(int)
        )

        # Filter out invalid ages
        real_age_distribution = real_age_distribution[real_age_distribution.index >= 0]

        # Get the actors' age distribution
        df_actors = region_df.copy()
        df_actors = df_actors.dropna(subset=['release'])
        df_actors['release'] = df_actors['release'].astype(int)
        df_actors = df_actors[df_actors['release'].between(start_year, end_year)]

        # Clean 'actor_gender' column
        df_actors['actor_gender'] = df_actors['actor_gender'].astype(str).str.upper()

        # Map gender selection to data labels
        gender_mapping = {
            'Male': 'M',
            'Female': 'F',
            'Both': ['M', 'F']
        }
        selected_genders = gender_mapping[gender]

        # Filter by gender
        if gender != 'Both':
            df_actors = df_actors[df_actors['actor_gender'] == selected_genders]
        else:
            df_actors = df_actors[df_actors['actor_gender'].isin(selected_genders)]

        # Filter by genre
        if genre != 'All':
            df_actors = df_actors[df_actors['main_genre'] == genre]

        # Handle empty data
        if df_actors.empty:
            print("No actor data available for the selected filters.")
            return

        # Process actor ages
        actor_ages = df_actors['age_at_release'].dropna().astype(float)
        actor_ages = actor_ages[actor_ages >= 0]  # Filter out negative ages

        # Handle empty actor ages
        if actor_ages.empty:
            print("No actor age data available for the selected filters.")
            return

        # Define a fixed age range for consistency
        age_min = 0
        age_max = 100
        age_range = np.linspace(age_min, age_max, 500)

        # Real population ages
        real_ages = np.repeat(real_age_distribution.index.values, (real_age_distribution * 1000).astype(int))
        real_ages = real_ages[real_ages >= age_min]  # Filter out ages below age_min
        if len(real_ages) == 0:
            print("No real population age data available for the selected filters.")
            return

        # Create Kernel Density Estimation (KDE) for real population
        real_kde = gaussian_kde(real_ages)
        real_density = real_kde(age_range)
        real_density /= real_density.sum()

        # Actor ages
        actor_ages = actor_ages[actor_ages <= age_max]  # Filter out ages above age_max
        actor_kde = gaussian_kde(actor_ages)
        actor_density = actor_kde(age_range)
        actor_density /= actor_density.sum()

        # Handle empty plots
        if real_density.sum() == 0 and actor_density.sum() == 0:
            print("No data available to plot for the selected filters.")
            return

        # Determine the maximum density value and set y-axis range
        max_density = max(real_density.max(), actor_density.max())
        y_max = min(max_density * 1.2, 0.05)  # Add 20% buffer, cap at 0.05

        # Generate dynamic title and width
        title_text = f'Age Distribution Comparison in {region}<br>(Gender: {gender}, Period: {period}, Genre: {genre})'
        dynamic_width = max(len(title_text) * 7, 1100)

        # Update the figure widget with new data
        with fig.batch_update():
            fig.data = []  # Clear existing data

            fig.add_trace(go.Scatter(
                x=age_range,
                y=real_density,
                name='Real-world Population',
                mode='lines',
                line=dict(color='teal'),
                fill='tozeroy',
                fillcolor='rgba(0, 128, 128, 0.2)',  # Teal with opacity
                hovertemplate='Age %{x:.1f}: %{y:.2%}<extra>Real-world Population</extra>'
            ))
            fig.add_trace(go.Scatter(
                x=age_range,
                y=actor_density,
                name='Actors',
                mode='lines',
                line=dict(color='purple'),
                fill='tozeroy',
                fillcolor='rgba(128, 0, 128, 0.2)',  # Purple with opacity
                hovertemplate='Age %{x:.1f}: %{y:.2%}<extra>Actors</extra>'
            ))

            # Adjust layout
            fig.update_layout(
                title={
                    'text': title_text,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'pad': {'b': 20}
                },
                width=dynamic_width,
                height=550,
                xaxis_title='Age',
                yaxis_title='Density',
                template='plotly_white',
                legend=dict(
                    title="Sources",
                    orientation="h",
                    yanchor="bottom",
                    y=0.95,
                    xanchor="center",
                    x=0.5
                ),
                xaxis=dict(range=[age_min, age_max]),
                yaxis=dict(range=[0, y_max]),
                margin=dict(t=100)
            )

    # Initialize widgets
    region_widget = widgets.Dropdown(
        options=regions,
        value=regions[0],
        description='Region'
    )

    gender_widget = widgets.Dropdown(
        options=['Male', 'Female', 'Both'],
        value='Both',
        description='Gender'
    )

    period_widget = widgets.Dropdown(
        options=periods,
        value="All periods",
        description='Period'
    )

    genres_widget = widgets.Dropdown(
        options=['All'],
        value='All',
        description='Genre'
    )

    def update_genres(*args):
        # Get the selected region
        selected_region = region_widget.value
        # Get the genres for the selected region
        selected_data = region_data[selected_region]['region_data']
        unique_genres = ['All'] + sorted(selected_data['main_genre'].dropna().unique())
        # Update the options of genres_widget
        genres_widget.options = unique_genres
        genres_widget.value = 'All'

    # Attach the update_genres function to changes in the region_widget
    region_widget.observe(update_genres, names='value')

    # Initialize genres
    update_genres()

    # Create the interactive plot
    def plot_age_distribution_widget(region, gender, period, genre):
        plot_age_distribution(region, gender, period, genre)

    interactive_plot = interactive(
        plot_age_distribution_widget,
        region=region_widget,
        gender=gender_widget,
        period=period_widget,
        genre=genres_widget
    )

    # Align widgets properly by using HBox and VBox
    widgets_box = VBox([HBox([region_widget, gender_widget]), HBox([period_widget, genres_widget])])

    # Display widgets on top, followed by the figure
    display(widgets_box)
    display(fig)
    # Save age distribution plot
    output_path = os.path.join(output_folder, "age_distribution.html")
    try:
        fig.write_html(output_path, full_html=True, include_plotlyjs='cdn')
        print(f"Plot saved successfully to: {output_path}")
    except Exception as e:
        print(f"Error saving plot: {str(e)}")


