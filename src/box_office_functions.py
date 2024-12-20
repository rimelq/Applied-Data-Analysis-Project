##############################################
#                                            #
#  Box Office Revenue Analysis Python Script #
#                                            #
##############################################

import os
import pandas as pd
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from IPython.display import display
from scipy.stats import gaussian_kde
import statsmodels.api as sm
import patsy

# CONSTANTS---------------------------------:

year_batches = [
    (1950, 1959),
    (1960, 1969),
    (1970, 1979),
    (1980, 1989),
    (1990, 1999),
    (2000, 2009),
    (2010, 2012)
]

HIGHLY_SUCCESSFUL_PERCENTILE = 0.9
SUCCESSFUL_PERCENTILE = 0.4


# FUNCTIONS--------------------------------:


def var_loader(DATA_FOLDER, mode='hollywood'):
    """
    Load various datasets for a specified mode (e.g., here Hollywood)
    """
    
    results = []
    file_paths = [
        f"{mode}/{mode}_data.csv",
        f"{mode}/{mode}_data_ethnicity.csv",
        f"{mode}/{mode}_ethnic_realworld.csv",
        f"{mode}/male_{mode}_realworld_averages.csv",
        f"{mode}/female_{mode}_realworld_averages.csv",
        f"{mode}/bothsexes_{mode}_realworld_averages.csv",
        f"{mode}/male_{mode}_realworld_proportions.csv",
        f"{mode}/female_{mode}_realworld_proportions.csv"
    ]
    
    for file_path in file_paths:
        try:
            full_path = DATA_FOLDER + file_path
            results.append(pd.read_csv(full_path))
        except FileNotFoundError:
            results.append(None)      
    return results
    

######################################################################


def get_gap_interval(gap):
    """
    Determine gap interval category based on percentage value
    """
    
    if gap < 25:
        return "[0,25]"
    elif gap < 50:
        return "[25,50]"
    elif gap < 75:
        return "[50,75]"
    else:
        return "[75,100]"


######################################################################


def compute_representation_gaps_ethnicity(data_ethnicity, realworld_ethnicity, ethnicities, start_year, end_year):
    """
    Compute ethnicity representation gaps for a time period
    """
    
    if data_ethnicity is None or realworld_ethnicity is None or not ethnicities:
        return 0.0
    
    df = data_ethnicity.dropna(subset=['release_y','actor_ethnicity_classification','main_genre']).copy()
    df = df[df['release_y'].between(start_year, end_year)]
    if df.empty:
        return 0.0

    df['casting_size'] = df.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
    film_ethnicities = df.groupby(['wiki_movie_id', 'actor_ethnicity_classification'], observed=False).size().unstack(fill_value=0)
    film_ethnicities = film_ethnicities.div(film_ethnicities.sum(axis=1), axis=0)
    film_ethnicities['casting_size'] = df.groupby('wiki_movie_id')['casting_size'].first()
    weighted_proportions = (film_ethnicities.drop(columns='casting_size').multiply(
        film_ethnicities['casting_size'], axis=0
    ).sum() / film_ethnicities['casting_size'].sum()).reindex(ethnicities, fill_value=0)

    def get_realworld_period(start, end):
        if start>=1950 and end<=1965:
            return "1950-1965"
        elif start>=1960 and end<=1980:
            return "1966-1980"
        elif start>=1970 and end<=1995:
            return "1981-1995"
        else:
            return "1996-2012"

    period_str = get_realworld_period(start_year, end_year)
    rw_subset = realworld_ethnicity[realworld_ethnicity['new_period'] == period_str]
    if rw_subset.empty:
        rw_props = realworld_ethnicity.groupby('group')['size'].mean()
    else:
        rw_props = rw_subset.set_index('group')['size']

    rw_props = rw_props.reindex(ethnicities, fill_value=0)
    if rw_props.sum() == 0:
        return 0.0
    rw_props = rw_props / rw_props.sum()

    with np.errstate(divide='ignore', invalid='ignore'):
        gaps = np.abs(weighted_proportions - rw_props) / rw_props * 100
        gaps = gaps.replace([np.inf, -np.inf, np.nan], 0)
    overall_gap = (gaps * rw_props).sum()
    return overall_gap


######################################################################


