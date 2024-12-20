##############################################
#                                            #
#  Reliability Score Analysis Python Script  #
#                                            #
##############################################


import pandas as pd
import plotly.express as px
import numpy as np


# FUNCTIONS--------------------------------:


def plot_dataset_distribution_across_regions(movie_metadata, 
                                             output_html_file = "dataset_distribution_across_regions.html", 
                                             output_csv_file = "dataset_distribution_across_regions.csv"):
    """
    Calculate and plot the dataset distribution across regions.
    """

    # Define region-country mappings
    hollywood_region = ['United States of America', 'Canada']
    indian_region = ['India']
    east_asian_region = ['China', 'Japan', 'Mongolia', 'Hong Kong', 'South Korea', 'Taiwan']
    european_region = ['Slovakia', 'Estonia', 'Bulgaria', 'Scotland', 'England', 'Slovak Republic', 
                      'Luxembourg', 'Netherlands', 'Ukraine', 'Monaco', 'Switzerland', 'Italy',
                      'Kingdom of Great Britain', 'Isle of Man', 'Northern Ireland', 'Ireland',
                      'Sweden', 'Albania', 'France', 'Poland', 'Slovenia', 'Romania', 'Serbia',
                      'Croatia', 'United Kingdom', 'Republic of Macedonia', 'Denmark', 
                      'Czech Republic', 'Austria', 'Spain', 'Russia', 'Bosnia and Herzegovina', 
                      'Czechoslovakia', 'Portugal', 'Iceland', 'Yugoslavia', 'Malta', 'Wales', 
                      'Georgia', 'Cyprus', 'Lithuania', 'Greece', 'Belgium', 'Hungary', 'Germany', 
                      'Norway', 'Finland', 'Montenegro']

    # Helper function to calculate dataset ratio
    def calculate_dataset_ratio(movie_metadata, countries):
        """
        Calculate the ratio of movies for a specific list of countries to the total dataset.
        """
        total_movies = len(movie_metadata)
        tot_num_country_movies = 0

        for country in countries:
            country_movies = movie_metadata[movie_metadata['Movie countries'].str.contains(country, na=False, case=False)]
            tot_num_country_movies += len(country_movies)
        
        return (tot_num_country_movies / total_movies) * 100 if total_movies > 0 else 0

    # Calculate ratios for regions
    india_data_ratio = calculate_dataset_ratio(movie_metadata, indian_region)
    east_asian_data_ratio = calculate_dataset_ratio(movie_metadata, east_asian_region)
    european_data_ratio = calculate_dataset_ratio(movie_metadata, european_region)
    hollywood_data_ratio = calculate_dataset_ratio(movie_metadata, hollywood_region)

    # Compile ratios into a dictionary
    ratios = {
        "India": india_data_ratio,
        "East Asia": east_asian_data_ratio,
        "Europe": european_data_ratio,
        "Hollywood": hollywood_data_ratio
    }

    # Calculate the "Other" percentage
    remaining_percentage = 100 - sum(ratios.values())
    ratios["Other"] = remaining_percentage

    # Create a DataFrame from ratios
    df_ratios = pd.DataFrame(list(ratios.items()), columns=["Region", "Data Percentage"])

    # Plot a pie chart
    fig = px.pie(
        df_ratios, 
        values="Data Percentage", 
        names="Region", 
        title="<b>Dataset Distribution Across Regions</b><br><span style='font-size:14px;'>Based on Movie Metadata</span>",
        color_discrete_sequence=["#7c1d6f", "#FF8C00", "#4682B4", "#32CD32", "#A9A9A9"]  # Custom color palette
    )

    fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0, 0, 0, 0.05])
    fig.update_layout(
        template="plotly_white",
        font=dict(color="black"),
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0"
    )

    # Show the figure
    fig.show()
    
    # Save the figure as an HTML file
    fig.write_html(output_html_file)
    print(f"Figure saved as {output_html_file}")
    
    # Save the resulting DataFrame to a CSV for later use
    df_ratios.to_csv(output_csv_file, index=False)


######################################################################


