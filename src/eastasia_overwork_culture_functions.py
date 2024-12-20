def create_and_save_overwork_and_balance_dictionaries(wordnet, output_dir="dictionaries"):
    """
    Creates and saves expanded dictionaries for overwork-related and work-life balance-related keywords.

    Parameters:
        output_dir (str): Directory to save the dictionaries as text files.

    Returns:
        None
    """

    import os

    # Function to expand seed words using WordNet
    def expand_seed_words(seed_words):
        expanded_words = set(seed_words)
        for word in seed_words:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    expanded_words.add(lemma.name().replace('_', ' '))
        return expanded_words

    # Define overwork-related seed words
    overwork_seed = [
        "overtime", "late night", "overwork", "workaholic", "exhaustion",
        "karoshi", "gwarosa", "996", "burnout", "deadline",
        "office", "salary", "promotion", "boss", "manager",
        "corporate", "company", "overtime", "workplace", "employee",
        "stress", "pressure", "suicide", "depression", "fatigue",
        "exhausted", "tired", "work-life", "family time", "marriage",
        "career", "success", "promotion", "status", "achievement",
        "competition", "performance", "evaluation", "bonus", "raise"
    ]

    # Define work-life balance-related seed words
    balance_seed = [
        "family", "leisure", "hobby", "vacation", "rest",
        "relaxation", "weekend", "holiday", "personal time", "break",
        "life", "happiness", "freedom", "balance", "health"
    ]

    # Expand dictionaries
    overwork_dict = expand_seed_words(overwork_seed)
    balance_dict = expand_seed_words(balance_seed)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the dictionaries as text files
    overwork_file = os.path.join(output_dir, "overwork_dictionary.txt")
    balance_file = os.path.join(output_dir, "balance_dictionary.txt")

    with open(overwork_file, "w") as file:
        file.write("\n".join(sorted(overwork_dict)))

    with open(balance_file, "w") as file:
        file.write("\n".join(sorted(balance_dict)))

    print(f"Overwork Dictionary saved to {overwork_file}")
    print(f"Balance Dictionary saved to {balance_file}")
    print("Overwork Dictionary:", len(overwork_dict), "words.")
    print("Balance Dictionary:", len(balance_dict), "words.")


import pandas as pd

def extract_and_save_eastasian_movies(movie_metadata, output_file="eastasian_movies.csv"):
    """
    Extracts movies from East Asian countries and saves them to a CSV file.

    Parameters:
        movie_metadata (DataFrame): The movie metadata DataFrame.
        output_file (str): Path to save the extracted East Asian movies.

    Returns:
        DataFrame: A DataFrame containing movies from East Asian countries.
    """
    # Define East Asian countries
    eastasian_countries = [
        "Japan", "China", "South Korea", "Taiwan", 
        "Hong Kong", "Macau", "Mongolia"
    ]

    # Filter movies where the country is in the list of East Asian countries
    eastasian_movies = movie_metadata[
        movie_metadata['Movie countries'].str.contains('|'.join(eastasian_countries), 
                                                        na=False, case=False)
    ]

    # Save the extracted DataFrame to a CSV file
    eastasian_movies.to_csv(output_file, index=False)

    print(f"East Asian movies saved to {output_file}")
    return eastasian_movies
