
# **From Script to reality: Does Cinema Mirror Life or Rewrite It**

## **Abstract**

Cinema has always served as a lens through which society is reflected—or distorted. This project investigates whether the cinematic world aligns with real-world demographics in terms of gender, ethnicity, and age, or whether it reinforces outdated stereotypes. By comparing on-screen representation to societal expectations across genres and regions, we aim to highlight discrepancies and explore their potential implications. Our analysis will compare demographic representation not only by region but also across major film industries such as Hollywood, Bollywood, and others. Beyond identifying these disparities, we will examine trends over time and consider data-driven proposals to address them. 

---

## **Research Questions**

Representation accuracy and trends:

1. How accurately does cinema reflect real-world gender, ethnicity, and age demographics?
2. What trends can be identified in cinematic representation over time?

Conclusive question: 

3. Are the largest demographic discrepancies linked to box office revenue?    

---

## **Data Processing**

### **Why Start from 1950?**  
We chose 1950 as our starting point, the era of classics like *Pather Panchali* and *Sunset Boulevard* because this period marks the availability of consistent demographic data and represents the beginning of the "contemporary" world. It also coincides with significant transformations in global cinema, including the rise of major film industries and the globalization of filmmaking.

---

### **Ethnicity Representation Across Film Industries**
The Hollywood film industry is often considered representative of North America, while Bollywood plays a similar role for South Asia. Our analysis extends to other regions such as East Asia and Europe to provide a comprehensive understanding of how cinematic industries reflect (or diverge from) the demographics of their associated populations.

