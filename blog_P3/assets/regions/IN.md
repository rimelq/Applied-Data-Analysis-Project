# **Bollywood Cluster**



<div style="display: flex; justify-content: space-between; align-items: flex-start;">
  <!-- Text Content -->
  <div style="flex: 3; padding: 10px;">

Along Earth’s southern latitudes, I encounter Bollywood, a shimmering star in the galaxy of South Asian entertainment. Festivals of color, ancient traditions, and a cinematic tapestry unlike any other converge here. In this analysis, let me uncover the patterns that shape Bollywood’s luminous screens.

  </div>

  <!-- Plot Content -->
  <div style="flex: 1; padding: 10px; display: flex; flex-direction: column; align-items: center;">
    <div style="width: 100%; max-width: 300px; aspect-ratio: 1 / 1; position: relative; overflow: hidden; border-radius: 8px;">
      <img 
        src="/assets/plots/reliability/reliabilty_IN.jpg" 
        style="width: 100%; height: 100%; object-fit: contain;">
    </div>
    <div style="font-size: 10px; color: #555; text-align: center; margin-top: 5px;">
      <em>*see at the end for more insight on this score</em>
    </div>
  </div>
</div>

---

## **Preliminary Visualizations of Ethnic Representation Over Time**

<!-- Dropdown ici-->



### **Observations**

<div style="display: flex; align-items: up; justify-content: space-between;">
  
  <!-- Text Container -->
  <div style="width: 50%; padding: 8px;">
    <p>

- **South Indian Ethnicities: The Stars of the Screen**  
South Indian ethnicities shine brightly with significantly higher representation compared to their real-world population. This likely reflects the strong influence of Tamil, Telugu, and Malayalam cinema, which left a stellar imprit on India's film industry.

- **Eastern Indian Ethnicities: Shadows in the Spotlight**  
In contrast, Eastern Indian ethnicities remain cloaked in softer light, underrepresented compared to their real-world presence. Bengali cinema, while culturally rich, manifests here like a quieter star, overshadowed by the South’s dazzling brilliance and Bollywood’s own radiance.



  </p>
</div>
<div style="width: 50%; padding: 8px;">
<p>

- **Western and Central Indian Ethnicities: Balanced in the Cosmos**  
Western and Central Indian ethnicities appear more balanced, their representation closer to real-world proportions. This could be the “Bollywood effect,” as Mumbai (Maharashtra)—the industry’s epicenter—naturally infuses its local flavors into the on-screen galaxy.

- **Religious and Caste Groups: The Unseen Constellations**  
Religious and caste identities flicker only faintly, barely detected in this dataset’s cosmic lens. Movies may skirt these topics, perhaps to maintain broad appeal or to avoid fracturing their audience’s orbit.

</p>
  </div>

</div> 

Now, we can observe how these ethnic representations influence the cosmic currency of box office returns.

<div style="display: flex; align-items: up; justify-content: space-between;">
  
  <!-- Text Container -->
  <div style="width: 30%; padding: 8px;">
    <p>

 The **Average Box Office Revenue by Majority Ethnicity** (1950–2012) guides us through a field of near-equilibrium, with revenues hovering around $18M for most groups. Yet a subtle anomaly appears: films featuring Eastern Indian ethnicities rise slightly above the cosmic baseline. Is it a quirk of market forces, audience preferences, or hidden gravitational pulls? The universe keeps its secrets close.



  </p>
</div>

  <!-- Plot Container -->
  <div style="width: 70%; padding: 8px;">
    <iframe src="/assets/plots/IN/average_Box_Office_revenue_by_ethnicity.html" width="100%" height="400px" style="border:none;"></iframe>

  </div>

  </div>

</div> 







---

# **Age Analysis of the Indian Movie Industry**

## **Preliminary Plots: Actor vs. Real-World Age Distributions**

<!--Dropdown ici-->


**Dominance of Youth Representation:**

Bollywood’s universe tilts heavily toward youth—actors in their early 20s illuminate the screens, while elders, though wise and storied, remain in dim twilight. Cultural ideals of youth and beauty shape this gravitational pattern, guiding casting decisions and narrative choices, and leaving more mature voices and faces at the cosmic periphery.

