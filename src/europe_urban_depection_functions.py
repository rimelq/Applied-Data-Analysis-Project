
def create_and_save_context_dictionaries( wordnet , output_dir= "./europe_skipgram/dictionaries/" ):
    """
    Create and save urban, intermediate, and rural dictionaries as .txt files.
    
    Parameters:
        output_dir (str): Directory to save the dictionaries.
        
    Returns:
        None
    """
    import os

    # Helper function to expand seed words
    def expand_seed_words(seed_words):
        expanded_words = set(seed_words)
        for word in seed_words:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    expanded_words.add(lemma.name().replace('_', ' '))
        return expanded_words

    # Seed words for each context type
    urban_seed = [
    "city", "urban", "metropolis", "downtown", "suburb", "metropolitan", 
    "skyscraper", "apartment", "tower", "street", "capital", "municipal",
    "cityscape", "urban sprawl", "concrete jungle", "commuter", "infrastructure",
    "high-rise", "mall", "plaza", "station", "factory", "urban center", 
    "central business district", "hub", "traffic", "industrial area", 
    "alley", "boulevard", "ghetto", "inner city", "megacity", "urban district",
    "cosmopolitan"
    ]

    intermediate_seed = [
        "town", "suburb", "suburban", "residential", "commuter town", 
        "municipality", "district", "neighborhood", "community", "settlement",
        "borough", "township", "outskirts", "semi-urban", "small town", "locality",
        "village center", "market town", "main street", "crossroads", 
        "urban fringe", "hamlet", "civic center", "regional hub", "provincial center",
        "borderland", "periphery", "mixed-use area", "sprawl zone"
    ]
    
    
    rural_seed = [
        "rural", "village", "countryside", "farm", "agricultural", "pastoral",
        "hamlet", "farmland", "field", "farming", "ranch", "cottage", 
        "provincial", "rustic", "remote", "wilderness", "forest", "meadow",
        "orchard", "barn", "watermill", "dirt road", "valley", "shepherd",
        "plow", "haystack", "hillside", "grazing", "homestead", "woodland", 
        "rural district", "grassland", "backcountry", "vineyard", "paddock",
        "idyll", "arable land", "foothills"
    ]

    # Expand dictionaries
    urban_dict = expand_seed_words(urban_seed)
    intermediate_dict = expand_seed_words(intermediate_seed)
    rural_dict = expand_seed_words(rural_seed)

    # Save dictionaries as .txt files
    with open(os.path.join(output_dir, "urban_dictionary.txt"), "w") as urban_file:
        urban_file.write("\n".join(sorted(urban_dict)))
    with open(os.path.join(output_dir, "intermediate_dictionary.txt"), "w") as intermediate_file:
        intermediate_file.write("\n".join(sorted(intermediate_dict)))
    with open(os.path.join(output_dir, "rural_dictionary.txt"), "w") as rural_file:
        rural_file.write("\n".join(sorted(rural_dict)))
    
    print("Urban Dictionary:", len(urban_dict), "words.")
    print(f"Urban dictionary saved to {output_dir}urban_dictionary.txt")
    print("Intermediate Dictionary:", len(intermediate_dict), "words.")
    print(f"Intermediate dictionary saved to {output_dir}intermediate_dictionary.txt")
    print("Rural Dictionary:", len(rural_dict), "words.")
    print(f"Rural dictionary saved to {output_dir}rural_dictionary.txt")


def extract_and_save_europe_movies(movie_metadata, output_file="european_movies_with_summaries.csv"):
    """
    Extract movies from European countries and save the data to a CSV file.

    Parameters:
        movie_metadata (DataFrame): The DataFrame containing movie metadata.
        output_file (str): The file path to save the European movies data.

    Returns:
        None
    """
    # List of European countries
    european_countries = [
        "France", "Germany", "Italy", "Spain", "United Kingdom", "Poland", 
        "Romania", "Netherlands", "Belgium", "Greece", "Czech Republic", 
        "Portugal", "Sweden", "Hungary", "Austria", "Switzerland", "Bulgaria", 
        "Denmark", "Finland", "Slovakia", "Norway", "Ireland", "Croatia", 
        "Moldova", "Bosnia", "Albania", "Lithuania", "Slovenia", "Latvia", 
        "Estonia", "Iceland", "Luxembourg", "Montenegro", "Malta", "Andorra"
    ]

    # Filter for European movies
    european_movies = movie_metadata[
        movie_metadata['Movie countries'].str.contains('|'.join(european_countries), na=False, case=False)
    ]

    # Save the filtered DataFrame to a CSV file
    european_movies.to_csv(output_file, index=False)

    print(f"European movies data saved to {output_file}")



