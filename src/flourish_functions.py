""" 
This file contains the necessary functions used to make the global 
flourish plots and the common basic plots used in all region analyis 

"""

from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np 

def age_density_actors_flourish(df, region_name, genres, periods_dict):
    results = []
    for period_name, (start_year, end_year) in periods_dict.items():
        # Filter data by period
        period_data = df[df['release_y'].between(start_year, end_year)] 
        for genre in genres:
            # Filter data by genre
            genre_data = period_data if genre == "All Genres" else period_data[period_data['main_genre'].str.strip().str.lower() == genre.lower()]

            for gender in ['M', 'F']:
                gender_data = genre_data[genre_data['actor_gender'] == gender]

                # Extract valid ages
                ages = gender_data['age_at_release'].dropna().astype(float)
                ages = ages[ages >= 0]  

                # Compute density
                age_range = np.linspace(0, 100, 101)
                if len(ages) > 1:
                    kde = gaussian_kde(ages)
                    density = kde(age_range)
                else:
                    density = np.zeros_like(age_range)

                # Append results for each age range
                for age, dens in zip(age_range, density):
                    results.append({
                        'Region': region_name,
                        'Period': period_name,
                        'Genre': genre,
                        'Gender': 'actor_male' if gender == 'M' else 'actor_female',
                        'Age': int(age),
                        'Density': dens
                    })

    actor_density_df = pd.DataFrame(results)

    return actor_density_df

#####################################

def age_density_real_world_flourish(df, region_name, gender_label, periods_dict):
    results = []

    for period_name, (start_year, end_year) in periods_dict.items():
        if period_name == "All Periods":
            # Sum across all rows for "All Periods"
            period_data = df.drop(columns=['Time Period'], errors='ignore').sum(axis=0)
        else:
            # Filter data by the selected period
            period_data = df[df['Time Period'] == period_name].drop(columns=['Time Period'], errors='ignore')
            if period_data.empty:
                continue
            period_data = period_data.iloc[0]  

        # Normalize density
        total_density = period_data.sum()
        if total_density > 0:
            period_data /= total_density

        # Append results for each age range
        for age, dens in period_data.items():
            # Handle '100+' edge case
            age = 100 if age == '100+' else float(age)
            results.append({
                'Region': region_name,
                'Period': period_name,  
                'Genre': 'All Genres',  
                'Gender': gender_label,  
                'Age': age,
                'Density': dens
            })

    return pd.DataFrame(results)




##############################

# Function to duplicate real-world data for all genres
def duplicate_realworld_data(df, gender_label, genres):
    duplicated_rows = []
    for _, row in df.iterrows():
        period = row['Period'] if 'Period' in row else None
        for genre in genres:
            new_row = row.copy()
            new_row['Genre'] = genre
            new_row['Gender'] = gender_label
            new_row['Period'] = period 
            duplicated_rows.append(new_row)

    return pd.DataFrame(duplicated_rows)

###############################

# Function to filter data by period 
def save_period_datasets(results, periods):

    for period_name in periods:
        # Filter data for the current period
        period_data = results[results['Period'] == period_name]

        # Save to CSV
        file_name = f'./flourish/age_density_{period_name.replace(" ", "_").lower()}.csv'
        period_data.to_csv(file_name, index=False)
        print(f"Saved: {file_name}")

################################

def combine_actor_and_realworld_data(actor_density, realworld_male_density, realworld_female_density):
    # Prepare Real-World data
    realworld_male_density = realworld_male_density.rename(columns={'Density': 'Real-World Male Population'})
    realworld_female_density = realworld_female_density.rename(columns={'Density': 'Real-World Female Population'})

    # Drop unnecessary 'Gender' column for real-world data
    realworld_male_density = realworld_male_density.drop(columns=['Gender'], errors='ignore')
    realworld_female_density = realworld_female_density.drop(columns=['Gender'], errors='ignore')

    # Merge Real-World Male and Female datasets
    realworld_combined = realworld_male_density.merge(
        realworld_female_density,
        on=['Age', 'Genre', 'Period', 'Region'],
        how='outer'
    )

    # Prepare actor data
    actor_density = actor_density.pivot_table(
        index=['Age', 'Genre', 'Period', 'Region'],
        columns='Gender',
        values='Density',
        aggfunc='sum'
    ).reset_index()

    # Rename pivoted actor columns 
    actor_density = actor_density.rename(columns={'actor_male': 'Male Actors', 'actor_female': 'Female Actors'})

    # Combine Actor and Real-World Data
    combined_df = actor_density.merge(
        realworld_combined,
        on=['Age', 'Genre', 'Period', 'Region'],
        how='outer'
    )

    # Fill missing densities with zeros
    combined_df = combined_df.fillna(0)

    # Final column order
    combined_df = combined_df[['Age', 'Genre', 'Period', 'Region', 'Male Actors', 'Female Actors', 'Real-World Male Population', 'Real-World Female Population']]

    return combined_df

###############################

# Extract cluster based on countries
def assign_cluster(country, clusters):
    for cluster_name, cluster_countries in clusters.items():
        if country in cluster_countries:
            return cluster_name
    return "Other"