def compute_representation_gaps_gender(region_df, male_real_world_df, female_real_world_df, start_year, end_year):
    """
    Compute gender representation gaps for a time period
    """
    
    df = region_df.dropna(subset=['release_y','actor_gender','main_genre']).copy()
    df = df[df['release_y'].between(start_year, end_year)]
    if df.empty:
        return 0.0

    df['casting_size'] = df.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
    gender_counts = df.groupby(['wiki_movie_id', 'actor_gender'], observed=False).size().unstack(fill_value=0)

    for g in ['M', 'F']:
        if g not in gender_counts.columns:
            gender_counts[g] = 0
    gender_props = gender_counts.div(gender_counts.sum(axis=1), axis=0)
    gender_props['casting_size'] = df.groupby('wiki_movie_id')['casting_size'].first()
    weighted = (gender_props[['M','F']].multiply(gender_props['casting_size'], axis=0).sum()) / gender_props['casting_size'].sum()
    m_prop_movie = weighted['M']
    f_prop_movie = weighted['F']
    total = m_prop_movie + f_prop_movie
    if total > 0:
        m_prop_movie /= total
        f_prop_movie /= total

    # Summing only numeric columns:
    male_numeric = male_real_world_df.select_dtypes(include=[np.number])
    female_numeric = female_real_world_df.select_dtypes(include=[np.number])

    male_total = male_numeric.sum().sum()
    female_total = female_numeric.sum().sum()
    real_total = male_total + female_total
    if real_total == 0:
        m_prop_real, f_prop_real = 0.5, 0.5
    else:
        m_prop_real = male_total/real_total
        f_prop_real = female_total/real_total

    gap_m = abs(m_prop_movie - m_prop_real) / m_prop_real * 100 if m_prop_real!=0 else 0
    gap_f = abs(f_prop_movie - f_prop_real) / f_prop_real * 100 if f_prop_real!=0 else 0
    overall_gap = gap_m * m_prop_real + gap_f * f_prop_real
    return overall_gap


######################################################################


def compute_representation_gaps_age(region_df, bothsexes_real_world_averages, start_year, end_year):
    """
    Compute age representation gaps for a time period
    """
    
    # Filter data for the given time period
    df = region_df.dropna(subset=['release_y', 'age_at_release']).copy()
    df = df[df['release_y'].between(start_year, end_year)]
    if df.empty:
        return 0.0

    # Computing the average age for each movie
    df['casting_size'] = df.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
    movie_avg_ages = df[['wiki_movie_id', 'age_at_release']].groupby('wiki_movie_id').apply(
        lambda x: (x['age_at_release'].mean(), len(x))
    )
    
    # Extracting average ages and casting sizes
    movie_avg_ages = movie_avg_ages.reset_index(name='values')
    movie_avg_ages['avg_age'] = movie_avg_ages['values'].apply(lambda x: x[0])
    movie_avg_ages['num_actors'] = movie_avg_ages['values'].apply(lambda x: x[1])

    # Weighted average age across all movies
    weighted_avg_age_movies = (
        (movie_avg_ages['avg_age'] * movie_avg_ages['num_actors']).sum()
        / movie_avg_ages['num_actors'].sum()
    )

    # Find the real-world time period that overlaps with start_year and end_year
    def matches_time_period(row):
        start_period, end_period = map(int, row['Time Period'].split('-'))
        return not (end_period < start_year or start_period > end_year)

    # Filter the relevant row from real-world averages
    matched_rows = bothsexes_real_world_averages[bothsexes_real_world_averages.apply(matches_time_period, axis=1)]

    if matched_rows.empty:
        print(f"No real-world data for years: {start_year}-{end_year}")
        return 0.0

    real_world_row = matched_rows.iloc[0]
    age_columns = [int(col) for col in bothsexes_real_world_averages.columns[1:] if col != '100+']
    real_world_values = real_world_row.iloc[1:].values 

    if '100+' in bothsexes_real_world_averages.columns:
        age_columns.append(100)
        real_world_values = np.append(real_world_values[:-1], real_world_row['100+'])

    # Weighted average age = sum(age * population) / sum(population)
    real_world_avg_age = np.sum(np.array(age_columns) * real_world_values) / np.sum(real_world_values)

    # Compute the percentage age gap
    age_gap_percentage = abs(weighted_avg_age_movies - real_world_avg_age) / real_world_avg_age * 100

    return age_gap_percentage


######################################################################