1. **Data Sources**:  
   - Ethnicity data for North America was sourced from the [EPR Core dataset](https://icr.ethz.ch/data/epr/core/), providing population breakdowns over time.  
   - Jewish-American population data was added from [Pew Research 2013](https://www.pewresearch.org/religion/2013/10/01/chapter-1-population-estimates/) and [Pew Research 2021](https://www.pewresearch.org/religion/2021/05/11/the-size-of-the-u-s-jewish-population/) due to their historical significance in Hollywood.
     
2. **Adjustments for Analysis**:  
   - Limited ethnic categorization in some regions led us to focus on the largest contributing country within each industry when necessary.  
   - In the Bollywood analysis, we focused on how Indian Bollywood movies represent Indian ethnicities compared to the real world. Bollywood actors with non-Indian ethnicities (less than 1% of the data) were excluded to maintain this focus.
   - In the Europe Analysis, we took premade data from the web as the real-world dataset was not focused on ethnicities but nationnalities for the european countries.
  
[Our reaction after preprocessing the ethnicities](meme.jpg)

### **Time Fragmentation**:  
   - Ethnicity data was divided into four time periods for consistency across all regions and industries:  
     - **1950–1965**  
     - **1966–1980**  
     - **1981–1995**  
     - **1996–2012**  

---

### **Gender and Age Representation**
1. **Real-World Data**:  
   Gender and age data was obtained from the [UN World Population Prospects dataset](https://population.un.org/wpp/), covering major regions associated with key film industries.

2. **Representation Baselines**:  
   - The dataset was segmented into the same time periods as the ethnicity analysis.  
   - Age distributions were further divided into five-year intervals to facilitate granular comparisons between real-world populations and on-screen demographics.  

---

## **Methods**

1. **Data Preprocessing**:  
   - Clean and preprocess demographic data from `character.metadata.tsv`, `movie.metadata.tsv`, and real-world datasets.  
   - Standardize formats to ensure consistency across regions and industries.
   - With over 70% missing values in *actor_ethnicity* overall, we explored **web scraping** to supplement the data. We scraped from both **Wikidata** and **Ethnicelebs**, though Ethnicelebs provided limited information. Wikidata, however, yielded promising results. While we haven’t integrated these values yet, we may consider using the Wikidata results in P3 to improve data completeness. (The file containing the tests for the web scraping process can be found in test/scrap.ipynb.)

2. **Comparative Analysis**:  
   - Compare on-screen demographics to real-world populations, highlighting differences across genres, industries, and regions. Due to Europe's cultural diversity, in order to exploit the dataset to the fullest we decided to split it into 3 subregions: eastern, western and northic due to culturo-ethnic fundamental differences.
   - Evaluate these disparities over the defined time periods.  

3. **Correlation with Financial Success**:  
   To investigate the link between representation gaps and box office revenue, we utilized:
   - **Radial Tree Plots:** Mapping success categories (Highly Successful, Successful, Normal) to genres and regions.
   - **Dual-Axis Charts:** Tracking representation gaps and revenue trends over decades.
   - **Sankey Diagrams:** Visualizing flows from representation gaps to genres and success outcomes.
   - **Linear Regression Analyses:** Measuring direct and controlled relationships between gaps and revenue.

4. **Thematic Vocabulary Analysis**:
   - Used NLTK to tokenize movie summaries for each region.
   - Generated vocabulary dictionaries from thematic seed words (e.g., "crime," leading to related words like "jail," "gang").
   - Compared tokenized words in the summaries with the vocabulary. If the overlap exceeded a predefined threshold, the movie was identified as addressing that theme.
From these theme-classified movies, further statistical analysis was conducted to derive insights. 

 

## **Timeline**

- Up Until Milestone P2: Completed all preprocessing and began regional analyses.
- Up until Milestone P3:
   - Week 10-12: Completed remaining regional analyses
   - Week 12 : Started website development
   - Week 13: Conducted the conclusive analysis
   - Week 12-14: Transform results into an engaging and interactive data story 

---

## **Contribution of team members**
- **Rim:** Real-world data preprocessing, Hollywood analysis, correlation studies and conclusive analysis
- **Alexandre Huou:** CMU datapreprocessing, lead website development and deployment
- **Zayneb:** East-Asia analysis, plotting the data, website development and deployement
- **Donia:** Bollywood analysis, summary-theme identification through key-word matching for deeper insights across all regions, data reliability analysis
- **Lily:** Europe analysis, plotting the data, data story writing, formatting on the site

---

## **A Word on the Data Story**

To make the data story engaging, we introduced an alien persona (of course called Ada) with a small backstory, which offers an external perspective on human cinematic trends. 

The site design incorporates a space-inspired color palette (e.g., alien greens, galaxy purples) to match the theme.
The storytelling approach aims to balance humor and professionalism to maintain reader interest.

---

## **Conclusion**

Our analysis highlights significant gaps in the way cinema portrays society. Across industries and regions, gender and age biases remain evident, often reinforcing societal norms. These disparities suggest that the film industry has been slow to evolve and maintains standards that do not reflect the diversity of the real world.

What stands out in our findings is the absence of relationship between representation gaps and box-office performance. This contradicts the argument that these portrayals are driven by financial motives and points instead to a reluctance to break away from long-standing traditions.

Cinema has always had the power to influence and reflect society. However, our study shows that it often falls short of its potential to represent the world accurately. 

---

# **A word on the site**

The site is interactive to follow Ada's journey. The reader can **explore each region** by clicking on the map. The reader will have an indication when it's time to go to the next region.
The best way to enjoy the site is to go through every region before reading the conclusive analysis but the reader can still read it after having read only one region analysis (though it is not recommended).

---

## **Quickstart**

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11 or ...
conda activate <env_name>

# install requirements
pip install -r pip_requirements.txt
```



### How to use the library
**Preprocessing Notebook:**
- Loads and cleans raw movie data from data/raw/CMU_movies, then saves the cleaned datasets to data/cleaned_datasets.
- Clusters the data by region (Oceania, Europe, East Asia, Hollywood, Bollywood) and saves it in data/clustered_clean.
- Loads and processes real-world demographic data from data/raw/real_world, saving relevant regional stats in data/final/region.

**Plotting Notebook:**
- Loads the prepared data from data/final/region to perform calculations and generate comparative plots, showing movie vs. real-world demographics.


## Project Structure

The directory structure of our project looks like this (note that the datasets are not included to to their sizes):
```
├── blog_P3                            <- Directory for website development
│
├── data                               <- Project data files
│   ├── raw                            <- Raw datasets
│   │   ├── CMU_movies                 <- Raw data for CMU movie datasets
│   │   └── real_world                 <- Raw real-world demographic data                   
│   ├── cleaned_datasets               <- Cleaned datasets after preprocessing
│   ├── clustered_clean                <- Region-based clustered datasets
│   └── final                          <- Final processed datasets for analysis
│       ├── bollywood                  <- Processed data for Bollywood region
│       ├── east_asia                  <- Processed data for East Asia region
│       ├── europe                     <- Processed data for Europe region
│       ├── hollywood                  <- Processed data for Hollywood region
│       └── oceania                    <- Processed data for Oceania region
│
├── src                                <- Source code
│   ├── preprocessing.py               <- Python script for the preprocessing
│   └── hollywood_functions.py         <- Python script for hollywood analysis
│   └── europe_functions.py            <- Python script for europe analysis
│   └── eastasia_functions.py          <- Python script for east-asia analysis
│   └── bollywood_functions.py         <- Python script for bollywood analysis
│   └── hollywood_crime_functions.py                <- Python script for hollywood crime analysis
│   └── europe_urban_depection_functions.py         <- Python script for europe urban analysis
│   └── bollywood_wealth_class_functions.py         <- Python script for bollywod wealth analysis
│   └── eastasia_overwork_culture_functions.py      <- Python script for east-asia overwork analysis
│   └── common_plots_functions.py      <- Python script for the basic plots that we later on made with flourish
│
│
├── .gitignore                         <- List of files ignored by git
├── pip_requirements.txt               <- Python dependencies file
├── results.ipynb                      <- Notebook with all analysis and their code
├── preprocessing_global_final.ipynb   <- Notebook for data cleaning and preprocessing
├── meme.png                           <- An easter egg for you
└── README.md
```
