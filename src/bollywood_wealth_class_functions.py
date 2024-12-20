def create_and_save_dicts(wordnet):
    """
    Creates expanded dictionaries for Top 10%, Middle 40%, and Bottom 50% socio-economic classes
    and saves them to text files.
    """

    # Function to expand seed words using WordNet
    def expand_seed_words(seed_words):
        expanded_words = set(seed_words)
        for word in seed_words:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    expanded_words.add(lemma.name().replace('_', ' '))
        return expanded_words

    # Seed words for each class
    top_10_seed = [
        "rich", "luxury", "wealthy", "millionaire", "billionaire", "elite", "affluent", "aristocrat", 
        "opulent", "high-class", "magnate", "tycoon", "lavish", "extravagant", "luxurious", 
        "plutocrat", "prosperous", "privileged", "upper-class", "business magnate", "capitalist", 
        "investor", "CEO", "entrepreneur", "heir", "socialite"
    ]
    middle_40_seed = [
        "middle-class", "working-class", "office worker", "teacher", "employee", "white-collar", 
        "professional", "manager", "supervisor", "blue-collar", "technician", "clerk", 
        "middle-income", "moderate-income", "suburban", "household income", "salaried", 
        "skilled worker", "service sector", "civil servant", "nurse", "engineer", "middle-class family"
    ]
    bottom_50_seed = [
        "poverty", "slum", "village", "farmer", "starvation", "poor", "destitute", "underprivileged", 
        "low-income", "indigent", "impoverished", "homeless", "downtrodden", "rural", "agrarian", 
        "manual laborer", "working poor", "subsistence farming", "villager", "day laborer", "shelter",
        "migrant worker", "shanty", "informal settlement", "tenant farmer", "peasant", "tough",
        "landless laborer", "unskilled laborer", "poverty-stricken", "underclass", "hard", "humiliation"
    ]

    # Expand dictionaries
    top_10_dict = expand_seed_words(top_10_seed)
    middle_40_dict = expand_seed_words(middle_40_seed)
    bottom_50_dict = expand_seed_words(bottom_50_seed)

    # Save dictionaries to text files
    with open("./bollywood_skipgram/top_10_dictionary.txt", "w") as file:
        file.write("\n".join(sorted(top_10_dict)))
    with open("./bollywood_skipgram/middle_40_dictionary.txt", "w") as file:
        file.write("\n".join(sorted(middle_40_dict)))
    with open("./bollywood_skipgram/bottom_50_dictionary.txt", "w") as file:
        file.write("\n".join(sorted(bottom_50_dict)))

    # Print confirmation and sizes
    print("Dictionaries created and saved:")
    print(f"Top 10% Dictionary: {len(top_10_dict)} words.")
    print(f"Middle 40% Dictionary: {len(middle_40_dict)} words.")
    print(f"Bottom 50% Dictionary: {len(bottom_50_dict)} words.")

def analyze_wealth_class_representation(pd, re, px, output_file="./bollywood_skipgram/wealth_class_analysis_bollywood.html"):
    """
    Analyzes wealth class representation in Bollywood movies and creates visualizations.

    Parameters:
        bollywood_with_summaries (DataFrame): Bollywood movie data with summaries.
        top_10_dict (set): Dictionary for Top 10% keywords.
        middle_40_dict (set): Dictionary for Middle 40% keywords.
        bottom_50_dict (set): Dictionary for Bottom 50% keywords.
        output_file (str): Path to save the output HTML file with the plot.

    Returns:
        None
    """

     # Load dictionaries
    with open("./bollywood_skipgram/top_10_dictionary.txt") as file:
        top_10_dict = set(file.read().splitlines())
    with open("./bollywood_skipgram/middle_40_dictionary.txt") as file:
        middle_40_dict = set(file.read().splitlines())
    with open("./bollywood_skipgram/bottom_50_dictionary.txt") as file:
        bottom_50_dict = set(file.read().splitlines())
    # Load data
    bollywood_with_summaries = pd.read_csv("./bollywood_skipgram/bollywood_with_summaries.csv")
    
    # Function to tokenize and count keywords in the summary
    def count_class_keywords(summary, keyword_dict):
        tokens = re.findall(r'\b\w+\b', summary.lower())
        return sum(1 for word in tokens if word in keyword_dict)

    # Add columns to count keywords for each class
    bollywood_with_summaries['top_10_keyword_count'] = bollywood_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, top_10_dict))
    bollywood_with_summaries['middle_40_keyword_count'] = bollywood_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, middle_40_dict))
    bollywood_with_summaries['bottom_50_keyword_count'] = bollywood_with_summaries['Summary'].apply(
        lambda x: count_class_keywords(x, bottom_50_dict))

    # Extract year from the "Movie release date" column
    bollywood_with_summaries['release_year'] = bollywood_with_summaries['Movie release date'].astype(str).str[:4]
    bollywood_with_summaries['release_year'] = pd.to_numeric(bollywood_with_summaries['release_year'], errors='coerce')
    bollywood_with_summaries = bollywood_with_summaries.dropna(subset=['release_year'])
    bollywood_with_summaries['release_year'] = bollywood_with_summaries['release_year'].astype(int)

    # Filter movies based on keyword count thresholds
    top_10_movies = bollywood_with_summaries[bollywood_with_summaries['top_10_keyword_count'] > 3]
    middle_40_movies = bollywood_with_summaries[bollywood_with_summaries['middle_40_keyword_count'] > 3]
    bottom_50_movies = bollywood_with_summaries[bollywood_with_summaries['bottom_50_keyword_count'] > 3]

    # Count total movies for each class
    movies_distribution = pd.DataFrame({
        'Class': ['Top 10%', 'Middle 40%', 'Bottom 50%'],
        'Number of Movies': [
            len(top_10_movies),
            len(middle_40_movies),
            len(bottom_50_movies)
        ]
    })

    # Group by release year and count movies
    top_10_by_year = top_10_movies.groupby('release_year').size()
    middle_40_by_year = middle_40_movies.groupby('release_year').size()
    bottom_50_by_year = bottom_50_movies.groupby('release_year').size()

    # Combine yearly counts into a single DataFrame
    class_representation_by_year = pd.DataFrame({
        'Year': top_10_by_year.index,
        'Top 10%': top_10_by_year.values,
        'Middle 40%': middle_40_by_year.reindex(top_10_by_year.index, fill_value=0).values,
        'Bottom 50%': bottom_50_by_year.reindex(top_10_by_year.index, fill_value=0).values
    }).set_index('Year').reset_index()

    # Plot: Class representation over the years
    fig = px.line(
        class_representation_by_year,
        x='Year',
        y=['Top 10%', 'Middle 40%', 'Bottom 50%'],
        labels={'value': 'Number of Movies', 'variable': 'Class Representation'},
        title="<b>Class Representation in <br>Bollywood Movies Over the Years</b>",
        color_discrete_sequence=["#009392", "#5c1165", "#cf597e"],
        template="plotly_white"
    )

    # Customize layout
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        plot_bgcolor="#F6f0f0",
        paper_bgcolor="#F6f0f0",
        font=dict(color="black"),
        xaxis_title="Year",
        yaxis_title="Number of Movies",
        legend_title="Class Representation",
        hovermode="x unified",
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

    fig.show()
    fig.write_html(output_file)

    # Print summary
    print("Analysis complete.")
    print(f"Total Top 10% Movies: {len(top_10_movies)}")
    print(f"Total Middle 40% Movies: {len(middle_40_movies)}")
    print(f"Total Bottom 50% Movies: {len(bottom_50_movies)}")
    print(f"Interactive plot saved as '{output_file}'")