---

## **Preliminary Visualizations of Gender Representation**

<div class="flourish-embed flourish-chart" data-src="visualisation/20880839"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20880839/thumbnail" width="100%" alt="chart visualization" /></noscript></div>


----

### **Male Dominance Across Genres:**

Scan Bollywood’s genre map and you’ll find male actors reigning supreme across most categories. In **Action/Adventure** and **Thriller/Suspense**, for instance, around 69% of the starring roles gravitate toward men. These patterns echo longstanding Earthly norms and traditional storytelling frameworks. Yet, a faint ripple of change emerges in **Fantasy** and **Sci-Fi**, where female representation nudges upward, perhaps hinting at a future where balanced storytelling can thrive.

Female-dominated movies do exist, but remain relatively rare, reflecting an imbalance that still defines much of this cinematic cosmos.

---


<div style="display: flex; align-items: up; justify-content: space-between;">
  <!-- Text Container -->
  <div style="width: 50%;; padding: 10px;">

<div style="overflow: hidden; transform: scale(0.75); transform-origin: top left; width: 600px; height: 300px;">
    <iframe src="/assets/plots/IN/gender_dominance_plot.html" width="600px" height="100%" style="border:none;"></iframe>
</div>

  </div>

  <!-- Plot Container -->
  <div style="width: 50%;; padding: 10px;">
<div style="width: 100%; height padding: 10px;">

<div style="overflow: hidden; transform: scale(0.75); transform-origin: top left; width: 600px; height: 300px;">
<iframe src="/assets/plots/IN/average_revenue_by_gender.html" width="600px" height="100%" style="border:none;"></iframe>  
</div>
</div>

  </div>

  </div>



 Box office data shows male-led films orbiting slightly higher revenue zones, reinforcing existing hierarchies. Yet, as we chart temporal shifts, we see the number of female actors steadily rising from the dawn of the 1900s through the early 2010s. Expanding industry and social change offered more opportunities for women, inching toward a more equitable cosmos.


<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/20792821"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20792821/thumbnail" width="100%" alt="bar-chart-race visualization" /></noscript></div>

**Overall Growth:**

From the earliest echoes of cinematic history through the busy 2010s, female representation rose. The industry’s expansion and shifting cultural tides allowed more women to step forward, claiming space in this stellar narrative.

**Sudden Drop Post-2010:**

Yet, a curious drop after 2010 appears, likely a data illusion caused by incomplete reporting of recent films. As metadata catches up to reality, this temporary void may fill with new narratives and evolving trends. The future remains open, and as Earth’s cultural constants shift, so might the orbits of star power and representation.

---

## **Bollywood wealth and class distribution analysis**

**Income Classification by Movie Themes**

