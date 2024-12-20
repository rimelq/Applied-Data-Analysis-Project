##############################################
#                                            #
#      Hollywood Analysis Python Script      #
#                                            #
##############################################


import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
from scipy.stats import friedmanchisquare
from scipy.stats import wasserstein_distance, entropy
from scipy.stats import chisquare
import math


# ETHNICITY FUNCTIONS--------------------------------:


def var_loader1(DATA_FOLDER, mode='hollywood'):
    """
    Load various datasets for a given mode, here for Hollywood
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
            df = pd.read_csv(full_path)
            results.append(df)
        except FileNotFoundError:
            results.append(None)      
    return results


##################################################################


def safe_convert_to_int(df, column):
    """
    Safely convert a column in a DataFrame to integers.
    """
    
    df = df[df[column].notna()]
    df = df[np.isfinite(df[column])]
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df[df[column].notna() & np.isfinite(df[column])]
    df[column] = df[column].astype(int)
    return df


##################################################################


def export_ethnicity_representation_by_genre_batches(region, region_data):
    """
    Export ethnicity representation ratios by genre and year batches
    """
    
    datasets = region_data[region]
    data_ethnicity = datasets['data_ethnicity']
    realworld_ethnicity = datasets['realworld_ethnicity']
    ethnicities = datasets['ethnicities']

    if data_ethnicity is None or realworld_ethnicity is None or not ethnicities:
        print(f"No data for {region} ethnicity analysis.")
        return

    ethnicity_mapping = {
        "African Americans": "African Americans",
        "American Indians": "American Indians",
        "Arab Americans": "Arab",
        "Asian Americans": "Asian",
        "Caucasian Americans": "Caucasian",
        "Jewish Americans": "Jewish",
        "Latino Americans": "Latino"
    }

    if 'release_y' not in data_ethnicity.columns:
        print(f"No release_y column for {region}.")
        return
    data_ethnicity = safe_convert_to_int(data_ethnicity, 'release_y')

    start_year = 1950
    end_year = 2012
    year_batches = {year: range(year, min(year + 5, end_year + 1)) for year in range(start_year, end_year + 1, 5)}

    genres = data_ethnicity['main_genre'].dropna().unique()
    if len(genres) == 0:
        print(f"No genres found for {region}.")
        return
    genres = sorted(genres)

    for genre in genres:
        genre_results = []
        for sy, years in year_batches.items():
            batch_results = {ethnicity: [] for ethnicity in ethnicities}

            for year in years:
                movie_data = data_ethnicity[(data_ethnicity['release_y'] == year) &
                                            (data_ethnicity['main_genre'] == genre)]
                if movie_data.empty:
                    continue

                movie_data = movie_data.copy()
                movie_data['casting_size'] = movie_data.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
                film_ethnicities = movie_data.groupby(['wiki_movie_id', 'actor_ethnicity_classification'], observed=False).size().unstack(fill_value=0)
                if film_ethnicities.empty:
                    continue

                film_ethnicities = film_ethnicities.div(film_ethnicities.sum(axis=1), axis=0)
                film_ethnicities['casting_size'] = movie_data.groupby('wiki_movie_id')['casting_size'].first()

                total_casting = film_ethnicities['casting_size'].sum()
                if total_casting == 0:
                    continue

                weighted_ethnicities = film_ethnicities.drop(columns='casting_size').multiply(
                    film_ethnicities['casting_size'], axis=0
                ).sum() / total_casting

                weighted_ethnicities = weighted_ethnicities.reindex(ethnicities, fill_value=0)
                if realworld_ethnicity is not None and 'group' in realworld_ethnicity.columns and 'size' in realworld_ethnicity.columns:
                    rw_set = realworld_ethnicity.set_index('group')['size']
                    
                    rw_set = rw_set.replace([0, np.inf, -np.inf], np.nan).fillna(1e-10)
                    representation_ratio = ((weighted_ethnicities / rw_set) - 1) * 100
                    representation_ratio = representation_ratio.replace([np.inf, -np.inf], 0).fillna(0)

                    for ethnicity_name, ratio in representation_ratio.items():
                        batch_results[ethnicity_name].append(ratio)

            for ethnicity_name, ratios in batch_results.items():
                if ratios:
                    avg_ratio = sum(ratios) / len(ratios)
                    mapped_name = ethnicity_mapping.get(ethnicity_name, ethnicity_name)
                    genre_results.append({
                        "Ethnicity": mapped_name,
                        "Batch Start Year": sy,
                        "Representation Ratio": avg_ratio
                    })

        if genre_results:
            genre_df = pd.DataFrame(genre_results)
            if not genre_df.empty:
                wide_df = genre_df.pivot_table(
                    index="Ethnicity",
                    columns="Batch Start Year",
                    values="Representation Ratio",
                    aggfunc="first"
                ).reset_index()

                wide_df.columns.name = None
                wide_df.columns = ["Ethnicity"] + [str(year) for year in wide_df.columns[1:]]

                file_name = f"./flourish/ethnicity_representation_{genre.replace('/', '_')}.csv"
                wide_df.to_csv(file_name, index=False)
                print(f"CSV exported: {file_name}")


##################################################################


def export_ethnicity_representation_all_genres(region, region_data):
    """
    Export ethnicity representation across all genres
    """
    
    datasets = region_data[region]
    data_ethnicity = datasets.get('data_ethnicity', None)
    realworld_ethnicity = datasets.get('realworld_ethnicity', None)
    ethnicities = datasets.get('ethnicities', [])

    if data_ethnicity is None or realworld_ethnicity is None or not ethnicities:
        print(f"No ethnicity data for {region}.")
        return

    ethnicity_mapping = {
        "African Americans": "African Americans",
        "American Indians": "American Indians",
        "Arab Americans": "Arab",
        "Asian Americans": "Asian",
        "Caucasian Americans": "Caucasian",
        "Jewish Americans": "Jewish",
        "Latino Americans": "Latino"
    }

    if 'release_y' in data_ethnicity.columns:
        data_ethnicity = safe_convert_to_int(data_ethnicity, 'release_y')
    else:
        print(f"No release_y column for {region}. Cannot proceed.")
        return

    start_year = 1950
    end_year = 2012
    year_batches = {year: range(year, min(year + 5, end_year + 1)) for year in range(start_year, end_year + 1, 5)}

    all_results = []

    for sy, years in year_batches.items():
        batch_results = {ethnicity: [] for ethnicity in ethnicities}

        for year in years:
            movie_data = data_ethnicity[data_ethnicity['release_y'] == year]
            if movie_data.empty:
                continue

            movie_data = movie_data.copy()
            movie_data['casting_size'] = movie_data.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
            film_ethnicities = movie_data.groupby(['wiki_movie_id', 'actor_ethnicity_classification'], observed=False).size().unstack(fill_value=0)
            if film_ethnicities.empty:
                continue

            film_ethnicities = film_ethnicities.div(film_ethnicities.sum(axis=1), axis=0)
            film_ethnicities['casting_size'] = movie_data.groupby('wiki_movie_id')['casting_size'].first()
            total_casting = film_ethnicities['casting_size'].sum()
            if total_casting == 0:
                continue
            weighted_ethnicities = film_ethnicities.drop(columns='casting_size').multiply(
                film_ethnicities['casting_size'], axis=0
            ).sum() / total_casting

            weighted_ethnicities = weighted_ethnicities.reindex(ethnicities, fill_value=0)
            rw_set = realworld_ethnicity.set_index('group')['size']
            rw_set = rw_set.replace([0, np.inf, -np.inf], np.nan).fillna(1e-10)
            representation_ratio = ((weighted_ethnicities / rw_set) - 1) * 100
            representation_ratio = representation_ratio.replace([np.inf, -np.inf], 0).fillna(0)

            for ethnicity_name, ratio in representation_ratio.items():
                batch_results[ethnicity_name].append(ratio)

        for ethnicity_name, ratios in batch_results.items():
            if ratios:
                all_results.append({
                    "Ethnicity": ethnicity_mapping.get(ethnicity_name, ethnicity_name),
                    "Batch Start Year": sy,
                    "Representation Ratio": sum(ratios) / len(ratios)
                })

    if all_results:
        results_df = pd.DataFrame(all_results)
        if not results_df.empty:
            wide_df = results_df.pivot_table(
                index="Ethnicity",
                columns="Batch Start Year",
                values="Representation Ratio",
                aggfunc="first"
            ).reset_index()

            wide_df.columns.name = None
            wide_df.columns = ["Ethnicity"] + [str(year) for year in wide_df.columns[1:]]

            file_name = f"./flourish/ethnicity_representation_all_genres.csv"
            wide_df.to_csv(file_name, index=False)
            print(f"CSV exported: {file_name}")


##################################################################

        
def chi_square_test_observed_vs_expected(data_ethnicity, realworld_ethnicity, genre="All"):
    """
    Perform chi-square test comparing observed and expected ethnicity frequencies
    """
    
    if genre != "All":
        data_ethnicity = data_ethnicity[data_ethnicity['main_genre'] == genre]

    # Ensure data_ethnicity isn't empty and has the required column
    if data_ethnicity.empty or 'actor_ethnicity_classification' not in data_ethnicity.columns:
        print("Not enough data to perform chi-square test for observed vs expected.")
        return

    observed_counts = data_ethnicity['actor_ethnicity_classification'].value_counts()

    if realworld_ethnicity is None or 'group' not in realworld_ethnicity.columns or 'size' not in realworld_ethnicity.columns:
        print("No real-world ethnicity data to compute expected frequencies.")
        return

    realworld_ethnicity_agg = realworld_ethnicity.groupby('group', as_index=False)['size'].sum()
    total_size = realworld_ethnicity_agg['size'].sum()
    if total_size == 0:
        print("No real-world data size is zero or invalid.")
        return

    realworld_ethnicity_agg['proportion'] = realworld_ethnicity_agg['size'] / total_size
    realworld_proportions = realworld_ethnicity_agg.set_index('group')['proportion']

    common_categories = observed_counts.index.intersection(realworld_proportions.index)
    if len(common_categories) == 0:
        print("No common categories between observed and expected. Cannot perform chi-square test.")
        return

    observed_counts = observed_counts.loc[common_categories]
    total_observed = observed_counts.sum()
    expected_counts = realworld_proportions.loc[common_categories] * total_observed
    expected_counts = expected_counts.replace([np.inf, -np.inf], np.nan).fillna(1e-10)

    chi2, p = stats.chisquare(f_obs=observed_counts, f_exp=expected_counts)

    print("\n\n\n--- Chi-Square Test for Observed vs. Expected Frequencies (Genre: {}) ---".format(genre))
    print("Chi-Square Statistic:", chi2)
    print("p-value:", p)
    print("\nObserved Frequencies:")
    print(observed_counts)
    print("\nExpected Frequencies:")
    print(np.round(expected_counts, 2))

    if p < 0.05:
        print("\nConclusion: Reject H0. Observed ethnic representation significantly differs from the expected.")
    else:
        print("\nConclusion: Fail to reject H0. Observed ethnic representation aligns with the expected.")


##################################################################


def chi_square_test_genre_dependence(data_ethnicity):
    """
    Perform chi-square test for ethnicity dependence on genre
    """
    
    if data_ethnicity.empty or 'actor_ethnicity_classification' not in data_ethnicity.columns or 'main_genre' not in data_ethnicity.columns:
        print("Not enough data or required columns missing to perform chi-square test for genre dependence.")
        return

    # Create contingency table
    contingency_table = pd.crosstab(
        data_ethnicity['actor_ethnicity_classification'], 
        data_ethnicity['main_genre']
    )

    # Ensuring the contingency table is not empty or degenerate
    if contingency_table.empty or contingency_table.sum().sum() == 0:
        print("Contingency table is empty or invalid for chi-square test.")
        return

    # Perform chi-square test
    try:
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

        print("\n\n\n--- Chi-Square Test for Genre-Dependence of Ethnic Representation ---")
        print("Chi-Square Statistic:", chi2)
        print("p-value:", p)
        print("Degrees of Freedom:", dof)
        print("\nExpected Frequencies:")
        print(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))

        if p < 0.05:
            print("\nConclusion: Reject H0. Ethnicity distribution depends on genre.")
        else:
            print("\nConclusion: Fail to reject H0. Ethnicity distribution is independent of genre.")
    except ValueError as e:
        print("Error performing chi-square test:", e)
        return


# GENDER FUNCTIONS--------------------------------:
    

def calculate_weighted_gender_proportions(df, period, genre):
    """
    Calculate weighted gender proportions for a genre and period
    """
    
    df_filtered = df.copy()
    df_filtered = df_filtered.dropna(subset=['actor_gender'])
    if 'release_y' not in df_filtered.columns:
        return 0, 0
    df_filtered = safe_convert_to_int(df_filtered, 'release_y')

    if period != "All periods":
        start_year, end_year = map(int, period.split('-'))
        df_filtered = df_filtered[df_filtered['release_y'].between(start_year, end_year)]

    if genre != "All":
        df_filtered = df_filtered[df_filtered['main_genre'] == genre]

    if df_filtered.empty:
        return 0, 0

    df_filtered['casting_size'] = df_filtered.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
    gender_counts = df_filtered.groupby(['wiki_movie_id', 'actor_gender']).size().unstack(fill_value=0)

    for gender_col in ['M', 'F']:
        if gender_col not in gender_counts.columns:
            gender_counts[gender_col] = 0

    gender_proportions = gender_counts.div(gender_counts.sum(axis=1), axis=0)
    gender_proportions['casting_size'] = df_filtered.groupby('wiki_movie_id')['casting_size'].first()
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


##################################################################


def prepare_real_world_data(male_real_world_df, female_real_world_df):
    """
    Prepare real-world data for gender proportions analysis
    """
    
    if 'Time Period' not in male_real_world_df.columns:
        male_real_world_df.reset_index(inplace=True)
    if 'Time Period' not in female_real_world_df.columns:
        female_real_world_df.reset_index(inplace=True)
    male_real_world_df.set_index('Time Period', inplace=True)
    female_real_world_df.set_index('Time Period', inplace=True)
    return male_real_world_df, female_real_world_df


##################################################################


def get_real_world_gender_proportions(period, male_real_world_df, female_real_world_df):
    """
    Get real-world gender proportions for a specific period
    """
    
    if period == "All periods":
        male_total = male_real_world_df.sum().sum()
        female_total = female_real_world_df.sum().sum()
    else:
        if period not in male_real_world_df.index or period not in female_real_world_df.index:
            return 0.5, 0.5
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


##################################################################


def export_female_proportions_by_year_batches(region, region_data):
    """
    Export female gender proportions by year batches
    """
    
    datasets = region_data[region]
    region_df = datasets['region_data']
    if 'release_y' not in region_df.columns:
        print("No release_y column in region data.")
        return
    region_df = safe_convert_to_int(region_df, 'release_y')

    start_year = 1950
    end_year = 2012
    year_batches = {year: range(year, min(year + 5, end_year + 1)) for year in range(start_year, end_year + 1, 5)}

    genres = sorted(region_df['main_genre'].dropna().unique())
    results = []

    for genre in genres:
        genre_results = {'Genre': genre}
        for batch_start, years in year_batches.items():
            batch_results = []
            for year in years:
                filtered_data = region_df[(region_df['release_y'] == year) & (region_df['main_genre'] == genre)].copy()
                if filtered_data.empty:
                    continue
                # Use .loc to avoid SettingWithCopyWarning
                filtered_data['casting_size'] = (
                    filtered_data.groupby('wiki_movie_id')['wiki_movie_id'].transform('count')
                )
                gender_counts = filtered_data.groupby(['wiki_movie_id', 'actor_gender']).size().unstack(fill_value=0)
                if 'F' not in gender_counts.columns:
                    gender_counts['F'] = 0
                gender_proportions = gender_counts.div(gender_counts.sum(axis=1), axis=0)
                gender_proportions['casting_size'] = filtered_data.groupby('wiki_movie_id')['casting_size'].first()

                total_casting = gender_proportions['casting_size'].sum()
                if total_casting == 0:
                    continue

                weighted_female_proportion = (
                    gender_proportions['F'].multiply(gender_proportions['casting_size']).sum()
                    / total_casting
                ) * 100
                batch_results.append(weighted_female_proportion)
            if batch_results:
                genre_results[batch_start] = sum(batch_results) / len(batch_results)
            else:
                genre_results[batch_start] = 0
        results.append(genre_results)

    results_df = pd.DataFrame(results)
    file_name = f"./flourish/female_proportions_{region}_by_batches.csv"
    results_df.to_csv(file_name, index=False)
    print(f"CSV exported: {file_name}")


##################################################################


def chi_square_test_gender_proportions_region(region_data=None, region="Hollywood", period="All periods", genres=["All"]):
    """
    Perform chi-square test for gender proportions in a region and period
    """
    
    if region_data is None:
        raise ValueError("region_data dictionary must be provided.")

    # Extract datasets for the specified region
    datasets = region_data[region]
    region_df = datasets['region_data'].copy()
    male_real_world_df = datasets['male_real_world_proportions'].copy()
    female_real_world_df = datasets['female_real_world_proportions'].copy()

    # Prepare real-world data for indexing by time period
    male_real_world_df, female_real_world_df = prepare_real_world_data(male_real_world_df, female_real_world_df)

    # Get real-world gender proportions for the specified period
    real_world_male, real_world_female = get_real_world_gender_proportions(period, male_real_world_df, female_real_world_df)
    # Normalize if total > 0
    total_pop = real_world_male + real_world_female
    if total_pop > 0:
        real_world_male /= total_pop
        real_world_female /= total_pop

    # Determine genre list
    if "All" in genres or not genres:
        genre_list = sorted(region_df['main_genre'].dropna().unique())
    else:
        genre_list = genres

    # Compute observed proportions for each genre
    proportions = []
    for g in genre_list:
        male_prop, female_prop = calculate_weighted_gender_proportions(region_df, period, g)
        proportions.append({"Category": g, "Male": male_prop, "Female": female_prop, "Type": "Genre"})

    # Add real-world population proportions
    proportions.append({
        "Category": "Real-world Population",
        "Male": real_world_male,
        "Female": real_world_female,
        "Type": "Real-world"
    })

    proportions_df = pd.DataFrame(proportions)

    # Compute observed proportions (excluding the real-world row)
    observed_male = proportions_df.loc[proportions_df['Category'] != 'Real-world Population', 'Male'].mean()
    observed_female = proportions_df.loc[proportions_df['Category'] != 'Real-world Population', 'Female'].mean()
    observed_proportions = np.array([observed_male, observed_female])
    observed_proportions /= observed_proportions.sum()

    real_world_proportions = np.array([real_world_male, real_world_female])
    total_samples = 1000
    observed_counts = observed_proportions * total_samples
    expected_counts = real_world_proportions * total_samples

    # Perform the Chi-Square test
    chi2, p = chisquare(f_obs=observed_counts, f_exp=expected_counts)

    print(f"\n--- Chi-Square Test for Gender Proportions in {region} (Period: {period}) ---")
    print("Observed Counts:", observed_counts.round(1))
    print("Expected Counts:", expected_counts.round(1))
    print("Chi-Square Statistic:", chi2)
    print("p-value:", p)

    if p < 0.05:
        print("\nConclusion: Reject H0. Gender proportions differ significantly from the real-world.")
    else:
        print("\nConclusion: Fail to reject H0. Gender proportions align with the real-world.")


##################################################################


def friedman_test_female_proportions(data_ethnicity, start_year=1950, end_year=2012, batch_size=5):
    """
    Perform Friedman test on female proportions across genres over time
    """
    
    time_batches = [(year, year + batch_size - 1) for year in range(start_year, end_year + 1, batch_size)]
    genre_proportions = {}

    for start, end in time_batches:
        batch_data = data_ethnicity[(data_ethnicity['release_y'] >= start) & 
                                    (data_ethnicity['release_y'] <= end)]
        genre_gender_counts = batch_data.groupby(['main_genre', 'actor_gender']).size().unstack(fill_value=0)
        if 'F' not in genre_gender_counts.columns:
            genre_gender_counts['F'] = 0
        genre_gender_counts['female_proportion'] = genre_gender_counts['F'] / genre_gender_counts.sum(axis=1)

        for genre in genre_gender_counts.index:
            if genre not in genre_proportions:
                genre_proportions[genre] = []
            genre_proportions[genre].append(genre_gender_counts.at[genre, 'female_proportion'])

    max_length = len(time_batches)
    for genre, proportions_list in genre_proportions.items():
        if len(proportions_list) < max_length:
            proportions_list.extend([math.nan] * (max_length - len(proportions_list)))

    genre_proportions_df = pd.DataFrame(genre_proportions)
    genre_proportions_df.dropna(axis=1, how='all', inplace=True)

    valid_genres = genre_proportions_df.dropna(axis=1).columns
    filtered_df = genre_proportions_df[valid_genres]
    time_batch_proportions = [filtered_df.iloc[i].values for i in range(len(time_batches))]

    if len(valid_genres) < 2:
        print("Not enough genres with complete data for Friedman test.")
        return math.nan, math.nan

    stat, p = friedmanchisquare(*time_batch_proportions)

    print("\n--- Friedman Test for Female Representation Consistency Across Genres (5-Year Batches) ---")
    print("Friedman Chi-Square Statistic:", stat)
    print("p-value:", p)

    if p < 0.05:
        print("\nConclusion: Reject H0. Female representation across genres varies significantly over time.")
    else:
        print("\nConclusion: Fail to reject H0. Female representation across genres is consistent over time.")

    return stat, p


##################################################################


def rank_genres_by_female_proportion(region, region_data, period="All periods"):
    """
    Rank genres by their female proportion in a period
    """
    
    datasets = region_data[region]
    region_df = datasets['region_data']
    genres = sorted(region_df['main_genre'].dropna().unique())
    proportions = []
    for genre in genres:
        _, female_prop = calculate_weighted_gender_proportions(region_df, period, genre)
        proportions.append({"Genre": genre, "Female Proportion": female_prop})
    proportions_df = pd.DataFrame(proportions)
    proportions_df.sort_values(by="Female Proportion", ascending=False, inplace=True)
    # Print top 10 genres
    print("\n--- Top 10 Genres by Female Proportion ---")
    print(proportions_df.head(10).to_string(index=False))


# AGE FUNCTIONS--------------------------------:
    

def calculate_gini(array):
    """
    Calculate the Gini coefficient for a given distribution.
    """
    
    array = np.array(array, dtype=float)
    if array.sum() == 0:
        return 0.0
    sorted_array = np.sort(array)
    n = len(sorted_array)
    cumulative = np.cumsum(sorted_array) / sorted_array.sum()
    gini = 1 - 2 * np.sum(cumulative * (1 / n))
    return gini


##################################################################


def calculate_kl_divergence(p, q):
    """
    Calculate the KL divergence between two distributions p and q.
    """
    
    p = np.clip(p, 1e-10, None)  
    q = np.clip(q, 1e-10, None)
    return entropy(p, q)


##################################################################


def create_dashboard(region, region_data):
    """
    Create a dashboard analyzing regional age and gender distributions.
    """
    
    datasets = region_data[region]
    region_df = datasets['region_data'].copy()

    if 'release_y' in region_df.columns:
        region_df = safe_convert_to_int(region_df, 'release_y')

    male_real_world_averages = datasets['male_real_world_averages'].copy()
    female_real_world_averages = datasets['female_real_world_averages'].copy()

    # Process real-world data
    male_real_world_averages = male_real_world_averages.drop(columns="Time Period", errors="ignore")
    female_real_world_averages = female_real_world_averages.drop(columns="Time Period", errors="ignore")

    # Age bins
    age_bins = np.arange(0, 101, 5)
    bin_labels = [f"{int(bin)}-{int(bin + 4)}" for bin in age_bins[:-1]]

    male_real_dist = []
    female_real_dist = []

    for start, end in zip(age_bins[:-1], age_bins[1:]):
        male_bin_total = male_real_world_averages.iloc[:, start:end].sum(axis=1).sum()
        female_bin_total = female_real_world_averages.iloc[:, start:end].sum(axis=1).sum()
        male_real_dist.append(male_bin_total)
        female_real_dist.append(female_bin_total)

    male_real_dist = np.array(male_real_dist, dtype=float)
    female_real_dist = np.array(female_real_dist, dtype=float)

    # Normalize distributions
    if male_real_dist.sum() > 0:
        male_real_dist /= male_real_dist.sum()
    if female_real_dist.sum() > 0:
        female_real_dist /= female_real_dist.sum()

    male_actors = region_df[region_df['actor_gender'] == 'M']['age_at_release'].dropna()
    female_actors = region_df[region_df['actor_gender'] == 'F']['age_at_release'].dropna()

    male_actor_hist, _ = np.histogram(male_actors, bins=age_bins, density=True)
    female_actor_hist, _ = np.histogram(female_actors, bins=age_bins, density=True)

    if male_actor_hist.sum() > 0:
        male_actor_hist /= male_actor_hist.sum()
    if female_actor_hist.sum() > 0:
        female_actor_hist /= female_actor_hist.sum()

    # Compute metrics
    gini_male_real = calculate_gini(male_real_dist)
    gini_female_real = calculate_gini(female_real_dist)
    gini_male_actors = calculate_gini(male_actor_hist)
    gini_female_actors = calculate_gini(female_actor_hist)

    wasserstein_male_female_actors = wasserstein_distance(male_actor_hist, female_actor_hist)
    kl_div_male_female_actors = calculate_kl_divergence(male_actor_hist, female_actor_hist)

    wasserstein_male_female_real = wasserstein_distance(male_real_dist, female_real_dist)
    kl_div_male_female_real = calculate_kl_divergence(male_real_dist, female_real_dist)

    wasserstein_male_actor_real = wasserstein_distance(male_actor_hist, male_real_dist)
    kl_div_male_actor_real = calculate_kl_divergence(male_actor_hist, male_real_dist)

    wasserstein_female_actor_real = wasserstein_distance(female_actor_hist, female_real_dist)
    kl_div_female_actor_real = calculate_kl_divergence(female_actor_hist, female_real_dist)

    # Summary of metrics
    data_summary = {
        "Comparison": [
            "Male Actors (Gini)",
            "Female Actors (Gini)",
            "Male Real (Gini)",
            "Female Real (Gini)",
            "Male Actors vs Female Actors",
            "Male Real vs Female Real",
            "Male Actors vs Male Real",
            "Female Actors vs Female Real"
        ],
        "Gini or Wasserstein/KL": [
            gini_male_actors,
            gini_female_actors,
            gini_male_real,
            gini_female_real,
            f"Wasserstein: {wasserstein_male_female_actors:.2f}, KL: {kl_div_male_female_actors:.2f}",
            f"Wasserstein: {wasserstein_male_female_real:.2f}, KL: {kl_div_male_female_real:.2f}",
            f"Wasserstein: {wasserstein_male_actor_real:.2f}, KL: {kl_div_male_actor_real:.2f}",
            f"Wasserstein: {wasserstein_female_actor_real:.2f}, KL: {kl_div_female_actor_real:.2f}"
        ]
    }
    summary_df = pd.DataFrame(data_summary)

    # Export summary to CSV
    summary_csv_filename = f"./flourish/{region}_age_distribution_summary.csv"
    summary_df.to_csv(summary_csv_filename, index=False)
    print(f"CSV exported: {summary_csv_filename}")

    # Create and export Lorenz plot, actor ratio plot, real ratio plot
    vivid_palette = {
        "teal": "#009392",
        "orange_red": "#e88471",
        "pink": "#cf597e",
        "magenta": "#9e2f7f",
        "purple": "#5c1165"
    }

    def lorenz_curve(data, label, color):
        """
        Lorenz curve function
        """
        
        if data.sum() == 0:
            print(f"Skipping Lorenz curve for {label} due to empty data.")
            return None
        sorted_data = np.sort(data)
        cumulative = np.cumsum(sorted_data) / sorted_data.sum()
        cumulative = np.insert(cumulative, 0, 0)
        return go.Scatter(
            x=np.linspace(0, 1, len(cumulative)),
            y=cumulative,
            name=label,
            mode="lines",
            line=dict(color=color)
        )

    # Lorenz curves
    fig_lorenz = go.Figure()
    male_real_trace = lorenz_curve(male_real_dist, "Male Real Population", vivid_palette["teal"])
    if male_real_trace: fig_lorenz.add_trace(male_real_trace)
    female_real_trace = lorenz_curve(female_real_dist, "Female Real Population", vivid_palette["orange_red"])
    if female_real_trace: fig_lorenz.add_trace(female_real_trace)
    male_actor_trace = lorenz_curve(male_actor_hist, "Male Actors", vivid_palette["pink"])
    if male_actor_trace: fig_lorenz.add_trace(male_actor_trace)
    female_actor_trace = lorenz_curve(female_actor_hist, "Female Actors", vivid_palette["magenta"])
    if female_actor_trace: fig_lorenz.add_trace(female_actor_trace)
    fig_lorenz.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Equality Line", line=dict(dash="dash", color=vivid_palette["purple"])))

    # Update Lorenz figure layout
    fig_lorenz.update_layout(
        title={
            'text': f"Lorenz Curves for Age Distributions in {region}",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 25},  
            'font': dict(family="Arial", size=16, color="black", weight="bold")  
        },
        font=dict(family="Arial", size=12.8),  
        xaxis_title="Cumulative Population",
        yaxis_title="Cumulative Age Distribution",
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
        margin=dict(t=130, r=200),  
    )


    def plot_actor_gender_ratios():
        """
        Function to plot ratios for actors
        """
        
        male_ratio = male_actor_hist / (male_actor_hist + female_actor_hist)
        female_ratio = female_actor_hist / (male_actor_hist + female_actor_hist)
        male_ratio = np.nan_to_num(male_ratio)
        female_ratio = np.nan_to_num(female_ratio)
    
        fig_ratio = go.Figure()
        fig_ratio.add_trace(go.Bar(
            x=bin_labels, 
            y=male_ratio * 100, 
            name="Male Ratio (%)", 
            marker=dict(color=vivid_palette["teal"]),
            text=[f"{val*100:.1f}" for val in male_ratio],
            textposition="inside",
            textangle=0,
            textfont=dict(color="white", family="Arial", size=13, weight="bold"),
            insidetextanchor='middle'
        ))
        fig_ratio.add_trace(go.Bar(
            x=bin_labels, 
            y=female_ratio * 100, 
            name="Female Ratio (%)", 
            marker=dict(color=vivid_palette["magenta"]),
            base=male_ratio * 100,
            text=[f"{val*100:.1f}" for val in female_ratio],
            textposition="inside",
            textangle=0,
            textfont=dict(color="white", family="Arial", size=13, weight="bold"),
            insidetextanchor='middle'
        ))
        fig_ratio.update_layout(
            title={
                'text': f"Actors Male/Female Ratios by Age in {region}",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'pad': {'b': 15},  
                'font': dict(family="Arial", size=16, color="black", weight="bold")
            },
            font=dict(family="Arial", size=12.8),
            barmode="stack",
            xaxis_title="Age Groups",
            yaxis_title="Percentage",
            template="plotly_white",
            plot_bgcolor="#f2f0eb",
            paper_bgcolor="#f2f0eb",
            legend=dict(
                title="Gender",
                orientation="h",
                yanchor="top",
                y=1.13,  
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=95, b=50), 
            bargap=0.05
        )
        return fig_ratio
    
    def plot_real_gender_ratios():
        """Function to plot ratios for real populations"""
        
        total_real = male_real_dist + female_real_dist
        male_real_ratio = np.nan_to_num(male_real_dist / total_real)
        female_real_ratio = np.nan_to_num(female_real_dist / total_real)
    
        fig_real_ratio = go.Figure()
        fig_real_ratio.add_trace(go.Bar(
            x=bin_labels, 
            y=male_real_ratio * 100, 
            name="Male Ratio (%)", 
            marker=dict(color=vivid_palette["teal"]),
            text=[f"{val*100:.1f}" for val in male_real_ratio],
            textposition="inside",
            textangle=0,
            textfont=dict(color="white", family="Arial", size=13, weight="bold"),
            insidetextanchor='middle'
        ))
        fig_real_ratio.add_trace(go.Bar(
            x=bin_labels, 
            y=female_real_ratio * 100, 
            name="Female Ratio (%)", 
            marker=dict(color=vivid_palette["magenta"]),
            base=male_real_ratio * 100,
            text=[f"{val*100:.1f}" for val in female_real_ratio],
            textposition="inside",
            textangle=0,
            textfont=dict(color="white", family="Arial", size=13, weight="bold"),
            insidetextanchor='middle'
        ))
        fig_real_ratio.update_layout(
            title={
                'text': f"Real Population Male/Female Ratios by Age in {region}",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'pad': {'b': 15},  
                'font': dict(family="Arial", size=16, color="black", weight="bold")
            },
            font=dict(family="Arial", size=12.8),
            barmode="stack",
            xaxis_title="Age Groups",
            yaxis_title="Percentage",
            template="plotly_white",
            plot_bgcolor="#f2f0eb",
            paper_bgcolor="#f2f0eb",
            legend=dict(
                title="Gender",
                orientation="h",
                yanchor="top",
                y=1.13,  
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=95, b=50),  
            bargap=0.05
        )
        return fig_real_ratio
    
    fig_ratio_actors = plot_actor_gender_ratios()
    fig_ratio_real = plot_real_gender_ratios()
        
    fig_lorenz.show()
    fig_ratio_actors.show()
    fig_ratio_real.show()

    # Save the figures to HTML
    fig_lorenz.write_html("./flourish/lorenz_plots.html")
    print("Lorenz plot has been saved to './flourish/lorenz_plots.html'.")
    fig_ratio_actors.write_html("./flourish/ratio_actors.html")
    print("Actors Gender Ratio plot has been saved to './flourish/ratio_actors.html'.")
    fig_ratio_real.write_html("./flourish/ratio_real.html")
    print("Real Population Gender Ratio plot has been saved to './flourish/ratio_real.html'.")


    # Print summary
    print("\nSummary Table of Metrics:\n")
    print(summary_df.to_string(index=False))
    print("\nInterpretation Guide:\n")
    print("Gini Index (single distributions):")
    print("- Closer to 0: More even/egalitarian distribution across age bins.")
    print("- Closer to 1: More unequal/skewed distribution.\n")
    print("Wasserstein Distance and KL Divergence (pairwise comparisons):")
    print("- Wasserstein Distance: 0 means identical distributions. Larger means more differing.")
    print("- KL Divergence: 0 means identical distributions. Larger means more divergence.\n")

    print("Comparisons:")
    print("- 'Male Actors vs Female Actors' measures difference in age distributions between male and female actors.")
    print("- 'Male Real vs Female Real' measures difference between male and female real-world populations.")
    print("- 'Male Actors vs Male Real' measures how male actors' ages differ from the male real population.")
    print("- 'Female Actors vs Female Real' measures how female actors' ages differ from the female real population.\n")

    print("Detailed Metrics:")
    print(f"Wasserstein Distance (Male Actors vs Female Actors): {wasserstein_male_female_actors:.2f}")
    print(f"KL Divergence (Male Actors vs Female Actors): {kl_div_male_female_actors:.2f}")
    print(f"Wasserstein Distance (Male Real vs Female Real): {wasserstein_male_female_real:.2f}")
    print(f"KL Divergence (Male Real vs Female Real): {kl_div_male_female_real:.2f}")
    print(f"Wasserstein Distance (Male Actors vs Male Real): {wasserstein_male_actor_real:.2f}")
    print(f"KL Divergence (Male Actors vs Male Real): {kl_div_male_actor_real:.2f}")
    print(f"Wasserstein Distance (Female Actors vs Female Real): {wasserstein_female_actor_real:.2f}")
    print(f"KL Divergence (Female Actors vs Female Real): {kl_div_female_actor_real:.2f}")

