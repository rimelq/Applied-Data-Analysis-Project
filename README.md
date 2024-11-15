
# **The Reel World vs. The Real World: Is Cinema Holding a True Mirror to Society?**

## **Abstract**

Cinema has always served as a lens through which society is reflected—or distorted. This project investigates whether the cinematic world aligns with real-world demographics in terms of gender, ethnicity, and age, or whether it reinforces outdated stereotypes. By comparing on-screen representation to societal expectations across genres and regions, we aim to highlight discrepancies and explore their potential implications. Our analysis will compare demographic representation not only by region but also across major film industries such as Hollywood, Bollywood, and others. Beyond identifying these disparities, we will examine trends over time and consider data-driven proposals to address them. 

---

## **Research Questions**
1. How accurately does cinema reflect real-world gender, ethnicity, and age demographics?
2. What trends can be identified in cinematic representation over time?
4. How do these portrayals vary across regions, industries, and genres?  
5. Are the largest demographic discrepancies linked to box office revenue?  

---

## **Data Processing**

### **Why Start from 1950?**  
We chose 1950 as our starting point, the era of classics like *Pather Panchali* and *Sunset Boulevard* because this period marks the availability of consistent demographic data and represents the beginning of the "contemporary" world. It also coincides with significant transformations in global cinema, including the rise of major film industries and the globalization of filmmaking.

---

### **Ethnicity Representation Across Film Industries**
The Hollywood film industry is often considered representative of North America, while Bollywood plays a similar role for South Asia. Our analysis extends to other regions such as East Asia, Europe and Oceania to provide a comprehensive understanding of how cinematic industries reflect (or diverge from) the demographics of their associated populations.

1. **Data Sources**:  
   - Ethnicity data for North America was sourced from the [EPR Core dataset](https://icr.ethz.ch/data/epr/core/), providing population breakdowns over time.  
   - Jewish-American population data was added from [Pew Research 2013](https://www.pewresearch.org/religion/2013/10/01/chapter-1-population-estimates/) and [Pew Research 2021](https://www.pewresearch.org/religion/2021/05/11/the-size-of-the-u-s-jewish-population/) due to their historical significance in Hollywood.
     
2. **Adjustments for Analysis**:  
   - Limited ethnic categorization in some regions (e.g., Canada, Oceania) led us to focus on the largest contributing country within each industry when necessary.  
   - Missing data points were filled with zeroes, assuming negligible population proportions.  
   - In this analysis, we focused on how Indian Bollywood movies represent Indian ethnicities compared to the real world.        Bollywood actors with non-Indian ethnicities (less than 1% of the data) were excluded to maintain this focus.

3. **Time Fragmentation**:  
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
   - With over 70% missing values in *actor_ethnicity* overall, we explored web scraping to supplement the data. We scraped from both **Wikidata** and **Ethnicelebs**, though Ethnicelebs provided limited information. Wikidata, however, yielded promising results. While we haven’t integrated these values yet, we may consider using the Wikidata results in P3 to improve data completeness. (The file containing the tests for the web scraping process can be found in test/scrap.ipynb.)

2. **Comparative Analysis**:  
   - Compare on-screen demographics to real-world populations, highlighting differences across genres, industries, and regions. Due to Europe's cultural diversity, in order to exploit the dataset to the fullest we decided to split it into 3 subregions: eastern, western and northic due to culturo-ethnic fundamental differences.
   - Evaluate these disparities over the defined time periods.  

3. **Correlation with Financial Success**:  
   - Investigate whether industries with larger representation gaps see higher or lower box office revenue.  
   - Use visualizations such as bubble plots with attributes like:  
     - **X-axis**: Time periods.  
     - **Y-axis**: Relative demographic discrepancies.  
     - **Bubble size**: Box office revenue.  
     - **Bubble color**: Genres or demographic attributes.  

4. **Trend Analysis**:  
   - Identify shifts in representation trends over the decades for each industry.  

5. **Insights and Recommendations**:  
   - Propose strategies for better alignment between on-screen demographics and real-world populations.  

---

## **Proposed Timeline for P3**

### **For P3 (Submission deadline: December 14, 2024):**

- **Week 1 (November 15–21)**:  
  - Conduct detailed analyses of demographic differences across genres, industries, regions, and time periods.  
  - Correlate demographic gaps with financial success metrics.  

- **Week 2 (November 22–28)**:  
  - Develop advanced visualizations, such as bubble plots and comparative charts.  
  - Highlight trends and outliers for each film industry.  

- **Week 3 (November 29–December 7)**:  
  - Synthesize findings and generate actionable insights.  
  - Begin drafting the data story, integrating visual elements to support the narrative.  

- **Week 4 (December 8–14)**:  
  - Finalize all analyses and visualizations.  
  - Publish the data story on a web platform (e.g., GitHub Pages).  
  - Submit the final GitHub repository with all deliverables.  

---

## **Organization within the Team**

- **Data Preprocessing and Pipeline Development**: [Alexandre Huou]  
- **Demographic Analysis and Correlation Studies**: [Rim El Qabli]  
- **Visualization and Interactive Story Design:** [Donia Gasmi]   
- **Statistical Analysis and Insights Generation**: [Lily Gilibert]
- **Website Development and Storytelling Integration:** [Zeineb Mellouli] 

---

## **Questions for TAs**

1. Is it feasible to infer whether financial profitability drives disparities in representation?  
2. Are there specific statistical methods or visualizations you recommend for analyzing demographic discrepancies in relation to box office performance?  
3. Is attempting to develop a machine learning model to provide actionable steps for improving representation a reasonable goal, or should we focus on descriptive insights instead?  
4. What challenges might arise when comparing representation across smaller or underrepresented regional industries?  
*Your input will guide us in prioritizing descriptive versus predictive analysis and ensure robust statistical validity.*
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

The directory structure of our project looks like this:
```
├── data                          <- Project data files
│   ├── raw                       <- Raw datasets
│   │   ├── CMU_movies            <- Raw data for CMU movie datasets
│   │   └── real_world            <- Raw real-world demographic data                   
│   ├── cleaned_datasets          <- Cleaned datasets after preprocessing
│   ├── clustered_clean           <- Region-based clustered datasets
│   └── final                     <- Final processed datasets for analysis
│       ├── bollywood             <- Processed data for Bollywood region
│       ├── east_asia             <- Processed data for East Asia region
│       ├── europe                <- Processed data for Europe region
│       ├── hollywood             <- Processed data for Hollywood region
│       └── oceania               <- Processed data for Oceania region
│
├── src                           <- Source code
│   ├── preprocessing_global.ipynb     <- Notebook for data cleaning and preprocessing
│   └── plot.ipynb                <- Notebook for plotting and analysis
│   └── plot_functions.py         <- Python script with plotting functions
│
├── tests                         <- Test scripts and notebooks
│
├── .gitignore                    <- List of files ignored by git
├── pip_requirements.txt          <- Python dependencies file
└── README.md
```