import pandas as pd
import plotly.express as px
import re
import nltk
from nltk.corpus import wordnet
# Function to load the data and create the plots with the given template
def plot_setting_representation(output_file="setting_representation_by_year.html"):
    """
    Analyzes the representation of urban, intermediate, and rural settings in European cinema and creates plots.

    Parameters:
        output_file (str): The base file path to save the plots.

    Returns:
        None
    """
    import pandas as pd
    import plotly.express as px
    import re

    # Load dictionaries
    with open("./europe_skipgram/dictionaries/urban_dictionary.txt") as file:
        urban_dict = set(file.read().splitlines())
    with open("./europe_skipgram/dictionaries/intermediate_dictionary.txt") as file:
        intermediate_dict = set(file.read().splitlines())
    with open("./europe_skipgram/dictionaries/rural_dictionary.txt") as file:
        rural_dict = set(file.read().splitlines())

    # Load the data
    european_with_summaries = pd.read_csv("./europe_skipgram/european_movies_with_summaries.csv")

    # Function to tokenize and count keywords in the summary
    def count_class_keywords(summary, keyword_dict):
        tokens = re.findall(r'\b\w+\b', summary.lower())
        return sum(1 for word in tokens if word in keyword_dict)

    # Add keyword counts for each category
    european_with_summaries['urban_keyword_count'] = european_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, urban_dict))
    european_with_summaries['intermediate_keyword_count'] = european_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, intermediate_dict))
    european_with_summaries['rural_keyword_count'] = european_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, rural_dict))

    # Extract and clean release year
    european_with_summaries['release_year'] = pd.to_numeric(
        european_with_summaries['Movie release date'].astype(str).str[:4], errors='coerce')
    european_with_summaries = european_with_summaries.dropna(subset=['release_year'])
    european_with_summaries['release_year'] = european_with_summaries['release_year'].astype(int)

    # Filter movies by keyword thresholds
    urban_movies = european_with_summaries[european_with_summaries['urban_keyword_count'] > 3]
    intermediate_movies = european_with_summaries[european_with_summaries['intermediate_keyword_count'] > 2]
    rural_movies = european_with_summaries[european_with_summaries['rural_keyword_count'] > 3]

    # Prepare yearly data
    def prepare_yearly_data():
        urban_by_year = urban_movies.groupby('release_year').size()
        intermediate_by_year = intermediate_movies.groupby('release_year').size()
        rural_by_year = rural_movies.groupby('release_year').size()

        return pd.DataFrame({
            'Urban (9.9%)': urban_by_year,
            'Intermediate (50.4%)': intermediate_by_year,
            'Rural (39.8%)': rural_by_year
        }).fillna(0)

    yearly_data = prepare_yearly_data()

    # Plot 1: Setting representation over time
    fig1 = px.line(yearly_data.reset_index(), 
                   x='release_year', 
                   y=['Urban (9.9%)', 'Intermediate (50.4%)', 'Rural (39.8%)'],
                   title="<b>Evolution of Setting<br> Representation in European Cinema</b>",
                   labels={'release_year': 'Year', 'value': 'Number of Movies'},
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
    ))
    fig1.write_html(output_file.replace('.html', '_time.html'))
    fig1.show()

    # Calculate overall percentages
    total_movies = len(urban_movies) + len(intermediate_movies) + len(rural_movies)
    movie_percentages = pd.DataFrame({
        'Setting': ['Urban', 'Intermediate', 'Rural'],
        'Movie Representation (%)': [
            len(urban_movies) / total_movies * 100,
            len(intermediate_movies) / total_movies * 100,
            len(rural_movies) / total_movies * 100
        ],
        'Real Land Area (%)': [9.9, 50.4, 39.8]
    })

    # Plot 2: Representation vs Real Land Area
    fig2 = px.bar(movie_percentages,
                  x='Setting',
                  y=['Movie Representation (%)', 'Real Land Area (%)'],
                  title="<b>Movie Representation vs<br> Real Land Area</b>",
                  barmode='group',
                  template="plotly_white",
                  color_discrete_sequence=["#009392", "#e88471", "#9ccb86"])

    fig2.update_layout(
              plot_bgcolor="#F6f0f0",
              paper_bgcolor=" #F6f0f0",
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
    fig2.write_html(output_file.replace('.html', '_comparison.html'))
    fig2.show()

    # Analyze representation by decade
    def analyze_by_decade(movies_df):
        movies_df['decade'] = (movies_df['release_year'] // 10) * 10
        return movies_df.groupby('decade').size()

    decades_data = pd.DataFrame({
        'Urban': analyze_by_decade(urban_movies),
        'Intermediate': analyze_by_decade(intermediate_movies),
        'Rural': analyze_by_decade(rural_movies)
    }).fillna(0)

    # Plot 3: Representation by Decade
    fig3 = px.bar(decades_data.reset_index(),
                  x='decade',
                  y=['Urban', 'Intermediate', 'Rural'],
                  title="<b>Setting Representation by Decade</b>",
                  labels={'decade': 'Decade', 'value': 'Number of Movies'},
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
    fig3.write_html(output_file.replace('.html', '_decade.html'))
    fig3.show()
    print(f"Plots saved as '{output_file.replace('.html', '_time.html')}', "
          f"'{output_file.replace('.html', '_comparison.html')}', "
          f"and '{output_file.replace('.html', '_decade.html')}'.")

