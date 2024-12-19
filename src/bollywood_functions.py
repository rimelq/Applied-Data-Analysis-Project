import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

DATA_FOLDER = './data/final/'

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

# Charging the Bollywood datasets in their respective dataframes
bollywood_data, bollywood_data_ethnicity, bollywood_ethnic_realworld, \
male_bollywood_realworld_averages, female_bollywood_realworld_averages, \
bothsexes_bollywood_realworld_averages, male_bollywood_realworld_proportions, \
female_bollywood_realworld_proportions = var_loader(DATA_FOLDER, mode="bollywood")


def process_and_plot_ethnicity_revenue(data, output_file):
    """
    Process the data and plot the average box office revenue by majority ethnicity of actors.

    Parameters:
        data (DataFrame): Input DataFrame containing the movie and ethnicity data.
        output_file (str): Path to save the output HTML file of the plot.
    """

    # Calculate the majority ethnicity for each movie
    def get_majority_ethnicity(series):
        filtered_series = series[series != 'Unknown']
        return filtered_series.value_counts().idxmax() if not filtered_series.empty else 'Unknown'

    data['actor_ethnicity_classification'] = data['actor_ethnicity_classification'].fillna('Unknown')
    data['majority_ethnicity'] = data.groupby('wiki_movie_id')['actor_ethnicity_classification'].transform(get_majority_ethnicity)

    # Filter out movies with 'Unknown' majority ethnicity
    filtered_data = data[data['majority_ethnicity'] != 'Unknown']
    filtered_data.reset_index(drop=True, inplace=True)

    # Extract unique rows for movies
    movies_majority_ethnicity = filtered_data[['wiki_movie_id', 'majority_ethnicity', 'box_office']].drop_duplicates()

    # Calculate the average box office revenue for each majority ethnicity
    average_revenue_by_ethnicity = movies_majority_ethnicity.groupby('majority_ethnicity')['box_office'].mean().reset_index()
    average_revenue_by_ethnicity.columns = ['Ethnicity', 'Average Box Office Revenue']
    average_revenue_by_ethnicity = average_revenue_by_ethnicity.sort_values(by='Average Box Office Revenue', ascending=False).reset_index(drop=True)

    # Plot the results
    fig = px.bar(
        average_revenue_by_ethnicity,
        x='Average Box Office Revenue',
        y='Ethnicity',
        orientation='h',
        title="<b>Average Box Office Revenue by Majority Ethnicity</b><br><span style='font-size:14px;'>(Period: 1950–2012)</span>",
        labels={'Average Box Office Revenue': 'Average Box Office Revenue ($)', 'Ethnicity': 'Majority Ethnicity'},
        text='Average Box Office Revenue',
        color_discrete_sequence=["#7c1d6f"]  
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis=dict(
            range=[1.76e7, 1.78e7],  # Keep the scale as requested
            title="Average Box Office Revenue ($)"
        ),
        yaxis=dict(
            title="Majority Ethnicity"
        ),
        title=dict(
            font=dict(size=18, color='black')
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  # Background color
        paper_bgcolor="#F2F0F0",  # Paper background color
        font=dict(color="black"),  # Font color for labels
        margin=dict(t=100),  
    )

    # Show the figure
    fig.show()

    # Save the figure as an HTML file
    fig.write_html(output_file)
    print(f"Figure saved as {output_file}")

def process_and_plot_gender_dominance(data, output_file):
    """
    Analyze gender proportions in movies, label them as male-dominated, female-dominated, or balanced,
    and plot the results with custom colors and layout.

    Parameters:
        data (DataFrame): Input DataFrame containing 'wiki_movie_id' and 'actor_gender'.
        output_file (str): Path to save the output HTML file of the plot.
    """
    # Calculate gender proportions for each movie
    def calculate_gender_proportions(df):
        df = df.dropna(subset=['actor_gender'])  # Drop rows with NaN actor_gender
        gender_counts = df.groupby('wiki_movie_id')['actor_gender'].value_counts(normalize=True).unstack(fill_value=0)
        return gender_counts

    gender_proportions = calculate_gender_proportions(data)

    # Drop movies with no valid gender proportions
    filtered_data = data[data['wiki_movie_id'].isin(gender_proportions.index)].copy()

    # Label movies based on gender proportions
    def label_gender_dominance(row):
        if row.get('F', 0) >= 0.5:
            return 'Female-Dominated'
        elif row.get('M', 0) >= 0.5:
            return 'Male-Dominated'
        else:
            return 'Balanced'

    gender_proportions['Gender Dominance'] = gender_proportions.apply(label_gender_dominance, axis=1)

    # Merge gender dominance labels back to the main data
    filtered_data = filtered_data.merge(
        gender_proportions[['Gender Dominance']],
        left_on='wiki_movie_id',
        right_index=True,
        how='left'
    )

    #Count gender dominance categories
    dominance_counts = gender_proportions['Gender Dominance'].value_counts().reset_index()
    dominance_counts.columns = ['Gender Dominance', 'Number of Movies']

    fig = px.bar(
        dominance_counts,
        x='Gender Dominance',
        y='Number of Movies',
        color='Gender Dominance',
        text='Number of Movies',
        color_discrete_map={
            'Male-Dominated': '#7c1d6f', 
            'Female-Dominated': '#eeb479',
            'Balanced': '#cccccc'          
        },
        title="<b>Number of Male-Dominated vs Female-Dominated Movies</b><br><span style='font-size:14px;'>Representation of Gender Dominance</span>",
    )

    
    fig.update_traces(
        textposition='outside',
        marker_line_color='black',
        marker_line_width=1.5
    )

    fig.update_layout(
        title=dict(
            font=dict(size=18, color='black'),
            x=0.5,  # Center align
            xanchor='center'
        ),
        xaxis=dict(
            title="Gender Dominance",
            titlefont=dict(size=12, color="black"),
            tickangle=0
        ),
        yaxis=dict(
            title="Number of Movies",
            titlefont=dict(size=12, color="black")
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  
        paper_bgcolor="#F2F0F0",  
        font=dict(color="black"),
        margin=dict(t=100, l=50, r=50, b=50), 
    )

    # Show the plot
    fig.show()

    # Save the figure as an HTML file
    fig.write_html(output_file)
    print(f"Figure saved as {output_file}")


def process_and_plot_average_revenue_by_gender(data, output_file):
    """
    Calculate and plot the average box office revenue for each gender dominance category.

    Parameters:
        data (DataFrame): Input DataFrame containing 'Gender Dominance' and 'box_office' columns.
        output_file (str): Path to save the output HTML file of the plot.
    """
    def calculate_gender_proportions(df):
            df = df.dropna(subset=['actor_gender'])  # Drop rows with NaN actor_gender
            gender_counts = df.groupby('wiki_movie_id')['actor_gender'].value_counts(normalize=True).unstack(fill_value=0)
            return gender_counts

    def label_gender_dominance(row):
            if row.get('F', 0) >= 0.5:
                return 'Female-Dominated'
            elif row.get('M', 0) >= 0.5:
                return 'Male-Dominated'
            else:
                return 'Balanced'

    gender_proportions = calculate_gender_proportions(data)
    gender_proportions['Gender Dominance'] = gender_proportions.apply(label_gender_dominance, axis=1)

    # Merge 'Gender Dominance' back into the main dataset
    data = data.merge(
            gender_proportions[['Gender Dominance']],
            left_on='wiki_movie_id',
            right_index=True,
            how='left'
        )
    
    # Calculate average box office revenue for each gender dominance category
    average_revenue_by_gender = data.groupby('Gender Dominance')['box_office'].mean().reset_index()
    average_revenue_by_gender.columns = ['Gender Dominance', 'Average Box Office Revenue']
    average_revenue_by_gender = average_revenue_by_gender.sort_values(by='Average Box Office Revenue', ascending=False).reset_index(drop=True)

    # Plot the results
    fig = px.bar(
        average_revenue_by_gender,
        x='Average Box Office Revenue',
        y='Gender Dominance',
        orientation='h',
        title="<b>Average Box Office Revenue by Dominating Gender in Movie</b><br><span style='font-size:14px;'>(Representation of Gender Dominance)</span>",
        labels={
            'Average Box Office Revenue': 'Average Box Office Revenue ($)',
            'Gender Dominance': 'Gender Dominance'
        },
        text='Average Box Office Revenue',
        color_discrete_sequence=['#7c1d6f']  # Bar color
    )

    # Adjust layout for styling and background
    fig.update_traces(
        texttemplate='%{text:.2s}',  # Format numbers as shortened (e.g., 1.78M)
        textposition='outside',
        marker_line_color='black',  # Add black border around bars
        marker_line_width=1.5
    )

    fig.update_layout(
        title=dict(
            font=dict(size=18, color='black'),
            x=0.5,  # Center align title
            xanchor='center'
        ),
        xaxis=dict(
            range=[1.76e7, 1.78e7], 
            title="Average Box Office Revenue ($)",
            titlefont=dict(size=12, color="black")
        ),
        yaxis=dict(
            title="Gender Dominance",
            titlefont=dict(size=12, color="black")
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  # Light gray plot background
        paper_bgcolor="#F2F0F0",  # Light gray canvas background
        font=dict(color="black"),  # Black text for labels
        margin=dict(t=100, l=50, r=50, b=50),  
        showlegend=False 
    )

    fig.show()

    # Save the plot as an HTML file
    fig.write_html(output_file)
    print(f"Figure saved as {output_file}")

def process_and_plot_female_actor_trend(data, output_file):
    """
    Analyze and plot the trend of female actors in movies over the years.

    Parameters:
        data (DataFrame): Input DataFrame containing 'actor_gender' and 'release_y' columns.
        output_file (str): Path to save the output HTML file of the plot.
    """

    # Remove rows with NaN values in 'actor_gender' or 'release_y'
    valid_data = data.dropna(subset=['actor_gender', 'release_y'])

    # Count the number of female actors per year
    female_actor_counts = valid_data[valid_data['actor_gender'] == 'F'] \
        .groupby('release_y') \
        .size() \
        .reset_index(name='Female Actor Count')

    # Create the line plot
    fig = px.line(
        female_actor_counts,
        x='release_y',
        y='Female Actor Count',
        title="<b>Trend of Female Actors in Indian Movies Over the Years</b>",
        labels={'release_y': 'Year', 'Female Actor Count': 'Count of Female Actors'},
        markers=True,
        line_shape='linear',
        color_discrete_sequence=['#eeb479']  # Line color
    )

    fig.update_traces(
        line=dict(width=2),  # Set line width
        marker=dict(size=5, color='#eeb479') 
    )

    fig.update_layout(
        title=dict(
            font=dict(size=18, color='black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            tickmode='linear',
            tick0=1900,  # Start tick interval from 1900
            dtick=10,  # Interval for ticks (every 10 years)
            titlefont=dict(size=12, color='black')
        ),
        yaxis=dict(
            title="Count of Female Actors",
            titlefont=dict(size=12, color='black')
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  # Light gray background
        paper_bgcolor="#F2F0F0",  # Light gray canvas
        font=dict(color="black"),  # Black text
        margin=dict(t=100, l=50, r=50, b=50)  # Adjust margins
    )

    fig.show()

    # Save the figure as an HTML file
    fig.write_html(output_file)
    print(f"Figure saved as {output_file}")


def process_and_plot_male_actor_trend(data, output_file):
    """
    Analyze and plot the trend of male actors in movies over the years.

    Parameters:
        data (DataFrame): Input DataFrame containing 'actor_gender' and 'release_y' columns.
        output_file (str): Path to save the output HTML file of the plot.
    """

    # Remove rows with NaN values in 'actor_gender' or 'release_y'
    valid_data = data.dropna(subset=['actor_gender', 'release_y'])

    # Count the number of male actors per year
    male_actor_counts = valid_data[valid_data['actor_gender'] == 'M'] \
        .groupby('release_y') \
        .size() \
        .reset_index(name='Male Actor Count')

    fig = px.line(
        male_actor_counts,
        x='release_y',
        y='Male Actor Count',
        title="<b>Trend of Male Actors in Indian Movies Over the Years</b><br><span style='font-size:14px;'>(Representation Across Decades)</span>",
        labels={'release_y': 'Year', 'Male Actor Count': 'Count of Male Actors'},
        markers=True,
        line_shape='linear',
        color_discrete_sequence=['#7c1d6f']  # Line color (dark purple)
    )

    # Update marker styling: 
    fig.update_traces(
        line=dict(width=2),  
        marker=dict(size=5, color='#7c1d6f')  
    )

    # Update layout and styling
    fig.update_layout(
        title=dict(
            font=dict(size=18, color='black'),
            x=0.5,  # Center align title
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            tickmode='linear',
            tick0=1900,  # Start tick interval from 1900
            dtick=10,  # Interval for ticks (every 10 years)
            titlefont=dict(size=12, color='black')
        ),
        yaxis=dict(
            title="Count of Male Actors",
            titlefont=dict(size=12, color='black')
        ),
        template="plotly_white",
        plot_bgcolor="#F2F0F0",  # Light gray background
        paper_bgcolor="#F2F0F0",  # Light gray canvas
        font=dict(color="black"),  # Black text
        margin=dict(t=100, l=50, r=50, b=50)  # Adjust margins
    )

    fig.show()

    # Save the figure as an HTML file
    fig.write_html(output_file)
    print(f"Figure saved as {output_file}")


def save_actor_counts_for_flourish(male_actor_counts, female_actor_counts, output_file):
    """
    Merge male and female actor counts, transpose the data for Flourish, and save it as a CSV file.

    Parameters:
        male_actor_counts (DataFrame): DataFrame containing 'release_y' and 'Male Actor Count'.
        female_actor_counts (DataFrame): DataFrame containing 'release_y' and 'Female Actor Count'.
        output_file (str): Path to save the transposed data as a CSV file.
    """

    # Merge male and female actor counts on 'release_y'
    actor_counts = male_actor_counts.merge(female_actor_counts, on="release_y", how="inner")

    #Transpose the DataFrame
    flipped_df = actor_counts.T

    # Reset the index to make the years as a column
    flipped_df = flipped_df.reset_index()

    # Rename the columns
    flipped_df = flipped_df.rename(columns={'index': 'Year'})

    # Save the DataFrame as a CSV file
    flipped_df.to_csv(output_file, index=False)
    print(f"Actor counts data saved as '{output_file}'")

    return flipped_df  