def calculate_missing_data_percentage(movie_metadata, output_html_file = "missing_data_across_regions.html", 
                                      output_csv_file = "missing_data_across_regions.csv"):
    """
    Calculate the percentage of missing data (NaNs) for each region and plot the results.
    """
    
    # Define region-country mappings
    hollywood_region = ['United States of America', 'Canada']
    indian_region = ['India']
    east_asian_region = ['China', 'Japan', 'Mongolia', 'Hong Kong', 'South Korea', 'Taiwan']
    european_region = ['Slovakia', 'Estonia', 'Bulgaria', 'Scotland', 'England', 'Slovak Republic', 
                       'Luxembourg', 'Netherlands', 'Ukraine', 'Monaco', 'Switzerland', 'Italy',
                       'Kingdom of Great Britain', 'Isle of Man', 'Northern Ireland', 'Ireland',
                       'Sweden', 'Albania', 'France', 'Poland', 'Slovenia', 'Romania', 'Serbia',
                       'Croatia', 'United Kingdom', 'Republic of Macedonia', 'Denmark', 
                       'Czech Republic', 'Austria', 'Spain', 'Russia', 'Bosnia and Herzegovina', 
                       'Czechoslovakia', 'Portugal', 'Iceland', 'Yugoslavia', 'Malta', 'Wales', 
                       'Georgia', 'Cyprus', 'Lithuania', 'Greece', 'Belgium', 'Hungary', 'Germany', 
                       'Norway', 'Finland', 'Montenegro']
    
    regions = {
        "Hollywood": hollywood_region,
        "India": indian_region,
        "East Asia": east_asian_region,
        "Europe": european_region
    }
    
    missing_data_percentages = {}
    
    # Helper function to calculate missing percentage
    def calculate_region_missing_percentage(region_countries):
        sub_data = movie_metadata[movie_metadata['Movie countries'].apply(
            lambda x: any(country in x for country in region_countries) if pd.notnull(x) else False
        )]
        
        total_elements = sub_data.size  
        total_missing = sub_data.isna().sum().sum()  
        return (total_missing / total_elements) * 100 if total_elements > 0 else 0

    # Calculate for each region
    for region_name, countries in regions.items():
        missing_percentage = calculate_region_missing_percentage(countries)
        missing_data_percentages[region_name] = missing_percentage
    
    # Convert to DataFrame and save as CSV
    df_missing = pd.DataFrame(list(missing_data_percentages.items()), columns=["Region", "Percentage of Missing Data"])
    df_missing = df_missing.sort_values(by="Percentage of Missing Data", ascending=False).reset_index(drop=True)
    
    # Plot the results
    fig = px.bar(
        df_missing,
        x="Percentage of Missing Data",
        y="Region",
        orientation='h',
        title="<b>Percentage of Missing Data Across Regions</b><br><span style='font-size:14px;'>Based on Movie Metadata</span>",
        labels={"Percentage of Missing Data": "Missing Data (%)", "Region": "Region"},
        color="Percentage of Missing Data",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        template="plotly_white",
        font=dict(color="black"),
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0"
    )
    fig.show()
    
    # Save the figure as an HTML file
    fig.write_html(output_html_file)
    print(f"Figure saved as {output_html_file}")
        
    # Save the resulting DataFrame to a CSV for later use
    df_missing.to_csv(output_csv_file, index=False)
    