To better understand Bollywood’s storytelling, I classified movies into three income themes based on their narratives [1](https://cdn.statcdn.com/Infographic/images/normal/31991.jpeg), [2](https://wid.world/www-site/uploads/2024/03/WorldInequalityLab_WP2024_09_Income-and-Wealth-Inequality-in-India-1922-2023_Final.pdf):

- **Top 10%:** Films portraying wealth, luxury, and elite lifestyles.  

- **Middle 40%:** Stories about working professionals and middle-class aspirations.  

- **Bottom 50%:** Narratives focusing on poverty, rural struggles, and underprivileged communities.  

Using movie summaries, I categorized the films into these themes and compared their prevalence over time with real-world income distribution data.

<iframe src="/assets/plots/IN/wealth_class_analysis_bollywood.html" width="100%" height="500px" style="border:none;"></iframe>

**My discoveries:**

- **Bottom 50% Dominance:**  
  Despite holding only about 15% of the income share in reality, stories about the bottom 50% dominate Bollywood, especially in recent years.  
- **Top 10% Overrepresentation:**  
  While their income share dramatically increases (36.7% to 57.7%), the ultra-wealthy are depicted less often than the bottom 50%.  
- **Middle 40% Neglected:**  
  The middle class sees the sharpest decline in real-world income share (42.8% to 27.3%) and remains underrepresented in Bollywood narratives.

**Conclusion:**  
Bollywood’s storytelling gravitates toward the extremes, spotlighting either the struggles of the bottom 50% or the opulence of the top 10%, while largely ignoring the middle class. This trend likely reflects a combination of audience preferences and the industry’s focus on aspirational or socially impactful themes.

## **References**

<span style="font-size: 11px;">

<a id="1">[1]</a> World Inequality Lab (2023). How the Income of India's Richest 10% Surged [https://cdn.statcdn.com/Infographic/images/normal/31991.jpeg]

<a id="2">[2]</a> Bharti, N. (2024). Income and Wealth Inequality in India, 1922-2023: The Rise of the Billionaire Raj [https://wid.world/www-site/uploads/2024/03/WorldInequalityLab_WP2024_09_Income-and-Wealth-Inequality-in-India-1922-2023_Final.pdf]



</span>

---

<div style="font-size: 1.5em; margin-top: 30px;">

**Before proceeding to the next section:**

- **Explore the map** to view the analyses for the 3 other Regions! 
&nbsp;&nbsp;&nbsp;&nbsp; <!-- Adds horizontal space -->
- Click **"Move Up"** to return to the top of the page.
</div>

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


---

<h2 id="integrated-analysis"></h2>

# **All-Regions Analysis of Representation Gaps and Box Office Revenue**

---
<br>
<br>


# Introduction

As I explored Earth's diverse cultures, I took on a mission to understand how movies reflect—or differ from—real-world demographics. Focusing on three key factors—**Ethnicity**, **Age**, and **Gender**—I analyzed gaps between the real-world population and the actors on screen. By studying how these differences changed over time and across regions, and by examining their connection to box office earnings, I aimed to uncover whether economic factors drive these imbalances.

To explore this cinematic landscape, I used several tools and methods:

1. **Radial Tree Plot**: A visual map showing how movie success levels (Highly Successful, Successful, Normal) connect to different genres and regions.  
2. **Combination Dual-Axis Charts**: Tracking representation gaps and box office revenue over time, across decades, regions, and metrics, to see if changes in representation align with changes in revenue.  
3. **Sankey Plots**: Visualizing the flow of movies from representation gap levels to genres and then to success categories, covering the entire 1950–2012 period, to uncover patterns between gap size, genre, and revenue.  
4. **Linear Regression Analyses**: Statistical models to explore whether representation gaps directly impact box office performance, both simply (gap vs. revenue) and with additional factors like metric type and time periods.

With these tools, I aim to answer: Does how the industry represents ethnicity, gender, and age influence—or get influenced by—its financial goals?

---

# Methodology Adopted

**Representation Gaps**:  
For each metric—**Ethnicity**, **Age**, and **Gender**—I calculated representation gaps as the absolute percentage difference between movie demographics and real-world proportions. Larger gaps indicate a greater deviation from Earth’s demographic reality. These gaps were measured for each region (Hollywood, Bollywood, East Asia, Europe) across 10-year periods (1950–1959, 1960–1969, …, 2010–2012).

**Box Office Revenue**:  
To evaluate economic outcomes, I analyzed box office revenues (average per decade or overall distributions) and grouped movies into success categories based on percentiles:  
- **Highly Successful**: Top 10% of revenue  
- **Successful**: 40th to 90th percentile  
- **Normal**: Below the 40th percentile  

By linking these success categories to representation gaps, I aimed to see if certain demographic imbalances were associated with higher revenues.

**Same Metrics as Before**:  
I consistently used the same age, gender, and ethnicity data throughout the analysis. Whether using radial plots, line/area charts, Sankey diagrams, or regression models, the metrics and methods remained stable, to ensure a reliable cross-check.

---

# The Four Analytical Works

## 1. Radial Tree Plot

<div class="flourish-embed flourish-hierarchy" data-src="visualisation/20820914"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20820914/thumbnail" width="100%" alt="hierarchy visualization" /></noscript></div>

This plot arranges genres around a circular axis, with success categories branching outward. It shows how different genres fall into these success tiers, either globally or within specific regions.

**Key Insights**:  
- **Global Patterns**: Action/Adventure and other mass-appeal genres often dominate the Highly Successful tier, highlighting their universal appeal. In contrast, documentaries and niche genres tend to cluster in the Successful or Normal zones, reflecting their limited commercial draw.  
- **Regional Nuances**: Hollywood excels in Action/Adventure and Sci-Fi at the top revenue levels, while Bollywood’s Romance/Drama is consistently successful but not always a blockbuster. East Asia finds success with Thriller/Suspense and locally popular genres, while Europe’s focus on arthouse films results in fewer major hits.  
- **Link to Representation Gaps**: While the radial tree plot doesn’t directly show demographic gaps, it complements earlier findings. Genres often tied to skewed demographics still perform well, suggesting economic success frequently relies on established industry formulas rather than demographic representation.

By mapping the distribution of genres into success categories, the chart highlights how commercial success is heavily influenced by genre preferences shaped by cultural and industry norms, rather than strict alignment with real-world demographics.


---

*For the Combination Dual-Axis Charts and Sankey diagrams, while results from other regions were analyzed as part of our cosmic experiment, only Hollywood's results are displayed to prioritize rendering efficiency, given its status as Earth's cinematic powerhouse.*

## 2. Combination Dual-Axis Charts: Hollywood

<!-- Dropdown pour chaque région ici-->

These charts overlay representation gaps and box office revenue over the decades, providing a temporal lens. For each region and metric, we see how gaps and revenue evolve together or diverge.

**Key Insights**:  
- **No Universal Trend**: Some periods show larger representation gaps with rising box office revenues, while others show smaller gaps with steady earnings. This inconsistency challenges any straightforward cause-and-effect narrative.  
- **Cultural and Historical Context**: Hollywood’s shifts may reflect the blockbuster era, social movements, or global market influence. Bollywood’s stable star system might make representation gaps less relevant to revenue. East Asia’s homogeneity may sustain large gaps without economic impact, while Europe’s arthouse focus doesn’t necessarily reward balanced representation with high earnings.  
- **Societal Phenomena**: Civil rights movements or global cultural exchanges may have slightly narrowed gaps without reducing box office returns. However, the data doesn’t support a clear link between “better representation = more revenue” or “worse representation = more revenue.” Instead, factors like genre trends, star power, and distribution strategies play a larger role.

By capturing changes over decades, these combination dual-axis charts illustrate that economic success is molded by historical forces and market evolutions rather than a direct or stable representation-gap-to-revenue pipeline.

---

## 3. Representation Gaps and Box Office Revenue Impact: Hollywood

<!-- Dropdown pour chaque région ici-->


The Sankey diagrams show the different flows of movies from representation gap intervals to genres and then to success categories. This tri-level mapping helps identify structural patterns.

**Key Insights**:  
- **Large Gap Intervals Still Yield Success**: Movies from large-gap categories (e.g., [50–75] or even [75–100]) often flow into popular genres and end up in Highly Successful tiers, showing that significant demographic imbalances don’t necessarily hinder profitability.  
- **Genre as an Economic Mediator**: Certain genres consistently push movies into Successful or Highly Successful tiers, regardless of demographic gaps. This suggests that genre preferences and star appeal often outweigh the importance of demographic representation.  
- **Comparing Metrics and Regions**: In Hollywood, large-gap movies often succeed in Action/Adventure genres, emphasizing that commercial success relies on tried-and-true formulas rather than representational accuracy. Bollywood’s steady success with Romance/Drama under high gaps reflects similar patterns. East Asia and Europe also exhibit these trends, with regional variations.

The Sankey plots, by exposing stable “flows” from gap categories to success categories, reinforce the notion that representation gap levels are not strong determinants of economic fate. Instead, the industry’s gravitational fields—rooted in genre traditions and audience tastes—predominantly shape financial success.

---

## 4. Linear Regression Analyses



After visually exploring patterns, I turned to linear and multiple regressions to seek a statistical relationship between representation gap and box office.

<!-- Dropdown pour chaque région ici-->


**Key Insights**:  
- **Limitations of Simple Regression**: Only Hollywood showed a slight negative relationship (higher gap = slightly lower revenue), but even this connection was weak.  
- **Overfitting in Multiple Regression**: When accounting for Metric and 10-year Batch labels, Representation Gap became statistically insignificant. This indicates that time periods and categorical differences, not demographic alignment, primarily explain the variation.  
- **Regional Analysis**: In Bollywood, East Asia, and Europe, no clear linear relationship between gaps and revenue was found. The complex mix of cultural history, market size, and genre preferences overshadows any straightforward effect of representation gaps.

These regressions confirm that, after accounting for historical context and metric differences, representation gaps have no significant statistical impact. This reinforces the idea that no simple gap measure can reliably predict box office success.



---

# Bringing It All Together

Across four distinct works, one message emerges: **economic success in cinema does not strongly hinge on how closely movie demographics match real-world populations.**

- **Radial Tree Plot**: Highlights that globally popular genres consistently achieve top-tier revenue, regardless of representational accuracy, suggesting that economic incentives don’t drive balanced representation.  
- **Combination Dual-Axis Charts**: Show that representation gaps change with historical trends, but these shifts don’t reliably link to higher or lower box office revenues. Industry formulas and cultural movements play a bigger role.  
- **Sankey Plots**: Reveal that even movies with significant demographic imbalances often succeed in top revenue tiers through profitable genres, emphasizing the dominance of established production norms over representation concerns.  
- **Linear Regression Analysis**: Confirms that when historical periods and metric types are accounted for, representation gaps have little impact. There’s no clear linear or causal relationship between gaps and revenue.

**Contextualizing with Societal and Historical Research**:  
Studies like those from the Annenberg Inclusion Initiative and historical analyses of Hollywood’s studio system confirm these trends. While social movements for diversity have influenced change, box office success still relies more on star power, blockbuster formulas, and marketing strategies than on accurate demographic representation. Bollywood primarily centers on big-name stars and romance genres as its key to success. East Asia tends to favor genres that appeal to local audiences, while Europe leans heavily toward arthouse films. These trends highlight how each region’s movie industry is shaped by long-standing market preferences and economic strategies, rather than by actively trying to improve demographic representation.


**Conclusion**:  
My cosmic exploration suggests that, while moral and cultural arguments for better representation are robust and well-documented, purely economic motives don’t straightforwardly reward or punish representational fidelity. Cinematic ecosystems seem able to thrive financially under various demographic distributions, relying instead on traditional genres, star legacies, and shifting audience tastes. To alter these constellations of representation, external sociopolitical forces, audience advocacy, and institutional reforms may be required—beyond the gravitational pull of the box office itself.

In sum, the works we assembled act like telescopes and spectrometers. They reveal a complex cinematic universe where demographic reality often bends under the weight of tradition, cultural myths, and economic expediency. True demographic alignment might not guarantee a bigger cosmic payoff, but the pursuit of a cinema that mirrors its audience’s diversity might still resonate with Earth’s evolving sense of justice and authenticity.



## References

<span style="font-size: 11px;">
<a id="1">[1]</a> Smith, S. L., Choueiti, M., Pieper, K., Case, A., & Clark, H. (2024). Inequality in 1,200 Popular Films: Examining Portrayals of Gender, Race/Ethnicity, LGBTQ+ & Disability from 2007 to 2018. Annenberg Inclusion Initiative. Retrieved from https://annenberg.usc.edu/research/aii

<a id="2">[2]</a> Gomery, D. (2005). The Hollywood Studio System: A History. British Film Institute Publishing. 

</span>


-----

**More insights on Data Reliability Score:**

The **Reliability Score 𝑅** is calculated as:

#### **Formula**:

#### R\=0.4⋅D+0.4⋅(1−M)+0.2⋅T 

With:
**D** = Dataset Size Ratio.
**M** = Missing Data Ratio. 
**T** = Temporal Coverage ratio.


Ensuring that:
- Higher missing data decreases the score.
- A region with balanced dataset size and temporal coverage will achieve higher scores.