# Function to process East Asian themes and create visualizations with a consistent template
def process_eastasian_themes(re, px, pd, output_file="eastasian_theme_analysis.html"):
    """
    Analyze work-related themes in East Asian movies and create visualizations.

    Parameters:
        output_file (str): Path to save the interactive HTML output file.

    Returns:
        None
    """
    import pandas as pd
    import plotly.express as px
    import re

    # Load dictionaries
    with open("dictionaries\\overwork_dictionary.txt") as file:
        overwork_dict = set(file.read().splitlines())
    with open("dictionaries\\balance_dictionary.txt") as file:
        balance_dict = set(file.read().splitlines())

    # Load data
    eastasian_with_summaries = pd.read_csv("eastasian_movies.csv")

    # Function to tokenize and count keywords in the summary
    def count_class_keywords(summary, keyword_dict):
        tokens = re.findall(r'\b\w+\b', summary.lower())
        return sum(1 for word in tokens if word in keyword_dict)

    # Add columns to count keywords for each setting type
    eastasian_with_summaries['overwork_keyword_count'] = eastasian_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, overwork_dict))
    eastasian_with_summaries['balance_keyword_count'] = eastasian_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, balance_dict))

    # Extract year from the "Movie release date" column
    eastasian_with_summaries['release_year'] = pd.to_numeric(
        eastasian_with_summaries['Movie release date'].astype(str).str[:4], errors='coerce'
    )
    eastasian_with_summaries = eastasian_with_summaries.dropna(subset=['release_year'])
    eastasian_with_summaries['release_year'] = eastasian_with_summaries['release_year'].astype(int)

    # Filter movies based on keyword thresholds
    overwork_movies = eastasian_with_summaries[eastasian_with_summaries['overwork_keyword_count'] > 7]
    balance_movies = eastasian_with_summaries[eastasian_with_summaries['balance_keyword_count'] > 9]

    # Calculate yearly counts for both themes
    def analyze_themes_over_time():
        overwork_by_year = overwork_movies.groupby('release_year').size()
        balance_by_year = balance_movies.groupby('release_year').size()
        return pd.DataFrame({'Overwork Theme': overwork_by_year, 'Work-Life Balance Theme': balance_by_year}).fillna(0)

    yearly_data = analyze_themes_over_time()

    # Plot 1: Evolution of work-related themes over time
    fig1 = px.line(
        yearly_data.reset_index(),
        x='release_year',
        y=['Overwork Theme', 'Work-Life Balance Theme'],
        title="<b>Evolution of Work-Related Themes<br> in East Asian Cinema</b>",
        labels={'release_year': 'Year', 'value': 'Number of Movies', 'variable': 'Theme'},
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#009392", "#e88471", "#9ccb86"])
    
    fig1.update_layout(
        plot_bgcolor="#F6f0f0",
        paper_bgcolor="#F6f0f0",
        font=dict(color="black"),
        legend=dict(
        orientation="h",  
        y=1.1,            
        x=0.5,            
        xanchor="center", 
         ),
        title=dict(
        font=dict(size=14),  
        x=0.5,  
        xanchor="center"
    )
    )
    fig1.show()
    fig1.write_html(output_file.replace('.html', '_themes_over_time.html'))

    # Plot 2: Work hours vs overwork movies
    def count_movies_by_country(df, country):
        return len(df[df['Movie countries'].str.contains(country, na=False, case=False)])

    fig2 = px.bar(
        data_frame=pd.DataFrame({
            'Country': ['Japan', 'South Korea', 'China'],
            'Work Hours (normalized)': [1607 / 2096 * 100, 1896 / 2096 * 100, 100],
            'Overwork Movies (%)': [
                count_movies_by_country(overwork_movies, 'Japan') / len(overwork_movies) * 100,
                count_movies_by_country(overwork_movies, 'South Korea') / len(overwork_movies) * 100,
                count_movies_by_country(overwork_movies, 'China') / len(overwork_movies) * 100
            ]
        }),
        x='Country',
        y=['Work Hours (normalized)', 'Overwork Movies (%)'],
        title="<b>Work Hours vs <br>Overwork Movie Representation (%)</b>",
        barmode='group',
        template="plotly_white",
        color_discrete_sequence=["#009392", "#e88471", "#9ccb86"])
    
    fig2.update_layout(
        plot_bgcolor="#F6f0f0",
        paper_bgcolor="#F6f0f0",
        font=dict(color="black"),
        legend=dict(
        orientation="h",  
        y=1.1,            
        x=0.5,            
        xanchor="center", 
         ),
        title=dict(
        font=dict(size=14),  
        x=0.5,  
        xanchor="center"
    )
    )
    fig2.show()
    fig2.write_html(output_file.replace('.html', '_work_hours.html'))


    # Plot 3: Long working hours vs work-life balance movies
    fig3 = px.bar(
        data_frame=pd.DataFrame({
            'Country': ['Japan', 'South Korea', 'China'],
            'Long Hours %': [10.1, 15.2, 20.5],
            'Work-Life Balance Movies (%)': [
                count_movies_by_country(balance_movies, 'Japan') / len(balance_movies) * 100,
                count_movies_by_country(balance_movies, 'South Korea') / len(balance_movies) * 100,
                count_movies_by_country(balance_movies, 'China') / len(balance_movies) * 100
            ]
        }),
        x='Country',
        y=['Long Hours %', 'Work-Life Balance Movies (%)'],
        title="<b>Long Working Hours vs<br> Work-Life Balance Movies (%)</b>",
        barmode='group',
        template="plotly_white", 
        color_discrete_sequence=["#009392", "#e88471", "#9ccb86"])

    fig3.update_layout(
        plot_bgcolor="#F6f0f0",
        paper_bgcolor="#F6f0f0",
        font=dict(color="black"),
        legend=dict(
             orientation="h",  
             y=1.1,            
             x=0.5,            
             xanchor="center", 
             ),
        title=dict(
        font=dict(size=14),  
        x=0.5,  
        xanchor="center"
    )
    )
    fig3.show()
    fig3.write_html(output_file.replace('.html', '_work_life_balance.html'))

    print(f"Plots saved as:\n"
          f"'{output_file.replace('.html', '_themes_over_time.html')}'\n"
          f"'{output_file.replace('.html', '_work_hours.html')}'\n"
          f"'{output_file.replace('.html', '_work_life_balance.html')}'")