######################################################################

    
def calculate_temporal_coverage(movie_metadata, output_html_file = "temporal_coverage_across_regions.html", 
                                output_csv_file = "temporal_coverage_across_regions.csv") :
    """
    Calculate the temporal coverage percentage of movies for each region.
    """
    
    # Define region-country mappings
    hollywood_region = ['United States of America', 'Canada']
    indian_region = ['India']
    east_asian_region = ['China', 'Japan', 'Mongolia', 'Hong Kong', 'South Korea', 'Taiwan']
    european_region = ['Slovakia', 'Estonia', 'Bulgaria', 'Scotland', 'England', 'Slovak Republic', 
                       'Luxembourg', 'Netherlands', 'Ukraine', 'Monaco', 'Switzerland', 'Italy',
                       'Kingdom of Great Britain', 'Isle of Man', 'Northern Ireland', 'Ireland',
                       'Sweden', 'Albania', 'France', 'Poland', 'Slovenia', 'Romania', 'Serbia',
                       'Croatia', 'United Kingdom', 'Republic of Macedonia', 'Denmark', 
                       'Czech Republic', 'Austria', 'Spain', 'Russia', 'Bosnia and Herzegovina', 
                       'Czechoslovakia', 'Portugal', 'Iceland', 'Yugoslavia', 'Malta', 'Wales', 
                       'Georgia', 'Cyprus', 'Lithuania', 'Greece', 'Belgium', 'Hungary', 'Germany', 
                       'Norway', 'Finland', 'Montenegro']
    
    regions = {
        "Hollywood": hollywood_region,
        "India": indian_region,
        "East Asia": east_asian_region,
        "Europe": european_region
    }

    # Clean the "Movie release date" column to extract years
    movie_metadata['release_year'] = movie_metadata['Movie release date'].apply(
        lambda x: pd.to_datetime(str(x), errors='coerce').year if pd.notnull(x) else None
    )

    movie_metadata = movie_metadata.dropna(subset=['release_year'])
    
    # Calculate total unique years in the full dataset
    total_years = movie_metadata['release_year'].nunique()

    # Dictionary to store temporal coverage percentages
    temporal_coverage = {}

    # Helper function to calculate temporal coverage percentage
    def calculate_region_temporal_coverage(region_countries):
        sub_data = movie_metadata[movie_metadata['Movie countries'].apply(
            lambda x: any(country in x for country in region_countries) if pd.notnull(x) else False
        )]
        unique_years_subdata = sub_data['release_year'].nunique()
        return (unique_years_subdata / total_years) * 100 if total_years > 0 else 0

    # Calculate for each region
    for region_name, countries in regions.items():
        coverage_percentage = calculate_region_temporal_coverage(countries)
        temporal_coverage[region_name] = coverage_percentage

    # Convert to DataFrame and save as CSV
    df_temporal_coverage = pd.DataFrame(list(temporal_coverage.items()), columns=["Region", "Temporal Coverage (%)"])
    df_temporal_coverage = df_temporal_coverage.sort_values(by="Temporal Coverage (%)", ascending=False).reset_index(drop=True)

    # Plot the results
    fig = px.bar(
        df_temporal_coverage,
        x="Temporal Coverage (%)",
        y="Region",
        orientation='h',
        title="<b>Temporal Coverage Across Regions</b><br><span style='font-size:14px;'>Based on Movie Metadata</span>",
        labels={"Temporal Coverage (%)": "Coverage Percentage", "Region": "Region"},
        color="Temporal Coverage (%)",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        template="plotly_white",
        font=dict(color="black"),
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0"
    )
    fig.show()
    
    # Save the figure as an HTML file
    fig.write_html(output_html_file)
    print(f"Figure saved as {output_html_file}")
    
    # Save the resulting DataFrame to a CSV for later use
    df_temporal_coverage.to_csv(output_csv_file, index=False)

    
def calculate_reliability_score(dataset_size_df, missing_data_df, temporal_coverage_df, 
                                output_html_file = "reliability_scores_across_regions.html", 
                                output_csv_file = "reliability_scores_across_regions.csv"):
    """
    Calculate the reliability scores for regions using Dataset Size, Missing Data, and Temporal Coverage.
    """

    # Merge all dataframes on the 'Region' column
    merged_df = dataset_size_df.merge(missing_data_df, on="Region").merge(temporal_coverage_df, on="Region")

    # Rename columns for clarity
    merged_df.rename(columns={
        'Data Percentage': 'Dataset_Size',
        'Percentage of Missing Data': 'Missing_Data',
        'Temporal Coverage (%)': 'Temporal_Coverage'
    }, inplace=True)

    # Normalize the Dataset Size and Temporal Coverage to [0, 1] 
    merged_df['Dataset_Size'] = merged_df['Dataset_Size'] / 100  
    merged_df['Missing_Data'] = merged_df['Missing_Data'] / 100  
    merged_df['Temporal_Coverage'] = merged_df['Temporal_Coverage'] / 100  

    # Calculate the reliability score using the formula
    merged_df['Reliability_Score'] = (
        0.4 * merged_df['Dataset_Size'] +
        0.4 * (1 - merged_df['Missing_Data']) +
        0.2 * merged_df['Temporal_Coverage']
    )

    # Round the scores for better readability
    merged_df['Reliability_Score'] = merged_df['Reliability_Score'].round(3)

    # Sort the regions by score
    merged_df = merged_df.sort_values(by='Reliability_Score', ascending=False)

    # Plot the scores using Plotly
    fig = px.bar(
        merged_df,
        x='Reliability_Score',
        y='Region',
        orientation='h',
        title="<b>Reliability Scores Across Regions</b><br><span style='font-size:14px;'>Based on Dataset Size, Missing Data, and Temporal Coverage</span>",
        labels={'Reliability_Score': 'Reliability Score', 'Region': 'Region'},
        color='Reliability_Score',
        color_continuous_scale=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0",
        font=dict(color="black"),
        title=dict(font=dict(size=18, color='black'))
    )
    fig.show()
    
    # Save the figure as an HTML file
    fig.write_html(output_html_file)
    print(f"Figure saved as {output_html_file}")
    
    # Save the resulting DataFrame to a CSV file for flourish visualisation
    merged_df[['Region', 'Reliability_Score']].to_csv(output_csv_file, index=False)
    print(f"Reliability scores saved to {output_csv_file}")

    