def get_success_categories_for_df(df):
    """
    Compute success categories for a given batch_df (or entire region dataframe).
    """
    
    df = df.dropna(subset=['wiki_movie_id', 'box_office']).copy()
    movie_revenues = df.groupby('wiki_movie_id', observed=False)['box_office'].first().dropna()
    if movie_revenues.empty:
        return {}

    q90 = movie_revenues.quantile(HIGHLY_SUCCESSFUL_PERCENTILE)
    q40 = movie_revenues.quantile(SUCCESSFUL_PERCENTILE)

    # Ensuring that q40 and q90 are distinct
    if q40 >= q90:
        q40 = q90 * 0.9 
    
    def cat(rev):
        if rev >= q90:
            return "Highly Successful"
        elif rev >= q40:
            return "Successful"
        else:
            return "Normal"

    return movie_revenues.apply(cat).to_dict()


######################################################################


def create_sankey_data_for_metric(region, metric, region_data):
    """
    Create Sankey diagram data for a specific metric and region
    """
    
    datasets = region_data[region]

    if metric == "Ethnicity":
        df = datasets['data_ethnicity']
    else:
        df = datasets['region_data']

    df = df.dropna(subset=['release_y','box_office','main_genre']).copy()
    df['release_y'] = df['release_y'].astype(int)

    genres = df['main_genre'].dropna().unique()
    genres = list(genres) 

    results = []

    # Computing for each batch
    for start_year, end_year in year_batches:
        batch_label = f"{start_year}-{end_year}"
        batch_df = df[df['release_y'].between(start_year, end_year)]
        if batch_df.empty:
            continue

        if metric == "Ethnicity":
            gap = compute_representation_gaps_ethnicity(
                datasets['data_ethnicity'],
                datasets['realworld_ethnicity'],
                datasets['ethnicities'],
                start_year, end_year
            )
        elif metric == "Gender":
            gap = compute_representation_gaps_gender(
                batch_df,
                datasets['male_real_world_proportions'],
                datasets['female_real_world_proportions'],
                start_year, end_year
            )
        elif metric == "Age":
            gap = compute_representation_gaps_age(
                batch_df,
                datasets['bothsexes_real_world_averages'],
                start_year, end_year
            )
        else:
            gap = 0.0

        if gap > 100:
            gap = 100.0
        source_node = get_gap_interval(gap)

        success_map = get_success_categories_for_df(batch_df)
        batch_df = batch_df[batch_df['main_genre'].isin(genres)]
        if batch_df.empty:
            continue

        batch_df['success_cat'] = batch_df['wiki_movie_id'].map(success_map).fillna("Normal")

        # Source (gap interval) -> Genre
        genre_counts = batch_df.groupby('main_genre', observed=False)['wiki_movie_id'].count()
        for g, val in genre_counts.items():
            results.append({
                "Batch Label": batch_label,
                "Step from": 1,
                "Step to": 2,
                "Source": source_node,
                "Target": g,
                "Value": val
            })

        # Genre -> Success
        genre_success_counts = batch_df.groupby(['main_genre','success_cat'], observed=False)['wiki_movie_id'].count()
        for (g, s), val in genre_success_counts.items():
            results.append({
                "Batch Label": batch_label,
                "Step from": 2,
                "Step to": 3,
                "Source": g,
                "Target": s,
                "Value": val
            })

    # Computing "All periods" category (1950-2012)
    all_period_label = "All periods"
    all_period_df = df[df['release_y'].between(1950, 2012)]
    if not all_period_df.empty:
        if metric == "Ethnicity":
            gap = compute_representation_gaps_ethnicity(
                datasets['data_ethnicity'],
                datasets['realworld_ethnicity'],
                datasets['ethnicities'],
                1950, 2012
            )
        elif metric == "Gender":
            gap = compute_representation_gaps_gender(
                all_period_df,
                datasets['male_real_world_proportions'],
                datasets['female_real_world_proportions'],
                1950, 2012
            )
        elif metric == "Age":
            gap = compute_representation_gaps_age(
                all_period_df,
                datasets['bothsexes_real_world_averages'],
                1950, 2012
            )
        else:
            gap = 0.0

        if gap > 100:
            gap = 100.0
        source_node = get_gap_interval(gap)

        success_map = get_success_categories_for_df(all_period_df)
        all_period_df = all_period_df[all_period_df['main_genre'].isin(genres)]
        if not all_period_df.empty:
            all_period_df['success_cat'] = all_period_df['wiki_movie_id'].map(success_map).fillna("Normal")
            # Source (gap interval) -> Genre
            genre_counts = all_period_df.groupby('main_genre', observed=False)['wiki_movie_id'].count()
            for g, val in genre_counts.items():
                results.append({
                    "Batch Label": all_period_label,
                    "Step from": 1,
                    "Step to": 2,
                    "Source": source_node,
                    "Target": g,
                    "Value": val
                })

            # Genre -> Success
            genre_success_counts = all_period_df.groupby(['main_genre','success_cat'], observed=False)['wiki_movie_id'].count()
            for (g, s), val in genre_success_counts.items():
                results.append({
                    "Batch Label": all_period_label,
                    "Step from": 2,
                    "Step to": 3,
                    "Source": g,
                    "Target": s,
                    "Value": val
                })

    if results:
        df_out = pd.DataFrame(results)
        fname = f"./hollywood/{region}_{metric}_sankey.csv"
        df_out.to_csv(fname, index=False)
        print(f"Exported {fname}")
    else:
        print(f"No data for {region} - {metric}, no CSV generated.")


