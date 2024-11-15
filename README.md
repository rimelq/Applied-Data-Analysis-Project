
# **The Reel World vs. The Real World: Is Cinema Holding a True Mirror to Society?**

## **Abstract**

Cinema has always served as a lens through which society is reflected—or distorted. This project investigates whether the cinematic world aligns with real-world demographics in terms of gender, ethnicity, and age, or whether it reinforces outdated stereotypes. By comparing on-screen representation to societal expectations across genres and regions, we aim to highlight discrepancies and explore their potential implications. Our analysis will compare demographic representation not only by region but also across major film industries such as Hollywood, Bollywood, and others. Beyond identifying these disparities, we will examine trends over time and consider data-driven proposals to address them.

---

## **Research Questions**

1. How accurately does cinema reflect real-world gender, ethnicity, and age demographics?  
2. How do these portrayals vary across regions, industries, and genres?  
3. Are the largest demographic discrepancies linked to box office revenue?  
4. What trends can be identified in cinematic representation over time?  

---

## **Data Processing**

### **Why Start from 1950?**  
We chose 1950 as our starting point because this period marks the availability of consistent demographic data and represents the beginning of the "contemporary" world. It also coincides with significant transformations in global cinema, including the rise of major film industries and the globalization of filmmaking.

---

### **Ethnicity Representation Across Film Industries**
The Hollywood film industry is often considered representative of North America, while Bollywood plays a similar role for South Asia. Our analysis extends to other regions such as Europe, Oceania, Africa, and the Middle East (TODO: are we doing middle east ?) to provide a comprehensive understanding of how cinematic industries reflect (or diverge from) the demographics of their associated populations.

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

2. **Comparative Analysis**:  
   - Compare on-screen demographics to real-world populations, highlighting differences across genres, industries, and regions.  
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
- **Visualization Development**: [Lily Gilibert]  
- **Statistical Analysis and Insights Generation**: [Zeineb Mellouli]  
- **Documentation and Data Story Writing**: [Donia Gasmi]  

---

## **Questions for TAs**

1. Is it feasible to infer whether financial profitability drives disparities in representation?  
2. Are there specific statistical methods or visualizations you recommend for analyzing demographic discrepancies in relation to box office performance?  
3. Is attempting to develop a machine learning model to provide actionable steps for improving representation a reasonable goal, or should we focus on descriptive insights instead?  
4. What challenges might arise when comparing representation across smaller or underrepresented regional industries?  

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
Tell us how the code is arranged, any explanations goes here.



## Project Structure

The directory structure of our project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

