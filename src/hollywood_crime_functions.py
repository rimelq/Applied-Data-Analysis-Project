def generate_and_save_crime_dictionary(wordnet, output_file="crime/crime_dictionary.txt"):
    """
    Generate an expanded crime-related dictionary using WordNet and save it to a file.
    
    Parameters:
        output_file (str): Path to save the generated crime dictionary.
    """
    
    # Seed terms for the crime theme
    crime_seed_terms = [
        # General terms for crime
        "crime", "criminal", "felony", "misdemeanor", "offense", "illegal", "lawbreaking",
        
        # Specific crimes
        "murder", "homicide", "theft", "robbery", "burglary", "fraud", "embezzlement", 
        "arson", "assault", "kidnapping", "smuggling", "blackmail", "extortion", "bribery",
        "drug trafficking", "poaching", "manslaughter", "cybercrime", "vandalism", "piracy", "drugs",
        
        # Violence and related terms
        "violence", "abuse", "gang", "shooting", "stabbing", "riot", "terrorism", 
        "massacre", "domestic violence", "terror",
        
        # Law enforcement and punishment
        "prison", "jail", "arrest", "convict", "detention", "sentence", "prosecution", 
        "court", "trial", "police", "detective", "investigation", "bail", "parole",
        
        # Criminal types and roles
        "thief", "robber", "murderer", "fraudster", "con artist", "hacker", "smuggler",
        "drug dealer", "arsonist", "kidnapper", "assailant", "terrorist", "vandal", 
        "gangster", "hitman",
        
        # Organized crime
        "mafia", "cartel", "underworld", "trafficking",
        
        # Corruption and political crime
        "corruption", "bribery", "scandal", "cover-up", "money laundering", 
        "racketeering", "tax evasion"
    ]

    # Function to fetch related terms from WordNet
    def expand_terms(seed_terms):
        expanded_terms = set()
        for term in seed_terms:
            for synset in wordnet.synsets(term):
                for lemma in synset.lemmas():
                    expanded_terms.add(lemma.name().lower().replace("_", " "))  # Normalize terms
        return expanded_terms

    # Expand the crime seed terms
    crime_lexicon = expand_terms(crime_seed_terms)

    # Save the expanded lexicon to a file
    with open(output_file, "w", encoding="utf-8") as file:
        # Sort terms for consistency
        file.write("\n".join(sorted(crime_lexicon)))  

    print(f"Crime dictionary saved successfully to '{output_file}'")
    print(f"Total terms in the crime dictionary: {len(crime_lexicon)}")

def extract_and_save_hollywood_movies(ast, movie_metadata, plot_summaries, output_file="hollywood_movies_with_summaries.csv"):
    """
    Extract Hollywood movies (USA and Canada), merge with plot summaries, and save the result to a CSV file.

    Parameters:
        movie_metadata (DataFrame): DataFrame containing movie metadata with 'Movie countries' and 'Wikipedia movie ID'.
        plot_summaries (DataFrame): DataFrame containing movie plot summaries with 'Wikipedia movie ID'.
        output_file (str): Path to save the merged Hollywood movies dataset.
    """
    
    # Function to extract countries from 'Movie countries' column
    def extract_countries(country_str):
        try:
            country_dict = ast.literal_eval(country_str) 
            return list(country_dict.values())  
        except:
            return []  
    
    # Function to check if a movie is a Hollywood movie
    def is_hollywood_movie(countries):
        return "United States of America" in countries or "Canada" in countries
    
    # Extract countries
    movie_metadata["Parsed countries"] = movie_metadata["Movie countries"].apply(extract_countries)
    
    # Filter 
    hollywood_movies = movie_metadata[movie_metadata["Parsed countries"].apply(is_hollywood_movie)]
    
    # Drop the 'Parsed countries' column to clean up the dataset
    hollywood_movies = hollywood_movies.drop(columns=["Parsed countries"])
    
    # Merge 
    hollywood_with_summaries = hollywood_movies.merge(plot_summaries, on="Wikipedia movie ID", how="inner")
    
    # Save to a CSV file
    hollywood_with_summaries.to_csv(output_file, index=False)
    
    print("Hollywood Movies with Summaries:", hollywood_with_summaries.shape)
    display(hollywood_with_summaries.head(1))

    print(f"Hollywood movies with summaries saved to: {output_file}")