######################################################################


def export_all_movies_csv(region_data):
    """
    Output one big CSV file containing all movies from all regions.
    Each movie has a single row, with Genre, Region, Success rate (Highly Successful / Successful / Normal),
    Number of movies in the region, Box office
    """
    
    # Combining all regions into one DataFrame
    combined = []
    for region, datasets in region_data.items():
        df = datasets['region_data'].copy()
        
        # Cleaning data similarly as before
        df = df.dropna(subset=['release_y', 'box_office', 'main_genre']) 
        df['Region'] = region

        df = df.groupby('wiki_movie_id', as_index=False).first()

        df['Number of movies in the region'] = 1

        combined.append(df)

    # Combine data from all regions
    all_df = pd.concat(combined, ignore_index=True)

    all_df['release_y'] = all_df['release_y'].astype(int, errors='ignore')

    # We compute success categories by region: for each, we compute the thresholds and map them to it.
    all_movies = []
    for region in region_data.keys():
        region_df = all_df[all_df['Region'] == region].copy()
        if region_df.empty:
            continue
        
        # Map success categories
        success_map = get_success_categories_for_df(region_df)
        region_df['Success rate'] = region_df['wiki_movie_id'].map(success_map).fillna("Normal")

        # Keep only required columns
        region_df = region_df[['main_genre', 'Success rate', 'Number of movies in the region', 'Region', 'box_office']]
        region_df.columns = ['Genre', 'Success rate', 'Number of movies in the region', 'Region', 'Box office']

        all_movies.append(region_df)

    # Combine all regions into the final DataFrame
    final_df = pd.concat(all_movies, ignore_index=True)

    # Exporting to CSV
    final_df.to_csv("./hollywood/all_movies_all_regions.csv", index=False)
    print("Exported all_movies_all_regions.csv")


######################################################################


def get_metric_gap(metric, region, df, datasets, start_year, end_year):
    """Helper function to compute the representation gap for a given metric and time period."""
    
    if metric == "Ethnicity":
        # For ethnicity, we must use the data_ethnicity dataframe
        return compute_representation_gaps_ethnicity(
            datasets['data_ethnicity'],
            datasets['realworld_ethnicity'],
            datasets['ethnicities'],
            start_year, end_year
        )
    elif metric == "Gender":
        return compute_representation_gaps_gender(
            df,
            datasets['male_real_world_proportions'],
            datasets['female_real_world_proportions'],
            start_year, end_year
        )
    elif metric == "Age":
        return compute_representation_gaps_age(
            df,
            datasets['bothsexes_real_world_averages'],
            start_year, end_year
        )
    else:
        return 0.0


######################################################################


