""" 
Used functions for the european dataset 
A different functions file is used due to the complexity of the European dataset

"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import gaussian_kde
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from scipy.stats import chi2

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import statsmodels.api as sm

import statsmodels.formula.api as smf
import plotly.io as pio
import plotly.express as px
pio.renderers.default = "notebook"




######################################################################

def get_ethnicity_proportions(df, ethnicities):
    """
    Compute counts and percentages for specified ethnicities in the dataset.

    Args:
        df (pd.DataFrame): DataFrame with an 'actor_ethnicity_classification' column.
        ethnicities (list of str): List of ethnicities to calculate.

    Returns:
        tuple: 
            - counts_dict (dict): Counts for each ethnicity.
            - proportions_dict (dict): Percentages for each ethnicity.

    Notes:
        'Unknown' is excluded from calculations.
    """
    ethnicity_counts = df['actor_ethnicity_classification'].value_counts()

    # calculate the total number of people with an ethnicity
    total = sum(ethnicity_counts.get(ethnicity, 0) for ethnicity in ethnicities if ethnicity != 'Unknown')

    # Initialize dictionaries 
    counts_dict = {}
    proportions_dict = {}

    # Calculate counts and proportions 
    if total > 0:
        for ethnicity in ethnicities:
            if ethnicity != 'Unknown':
                count = ethnicity_counts.get(ethnicity, 0)
                proportion = (count / total) * 100
                counts_dict[ethnicity] = count
                proportions_dict[ethnicity] = proportion
    else:
        for ethnicity in ethnicities:
            if ethnicity != 'Unknown':
                counts_dict[ethnicity] = 0
                proportions_dict[ethnicity] = 0

    return counts_dict, proportions_dict

####################################################################

def ethnicity_comparison_plot(region_data, real_world_proportions, ethnicities, genre):
    """"
    Create a horizontal bar chart comparing ethnicity proportions in cinema (Europe) vs real-world data.

    Args:
        region_data (pd.DataFrame): Dataset containing ethnicity and genre information for the region.
        real_world_proportions (dict): Real-world ethnicity proportions as percentages.
        ethnicities (list of str): List of ethnicities to include in the comparison.
        genre (str): The genre to filter by (use "All Genres" for no filter).

    Returns:
        plotly.graph_objects.Figure: A bar chart showing the comparison.
    """
    # Filter out 'Unknown' ethnicities from the region data
    df_filtered = region_data[region_data['actor_ethnicity_classification'] != 'Unknown']

    # Get ethnicity proportions based on genre filter
    if genre == "All Genres":
        _, genre_prop = get_ethnicity_proportions(df_filtered, ethnicities)
    else:
        genre_df = df_filtered[df_filtered['main_genre'] == genre]  
        _, genre_prop = get_ethnicity_proportions(genre_df, ethnicities)

    # Scale factor to increase bar size for better visibility
    scale_factor = 100  

    fig = go.Figure()

    # Add bar for the cinema industry 
    fig.add_trace(
        go.Bar(
            y=ethnicities,
            x=[-genre_prop.get(eth, 0) * scale_factor for eth in ethnicities],  # Negative values for cinema industry
            name='Europe (Cinema Industry)',
            orientation='h',
            marker=dict(color='#7D3C98'),
            text=[f'{genre_prop.get(eth, 0):.1f}%' for eth in ethnicities],
            textposition='outside',
            hovertemplate='%{y}: %{text}'  
        )
    )

    # Add bar for real-world population data (always visible on positive axis)
    fig.add_trace(
        go.Bar(
            y=ethnicities,
            x=[real_world_proportions.get(eth, 0) * scale_factor for eth in ethnicities],
            name='Real-World Population',
            orientation='h',
            marker=dict(color='teal'),
            text=[f'{real_world_proportions.get(eth, 0):.2f}%' for eth in ethnicities],
            textposition='outside',
            hovertemplate='%{y}: %{text}'
        )
    )

    # Update layout 
    fig.update_layout(
        title_text="Comparison of Ethnicity Proportions in Europe vs Real-World Population",
        xaxis_title="← Cinema Industry | Real-world Population →",
        yaxis_title="Ethnicity Group",
        barmode='relative',
        template='plotly_white',
        height=600,
        width=1000
    )

    return fig


####################################################################



def chi_squared_ethnicity_test(region_data, ethnicities, real_world_proportions):
    """
    Perform a chi-squared test to compare observed ethnicity proportions in a dataset
    to real-world proportions.

    Parameters:
        region_data (DataFrame): The dataset containing ethnicity information.
        ethnicities (list): List of ethnicities to include in the comparison.
        real_world_proportions (dict): Real-world proportions of ethnicities (in percentages).

    Returns:
        dict: A dictionary containing chi-squared statistic, degrees of freedom, p-value,
              and a conclusion on whether the proportions are significantly different.
    """

    counts, _ = get_ethnicity_proportions(region_data, ethnicities)
    observed_counts = np.array([counts.get(ethnicity, 0) for ethnicity in ethnicities])

    total_count = sum(observed_counts)
    expected_counts = total_count * np.array([real_world_proportions.get(ethnicity, 0) / 100 for ethnicity in ethnicities])

    # Calculate chi-squared statistic
    chi_squared_stat = np.sum((observed_counts - expected_counts) ** 2 / expected_counts)

    # Degrees of freedom
    df = len(observed_counts) - 1

    # Calculate p-value
    p_value = 1 - chi2.cdf(chi_squared_stat, df)

    p_value_str = f"{p_value:.20f}"

    significant_difference = p_value <= 0.05
    conclusion = "The proportions are significantly different." if significant_difference else "The proportions are not significantly different."

    results = {
        "Chi-Squared Statistic": chi_squared_stat,
        "Degrees of Freedom": df,
        "P-Value": p_value_str,
        "Conclusion": conclusion
    }

    return results

####################################################################

def age_distribution_plot(europe_avg_male, europe_avg_female, europe_df, time_periods, period="All Periods", genre="All Genres"):
    """
    Generate a Plotly figure comparing age distributions between real-world populations and actors.

    Args:
        europe_avg_male (pd.DataFrame): Real-world male age distribution data.
        europe_avg_female (pd.DataFrame): Real-world female age distribution data.
        europe_df (pd.DataFrame): Actor data including age, gender, release year, and genre.
        time_periods (dict): Dictionary mapping period names to year ranges.
        period (str): Selected time period for filtering data.
        genre (str): Selected genre for filtering data.

    Returns:
        go.Figure: Plotly figure showing the age distribution comparison.
    """
    fig = go.Figure()

    # Exclude non-age columns
    age_columns = europe_avg_female.columns.drop('Time Period', errors='ignore')

    # Aggregate real-world population data
    def aggregate_real_data(df_real):
        if period == "All Periods":
            return df_real[age_columns].sum()
        else:
            filtered_df_real = df_real[df_real['Time Period'] == period]
            if filtered_df_real.empty:
                return None
            return filtered_df_real[age_columns].iloc[0]

    real_age_distribution_male = aggregate_real_data(europe_avg_male)
    real_age_distribution_female = aggregate_real_data(europe_avg_female)

    # Normalize the real-world age distributions
    def normalize_real_age_distribution(real_age_distribution):
        real_age_distribution = real_age_distribution / real_age_distribution.sum()
        real_age_distribution.index = (
            real_age_distribution.index.astype(str)
            .str.replace('+', '', regex=False)
            .astype(int)
        )
        return real_age_distribution[real_age_distribution.index >= 0]

    if real_age_distribution_male is not None:
        real_age_distribution_male = normalize_real_age_distribution(real_age_distribution_male)
    if real_age_distribution_female is not None:
        real_age_distribution_female = normalize_real_age_distribution(real_age_distribution_female)

    df_actors = europe_df.copy()
    df_actors['releas_ye'].dropna(inplace=True)

    # Filter by period
    if period != "All Periods":
        start_year, end_year = time_periods[period]
        df_actors = df_actors[df_actors['release_y'].between(start_year, end_year)]

    # Filter by genre
    if genre != "All Genres":
        df_actors = df_actors[df_actors['main_genre'].str.strip().str.lower() == genre.lower()]

    # Filter and process actor age data by gender
    actor_ages_male = df_actors[df_actors['actor_gender'] == 'M']['age_at_release'].dropna().astype(float)
    actor_ages_female = df_actors[df_actors['actor_gender'] == 'F']['age_at_release'].dropna().astype(float)
    actor_ages_male = actor_ages_male[actor_ages_male >= 0]
    actor_ages_female = actor_ages_female[actor_ages_female >= 0]

    # KDE for real-world population
    age_range = np.linspace(0, 100, 500)

    real_kde_male = gaussian_kde(real_age_distribution_male.index, weights=real_age_distribution_male.values)
    real_kde_female = gaussian_kde(real_age_distribution_female.index, weights=real_age_distribution_female.values)

    real_density_male = real_kde_male(age_range)
    real_density_female = real_kde_female(age_range)

    # Add real-world population traces
    fig.add_trace(
        go.Scatter(
            x=age_range, y=real_density_male, mode='lines', name='Real-world Population (Male)',
            line=dict(color='blue'), fill='tozeroy', fillcolor='rgba(0, 0, 255, 0.2)'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=age_range, y=real_density_female, mode='lines', name='Real-world Population (Female)',
            line=dict(color='red'), fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.2)'
        )
    )

    # KDE for actor data
    if len(actor_ages_male) > 1:
        actor_kde_male = gaussian_kde(actor_ages_male)
        actor_density_male = actor_kde_male(age_range)
    else:
        actor_density_male = np.zeros_like(age_range)

    if len(actor_ages_female) > 1:
        actor_kde_female = gaussian_kde(actor_ages_female)
        actor_density_female = actor_kde_female(age_range)
    else:
        actor_density_female = np.zeros_like(age_range)

    # Add actor traces
    fig.add_trace(
        go.Scatter(
            x=age_range, y=actor_density_male, mode='lines', name='Actors (Male)',
            line=dict(color='blue', dash='dot'), fill='tozeroy', fillcolor='rgba(0, 0, 255, 0.1)'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=age_range, y=actor_density_female, mode='lines', name='Actors (Female)',
            line=dict(color='red', dash='dot'), fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.1)'
        )
    )

    # Find peak ages
    peak_age_real_male = age_range[np.argmax(real_density_male)]
    peak_age_real_female = age_range[np.argmax(real_density_female)]
    peak_age_actor_male = age_range[np.argmax(actor_density_male)]
    peak_age_actor_female = age_range[np.argmax(actor_density_female)]

    # Add vertical lines for peak ages
    fig.add_trace(
        go.Scatter(
            x=[peak_age_real_male, peak_age_real_male], y=[0, max(real_density_male)],
            mode='lines', name='Peak Age (Real Male)',
            line=dict(color='blue')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[peak_age_real_female, peak_age_real_female], y=[0, max(real_density_female)],
            mode='lines', name='Peak Age (Real Female)',
            line=dict(color='red')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[peak_age_actor_male, peak_age_actor_male], y=[0, max(actor_density_male)],
            mode='lines', name='Peak Age (Actor Male)',
            line=dict(color='blue', dash='dot')
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[peak_age_actor_female, peak_age_actor_female], y=[0, max(actor_density_female)],
            mode='lines', name='Peak Age (Actor Female)',
            line=dict(color='red', dash='dot')
        )
    )

    # Update layout
    fig.update_layout(
        title=f'Age Distribution Comparison in Europe (Period: {period}, Genre: {genre})',
        height=800,
        width=1200,
        showlegend=True,
        legend_title_text='Sources',
        xaxis_title='Age',
        yaxis_title='Density'
    )

    return fig

#########################################################################

def gender_proportion_plot(df, europe_avg_male, europe_avg_female, genres):
    data = []
    periods_bins = ["1950-1965", "1966-1980", "1981-1995", "1996-2012"]

    # Process Real-World Data
    real_world_male = europe_avg_male.set_index("Time Period").mean(axis=1)
    real_world_female = europe_avg_female.set_index("Time Period").mean(axis=1)
    real_world_male_std = europe_avg_male.set_index("Time Period").std(axis=1)
    real_world_female_std = europe_avg_female.set_index("Time Period").std(axis=1)

    for genre in genres:
        if genre != 'All Genres':
            # Process actor data
            actor_male_ages, actor_male_std = calculate_actor_ages(df, "M", genre=genre)
            actor_female_ages, actor_female_std = calculate_actor_ages(df, "F", genre=genre)

            for i, period in enumerate(periods_bins):
                data.append({
                    "Period": period,
                    "Genre": genre,
                    "Group": "Real-World Male",
                    "Average Age": real_world_male.values[i] if i < len(real_world_male.values) else None,
                    "Std": real_world_male_std.values[i] if i < len(real_world_male_std.values) else None
                })
                data.append({
                    "Period": period,
                    "Genre": genre,
                    "Group": "Real-World Female",
                    "Average Age": real_world_female.values[i] if i < len(real_world_female.values) else None,
                    "Std": real_world_female_std.values[i] if i < len(real_world_female_std.values) else None
                })
                data.append({
                    "Period": period,
                    "Genre": genre,
                    "Group": "Actor Male",
                    "Average Age": actor_male_ages.values[i] if i < len(actor_male_ages.values) else None,
                    "Std": actor_male_std.values[i] if i < len(actor_male_std.values) else None
                })
                data.append({
                    "Period": period,
                    "Genre": genre,
                    "Group": "Actor Female",
                    "Average Age": actor_female_ages.values[i] if i < len(actor_female_ages.values) else None,
                    "Std": actor_female_std.values[i] if i < len(actor_female_std.values) else None
                })

    return pd.DataFrame(data)

###########################################################################

def calculate_actor_ages(df, gender, genre=None):
    # Filter by genre
    if genre and genre != "All Genres":
        df = df[df['main_genre'] == genre]

    df_filtered = df[df['actor_gender'] == gender]

    # Group data 
    df_grouped = df_filtered.groupby(
        pd.cut(
            df_filtered['release_y'], 
            bins=[1950, 1965, 1980, 1995, 2012], 
            labels=["1950-1965", "1966-1980", "1981-1995", "1996-2012"]
        ),
        observed=False 
    )

    avg_ages = df_grouped['age_at_release'].mean()
    std_ages = df_grouped['age_at_release'].std()
    return avg_ages, std_ages

#########################################################

def gender_OLS(df, output_html="ols_summary.html", output_md="ols_summary.md", plot_html="gender_ols_plot.html"):
    # Filter to take only years above 1950
    df = df[df['release_y'] >= 1950]

    # Group by year and count gender per year
    gender_counts = df.groupby(['release_y', 'actor_gender']).size().unstack(fill_value=0).reset_index()

    # Calculate proportion per year
    gender_counts['total'] = gender_counts['M'] + gender_counts['F']
    gender_counts['female_prop'] = gender_counts['F'] / gender_counts['total']

    # Fit OLS
    model = smf.ols(formula="female_prop ~ release_y", data=gender_counts).fit()

    # Save summary to Markdown
    with open("gender_ols_summary.md", "w") as f:
        f.write(model.summary().as_text())
    print(f"OLS summary saved as Markdown: gender_ols_summary.md")
    print(model.summary())

    # Predict values
    gender_counts['predicted_prop'] = model.predict(gender_counts)

    # Create an interactive plot with Plotly
    fig = px.scatter(
        gender_counts, 
        x='release_y', 
        y='female_prop', 
        title='Gender Ratio Over Time in European Cinema',
        labels={'release_y': 'Year of Release', 'female_prop': 'Proportion of Female Actors'},
        color_discrete_sequence=['#009392'],
        hover_data={'release_y': True, 'female_prop': True}
    )

    # Add the trend line
    fig.add_scatter(
        x=gender_counts['release_y'],
        y=gender_counts['predicted_prop'],
        mode='lines',
        name='Trend Line (OLS Regression)',
        line=dict(color='#9e2f7f', width=3)
    )

    fig.update_layout(
        width=800,  
        height=450, 
        plot_bgcolor="#f6f0f0", 
        paper_bgcolor="#f6f0f0", 
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.1,             
        )
    )

    fig.show()

    # Save the interactive plot to an HTML file
    pio.write_html(fig, file=plot_html, auto_open=False)
    print(f"Interactive plot saved as HTML: {plot_html}")

    # Print regression coefficients
    print(f"Linear Regression Coefficients:")
    print(f"Intercept: {model.params['Intercept']}")
    print(f"Year Coefficient: {model.params['release_y']}")

###############################################################

def radar_chart_plot(df, ethnicities, output_file="radar_chart.html"):
    # Filter to exclude 'Unknown' ethnicities
    df_filtered = df[df['actor_ethnicity_classification'] != 'Unknown']

    # Calculate proportions
    proportions = {'Male': [], 'Female': []}
    for ethnicity in ethnicities:
        df_ethnicity = df_filtered[df_filtered['actor_ethnicity_classification'] == ethnicity]
        male_count = len(df_ethnicity[df_ethnicity['actor_gender'] == 'M'])
        female_count = len(df_ethnicity[df_ethnicity['actor_gender'] == 'F'])
        total = male_count + female_count
        if total > 0:
            proportions['Male'].append(male_count / total * 100)
            proportions['Female'].append(female_count / total * 100)
        else:
            proportions['Male'].append(0)
            proportions['Female'].append(0)

    fig = go.Figure()

    # Add traces for male and female proportions
    fig.add_trace(go.Scatterpolar(
        r=proportions['Male'],
        theta=ethnicities,
        fill='toself',
        name='Male Proportion',
        marker=dict(color='#009392')
    ))

    fig.add_trace(go.Scatterpolar(
        r=proportions['Female'],
        theta=ethnicities,
        fill='toself',
        name='Female Proportion',
        marker=dict(color='#7c1d6f')
    ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title="Gender Proportions Across Ethnicities",
        showlegend=True,
        width=500,
        height=400,
        paper_bgcolor="#f6f0f0",
        plot_bgcolor="#f6f0f0"
    )

    fig.show()

    pio.write_html(fig, file=output_file, auto_open=False)
    print(f"Radar chart saved to {output_file}")    

###########################################################

# Function to calculate gender proportions for each genre and time period
def calculate_gender_proportions(df, time_periods, genres):
    gender_proportions = {}

    for period_name, (start_year, end_year) in time_periods.items():
        df_period = df[df['release_y'].between(start_year, end_year)]
        gender_proportions[period_name] = {}

        for genre in genres:
            if genre == "All Genres":
                df_genre = df_period
            else:
                df_genre = df_period[df_period['main_genre'] == genre]

            male_count = len(df_genre[df_genre['actor_gender'] == 'M'])
            female_count = len(df_genre[df_genre['actor_gender'] == 'F'])
            total_count = male_count + female_count

            if total_count > 0:
                male_proportion = male_count / total_count
                female_proportion = female_count / total_count
            else:
                male_proportion = 0
                female_proportion = 0

            gender_proportions[period_name][genre] = {
                'Male': male_proportion,
                'Female': female_proportion
            }

    return gender_proportions

###################################################################

# Function to get real-world gender proportions
def get_real_world_gender_proportions(europe_avg_male, europe_avg_female, period):
    if period == "All Periods":
        male_total = europe_avg_male.iloc[:, 1:].sum().sum()
        female_total = europe_avg_female.iloc[:, 1:].sum().sum()
    else:
        male_total = europe_avg_male[europe_avg_male['Time Period'] == period].iloc[:, 1:].sum().sum()
        female_total = europe_avg_female[europe_avg_female['Time Period'] == period].iloc[:, 1:].sum().sum()

    total = male_total + female_total
    if total == 0:
        return 0.5, 0.5
    return male_total / total, female_total / total

###################################################################

# Function to plot gender proportions with four subplots for each region
def gender_prop_subplots(df, period, genres, time_periods, europe_avg_male, europe_avg_female):
    fig = go.Figure()


    gender_proportions = calculate_gender_proportions(df, time_periods, genres)

    # Plot gender proportions for movies by genre
    for genre in genres:
        if genre != 'All Genres':
            male_prop = gender_proportions[period].get(genre, {}).get('Male', 0)
            female_prop = gender_proportions[period].get(genre, {}).get('Female', 0)

            fig.add_trace(
                go.Bar(
                    x=[genre],
                    y=[male_prop],
                    name='Male',
                    marker=dict(color='teal'),
                    hovertemplate=f"Male: {male_prop*100:.1f}%<extra></extra>",
                    legendgroup='Male Actors',
                    showlegend=True if genre=='All Genres' else False
                ),
            )

            fig.add_trace(
                go.Bar(
                    x=[genre],
                    y=[female_prop],
                    name='Female',
                    marker=dict(color='purple'),
                    base=[male_prop],
                    hovertemplate=f"Female: {female_prop*100:.1f}%<extra></extra>",
                    legendgroup='Female Actors',
                    showlegend=True if genre=='All Genres' else False
                ),
            )

    # Plot real-world gender proportions as the last bin 
    male_real_world, female_real_world = get_real_world_gender_proportions(europe_avg_male, europe_avg_female, period)

    fig.add_trace(
        go.Bar(
            x=['Real World'],
            y=[male_real_world],
            name='Male',
            marker=dict(color='teal', pattern=dict(shape='x')),
            hovertemplate=f"Male: {male_real_world*100:.1f}%<extra></extra>",
            legendgroup='Male Population',
            showlegend=True if genre=='All Genres' else False
        ),
    )

    fig.add_trace(
        go.Bar(
            x=['Real World'],
            y=[female_real_world],
            name='Female',
            marker=dict(color='purple', pattern=dict(shape='x')),
            base=[male_real_world],
            hovertemplate=f"Female: {female_real_world*100:.1f}%<extra></extra>",
            legendgroup='Female Population',
            showlegend=True if genre=='All Genres' else False
        ),
    )

    # Update layout
    fig.update_layout(
        title_text=f"Gender Proportions by Genre & Real-world Population (Period: {period})",
        barmode='stack',
        template='plotly_white',
        height=800,
        width=1200,
        xaxis_tickangle=-25,
        legend=dict(
            title="Gender",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    return fig