def extract_and_plot_crime_movies( hollywood_with_summaries, crime_dictionary, output_file1 ="crime_movies_distribution.html", output_file2 = 'crime_movies_percentage.html'):
    """
    Extract crime-related Hollywood movies, analyze their distribution over years, and plot results.
    
    Parameters:
        movie_metadata (DataFrame): DataFrame containing movie metadata.
        plot_summaries (DataFrame): DataFrame containing movie summaries.
        crime_dictionary_file (str): Path to the crime dictionary file.
        output_file (str): Path to save the HTML plot.
    """
    import pandas as pd
    import plotly.express as px

    # Count crime-related keywords in summaries
    def tokenize_and_count(summary, theme_dict):
        tokens = summary.lower().split()
        return sum(1 for word in tokens if word in theme_dict)
    
    hollywood_with_summaries['crime_keyword_count'] = hollywood_with_summaries['Summary'].apply(
        lambda x: tokenize_and_count(x, crime_dictionary)
    )

    # Filter crime-related movies (threshold of 15 crime-related words)
    crime_related_movies = hollywood_with_summaries[hollywood_with_summaries['crime_keyword_count'] > 10].copy()
    
    # Extract year from the release date
    crime_related_movies['release_year'] = crime_related_movies['Movie release date'].astype(str).str[:4]
    crime_related_movies['release_year'] = pd.to_numeric(crime_related_movies['release_year'], errors='coerce')
    crime_related_movies = crime_related_movies.dropna(subset=['release_year']).astype({'release_year': 'int'})

    # Extract year from the release date
    hollywood_with_summaries['release_year'] = hollywood_with_summaries['Movie release date'].astype(str).str[:4]
    hollywood_with_summaries['release_year'] = pd.to_numeric(hollywood_with_summaries['release_year'], errors='coerce')
    hollywood_with_summaries = hollywood_with_summaries.dropna(subset=['release_year']).astype({'release_year': 'int'})
    
    # Group by year and calculate percentage
    total_movies_per_year = hollywood_with_summaries['release_year'].value_counts().sort_index()
    crime_movies_per_year = crime_related_movies['release_year'].value_counts().sort_index()
    crime_percentage = (crime_movies_per_year / total_movies_per_year * 100).fillna(0).reset_index()
    crime_percentage.columns = ['Year', 'Crime Movie Percentage']

    # Plot the percentage of crime movies
    fig_percentage = px.line(
        crime_percentage,
        x="Year",
        y="Crime Movie Percentage",
        title="<b>Percentage of Crime Movies Overall Movies Over the Years</b>",
        labels={"Year": "Year", "Crime Movie Percentage": "Percentage (%)"},
        template="plotly_white"
    )
    fig_percentage.update_layout(
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0",
        font=dict(color="black")
    )

    fig_percentage.show()
    fig_percentage.write_html(output_file2)
    print(f"Crime movie percentage plot saved as '{output_file2}'")

    # Plot the raw number of crime movies
    crime_movies_count = crime_related_movies['release_year'].value_counts().sort_index().reset_index()
    crime_movies_count.columns = ['Year', 'Number of Crime Movies']

    fig_count = px.bar(
        crime_movies_count,
        x="Year",
        y="Number of Crime Movies",
        title="<b>Number of Crime Movies Over the Years</b>",
        labels={"Year": "Year", "Number of Crime Movies": "Number of Crime Movies"},
        template="plotly_white"
    )
    fig_count.update_layout(
        plot_bgcolor="#F2F0F0",
        paper_bgcolor="#F2F0F0",
        font=dict(color="black")
    )

    fig_count.show()
    fig_count.write_html(output_file1)

    print(f"Crime movie distribution plot saved as '{output_file1}'")