def create_summary_csv_for_metric(region, metric, region_data):
    """
    Create and export a summary CSV for a specific metric and region
    """
    
    datasets = region_data[region]

    if metric == "Ethnicity":
        df_main = datasets['region_data'].copy()
    else:
        df_main = datasets['region_data'].copy()

    df_main = df_main.dropna(subset=['release_y','box_office','main_genre']).copy()
    df_main['release_y'] = df_main['release_y'].astype(int)

    results = []

    # Compute for each batch
    for start_year, end_year in year_batches:
        batch_label = f"{start_year}-{end_year}"
        batch_df = df_main[df_main['release_y'].between(start_year, end_year)]
        if batch_df.empty:
            continue

        # Compute representation gap
        gap = get_metric_gap(metric, region, batch_df, datasets, start_year, end_year)
        if gap > 100:
            gap = 100.0

        # Mean box office for this batch
        total_box_office = batch_df['box_office'].mean()

        results.append({
            "Batch Label": batch_label,
            "Box Office": total_box_office,
            "Representation Gap (%)": gap
        })

    # Convert results to DataFrame and export
    if results:
        df_out = pd.DataFrame(results)
        fname = f"./hollywood/{region}_{metric}_summary.csv"
        df_out.to_csv(fname, index=False)
        print(f"Exported {fname}")
    else:
        print(f"No data for {region} - {metric}, no CSV generated.")


######################################################################


# Loading the global_summary.csv
global_df = pd.read_csv("./hollywood/global_summary.csv")

# Ensuring that the data is clean
global_df = global_df.dropna(subset=["Box Office", "Representation Gap (%)"])

def run_regression_and_plot_for_region(region_name):
    """
    Function that runs regression and plots it for a given region
    """
    
    # Filter data for this region
    df_region = global_df[global_df["Region"] == region_name].copy()
    
    if df_region.empty:
        print(f"No data for region: {region_name}")
        return
    
    # Simple Linear Regression: Box Office ~ Representation Gap
    X_simple = sm.add_constant(df_region["Representation Gap (%)"])
    y = df_region["Box Office"]
    model_simple = sm.OLS(y, X_simple).fit()
    
    print(f"\n=== Simple Linear Regression Results for {region_name} ===")
    print(model_simple.summary())
    
    # Multiple Linear Regression: Include Metric and Batch Label as categorical variables
    formula = "Q('Box Office') ~ Q('Representation Gap (%)') + C(Metric) + C(Q('Batch Label'))"
    y_m, X_m = patsy.dmatrices(formula, data=df_region, return_type='dataframe')
    model_multiple = sm.OLS(y_m, X_m).fit()
    
    print(f"\n=== Multiple Linear Regression Results for {region_name} ===")
    print(model_multiple.summary())
    
    # Plotting
    gap = df_region["Representation Gap (%)"]
    revenue = df_region["Box Office"]
    
    # Predict from the simple model
    gap_grid = np.linspace(gap.min(), gap.max(), 100)
    X_pred = sm.add_constant(gap_grid)
    y_pred = model_simple.predict(X_pred)
    
    # Vivid palette
    vivid_palette = {
        "teal": "#009392",
        "orange_red": "#e88471",
        "pink": "#cf597e",
        "magenta": "#9e2f7f",
        "purple": "#5c1165"
    }
    
    fig = go.Figure()

    # Scatter points of actual data
    fig.add_trace(go.Scatter(
        x=gap,
        y=revenue,
        mode='markers',
        name='Data',
        marker=dict(color=vivid_palette["pink"], size=8, opacity=0.7),
        hovertemplate='Gap: %{x:.2f}%<br>Box Office: %{y:.2f}<extra></extra>'
    ))

    # Regression line
    fig.add_trace(go.Scatter(
        x=gap_grid,
        y=y_pred,
        mode='lines',
        name='Regression Line',
        line=dict(color=vivid_palette["teal"], width=2),
        hovertemplate='Gap: %{x:.2f}%<br>Predicted Box Office: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': f"{region_name} - Box Office vs Representation Gap (%) with Regression Line",
            'x':0.5,
            'xanchor':'center',
            'yanchor':'top',
            'font':dict(family="Arial", size=16, color="black", weight="bold")
        },
        font=dict(family="Arial", size=12.8),
        xaxis_title="Representation Gap (%)",
        yaxis_title="Box Office (Mean per Batch)",
        template="plotly_white",
        plot_bgcolor="#f2f0f0",
        paper_bgcolor="#f2f0f0",
        legend=dict(
            title="",
            orientation="v",
            y=0.5,
            x=1.02,
            xanchor="left",
            yanchor="middle",
        ),
        margin=dict(t=130, r=200)
    )

    fig.show()
    fig.write_html(f"./hollywood/regression_plot_{region_name}.html")
    
