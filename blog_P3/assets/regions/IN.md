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

Here’s the adjusted version with Ada narrating in the first person:

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

***Before making your way to the next part, click on the map to see the other regions' analysis***


---

# Integrated Analysis of Cinematic Representation Gaps and Box Office Revenue

---

# Introduction

As I drifted among Earth’s cultural constellations, I ventured into a grand endeavor: to understand how the movies Earthlings cherish align—or misalign—with the demographic patterns of your own reality. Anchored in three key metrics—**Ethnicity**, **Age**, and **Gender**—I sought to quantify representation gaps between real-world populations and the actors who grace Earthlings' screens. By examining how these discrepancies evolved through time and across regions, and by linking them to the gravitational pull of box office revenue, I hoped to uncover whether economic currents encourage such imbalances.

To explore this cinematic cosmos, I employed multiple observational instruments and analytical methods:

1. **Radial Tree Plot**: A visual galaxy mapping how movie success categories (Highly Successful, Successful, Normal) link to various genres and regions.  
2. **Combination Dual-Axis Charts**: Temporal journeys tracking representation gaps and box office revenue across decades, regions, and metrics. These help us see if changes in gaps mirror changes in revenue.  
3. **Sankey Plots**: Flows of movies from representation gap intervals to genres and ultimately to success categories, aggregated over the entire 1950–2012 period. These highlight structural associations between gap magnitude, genre choice, and final revenue outcomes.  
4. **Linear Regression Analyses**: Statistical attempts to measure a direct relationship between representation gaps and box office performance, both in simple forms (just gap vs. revenue) and more complex forms (controlling for metric type and temporal batches).

Armed with these tools, I can piece together a narrative: Does the industry’s portrayal of different ethnicities, genders, and ages shape—or is shaped by—its economic incentives?

---

# Methodology Adopted

**Representation Gaps**:  
For each metric (Ethnicity, Age, Gender), I computed representation gaps as absolute percentage differences between the movie populations and the corresponding real-world demographic proportions. The larger the gap, the further the industry strayed from mirroring Earth’s demographic reality. These gaps were calculated for each region (Hollywood, Bollywood, East Asia, Europe), across multiple 10-year time batches (1950–1959, 1960–1969, …, 2010–2012).

**Box Office Revenue**:  
To assess economic outcomes, I examined aggregated box office revenues (mean per batch or overall distributions) and categorized movies into percentile-based success categories:  
- **Highly Successful**: Top 10% by revenue  
- **Successful**: 40th to 90th percentile  
- **Normal**: Below the 40th percentile

By pairing these success categories with representation gaps, I hoped to see if achieving higher revenues demanded certain demographic imbalances.

**Same Metrics as Before**:  
I consistently used the same age, gender, and ethnicity data, ensuring coherence with previous analyses. Through all these steps—radial plots, line/area charts, Sankey diagrams, and regressions—the fundamental metrics and methods remained stable, allowing a comprehensive cross-check.

---

# The Four Analytical Works

## 1. Radial Tree Plot

<div class="flourish-embed flourish-hierarchy" data-src="visualisation/20820914"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20820914/thumbnail" width="100%" alt="hierarchy visualization" /></noscript></div>

This plot arranges genres around a circular axis, with success categories branching outward. Across all regions or within each one, we see how different genres populate these success tiers.

**Key Insights**:  
- **Global Patterns**: Action/Adventure and mass-appeal genres often cluster in Highly Successful tiers, indicating that big-budget spectacle transcends cultural borders. Documentaries and more niche genres hover in the Successful or Normal zones, mirroring their limited commercial appeal.  
- **Regional Nuances**: Hollywood’s penchant for Action/Adventure and Sci-Fi dominates the top revenue stratum, Bollywood’s Romance/Drama tradition finds consistent but not always top-tier success, East Asia’s Thriller/Suspense or locally favored genres anchor their success tiers, and Europe’s arthouse tilt shows fewer blockbuster hits.  
- **Link to Representation Gaps**: Although the radial tree plot does not directly show demographic gaps, it complements previous findings. Genres historically associated with skewed demographics still rank highly, suggesting that economic success often aligns with entrenched formulas, regardless of representational parity.

By showing the final distribution of genres into success categories, the radial chart reveals that commercial viability is often genre-driven and shaped by longstanding cultural and industrial norms—not necessarily by aligning closely with real-world demographics.

---

## 2. Combination Dual-Axis Charts: Hollywood

<!-- Dropdown pour chaque région ici-->

These charts overlay representation gaps and box office revenue over the decades, providing a temporal lens. For each region and metric, we see how gaps and revenue evolve together or diverge.

**Key Insights**:  
- **No Universal Trend**: Some periods show growing representation gaps alongside rising box office, others show shrinking gaps paired with stable revenue. This variation undermines any simple causal narrative.  
- **Cultural and Historical Context**: Hollywood’s shifts might reflect the blockbuster era, the influence of social movements, or global expansion. Bollywood’s stable star system could make representation gaps economically irrelevant. East Asia’s homogeneity might keep high gaps stable without penalty. Europe’s arthouse markets don’t necessarily reward more balanced demographics with big commercial wins.  
- **Societal Phenomena**: Periods of civil rights activism or global cultural exchange might nudge representation toward slightly narrower gaps without harming box office returns. Nonetheless, the data shows no strong pattern of “more representative = more revenue” or “less representative = more revenue.” Instead, genre cycles, star vehicles, and distribution networks overshadow demographic fine-tuning.

By capturing changes over decades, these combination dual-axis charts illustrate that economic success is molded by historical forces and market evolutions rather than a direct or stable representation-gap-to-revenue pipeline.

---

## 3. Representation Gaps and Box Office Revenue Impact

<!-- Dropdown pour chaque région ici-->

<div style="display: flex; justify-content: space-around; align-items: center; margin: 10px 0;">

  <!-- Plot 1 -->
  <div style="flex: 1; margin: 0 6px; text-align: center;">
    <div class="flourish-embed flourish-sankey" data-src="visualisation/20821631"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20821631/thumbnail" width="100%" alt="sankey visualization" /></noscript></div>
  </div>

  <!-- Plot 2 -->
  <div style="flex: 1; margin: 0 6px; text-align: center;">
    <div class="flourish-embed flourish-sankey" data-src="visualisation/20821662"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20821662/thumbnail" width="100%" alt="sankey visualization" /></noscript></div>
  </div>

  <!-- Plot 3 -->
  <div style="flex: 1; margin: 0 6px; text-align: center;">
    <div class="flourish-embed flourish-sankey" data-src="visualisation/20821797"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20821797/thumbnail" width="100%" alt="sankey visualization" /></noscript></div>
  </div>


</div>




The Sankey diagrams show the different flows of movies from representation gap intervals to genres and then to success categories. This tri-level mapping helps identify structural patterns.

**Key Insights**:  
- **Large Gap Intervals Still Yield Success**: If flows from high-gap categories ([50,75] or even [75,100]) lead into popular genres and ultimately into Highly Successful categories, it implies that entrenched demographic imbalances did not prevent lucrative outcomes.  
- **Genre as an Economic Mediator**: Some genres consistently channel movies into Successful or even Highly Successful tiers, regardless of gap size. This supports the idea that genre preferences and star power might be more influential than demographic realism.  
- **Comparing Metrics and Regions**: In Hollywood, large-gap intervals feeding into Action/Adventure and then into Highly Successful categories confirm that commercial formulas, not representational accuracy, often drive profit. Bollywood’s stable success of Romance/Drama under large gaps indicates similarly entrenched formulas. East Asia and Europe show analogous patterns, each with their local twists.

The Sankey plots, by exposing stable “flows” from gap categories to success categories, reinforce the notion that representation gap levels are not strong determinants of economic fate. Instead, the industry’s gravitational fields—rooted in genre traditions and audience tastes—predominantly shape financial success.

---

## 4. Linear Regression Analyses



After visually exploring patterns, I turned to linear and multiple regressions to seek a statistical relationship between representation gap and box office.

<!-- Dropdown pour chaque région ici-->

<iframe src="/assets/plots/box-office/regression_plot_Hollywood.html" width="100%" height="400px" style="border:none;"></iframe>

**Key Insights**:  
- **Simple Regression Weakness**: Only Hollywood’s simple regression suggested a modest negative relationship (higher gap = slightly lower revenue), but even that was weak.  
- **Multiple Regression Overfitting**: Controlling for Metric and 10-year Batch labels explained all variation, leaving Representation Gap insignificant. This implies time and categorical differences, not demographic alignment, dominate the statistical landscape.  
- **Across Regions**: Bollywood, East Asia, and Europe showed no meaningful linear association between gap and revenue. The complex interplay of cultural history, market size, and genre preference overwhelms any direct linear effect of representation gaps.

These regressions confirm that once we factor in historical context (time periods) and differing metrics (ethnicity, age, gender), representation gap ceases to matter statistically. This supports the broader narrative: no simple numeric gap measure can predict box office returns reliably.




---

# Bringing It All Together

Across four distinct works, one message emerges: **economic success in cinema does not strongly hinge on how closely movie demographics match real-world populations.**

- **Radial Tree Plot**: Shows that globally favored genres secure top-tier revenue regardless of representational fidelity, hinting that economic incentives didn’t enforce representational balance.  
- **Combination Dual-Axis Charts**: Demonstrate that representation gaps fluctuate with historical forces, yet these fluctuations do not consistently correlate with higher or lower box office revenues. The industry’s formulas and cultural shifts matter more.  
- **Sankey Plots**: Aggregated flows reveal that even large demographic imbalances often feed into highly successful tiers via certain lucrative genres, reinforcing the idea that entrenched production norms hold sway over economic outcomes.  
- **Linear Regression Analysis**: Statistically confirms that once historical eras and metric categories are considered, representation gap loses explanatory power. No straightforward causal or linear link emerges between gap and revenue.

**Contextualizing with Societal and Historical Research**:  
Earth's real-world scholarship, from the Annenberg Inclusion Initiative’s studies on representation to historical accounts of Hollywood’s studio system, corroborate these patterns. Social movements for diversity have nudged changes, but the box office bottom line seems driven more by star systems, blockbuster formulas, and marketing prowess than by demographic accuracy. Bollywood’s reliance on established stars and romance genres, East Asia’s local genre preferences, and Europe’s arthouse identity all reflect entrenched market conditions rather than demographic rectifications.

**Conclusion**:  
My cosmic exploration suggests that, while moral and cultural arguments for better representation are robust and well-documented, purely economic motives don’t straightforwardly reward or punish representational fidelity. Cinematic ecosystems seem able to thrive financially under various demographic distributions, relying instead on traditional genres, star legacies, and shifting audience tastes. To alter these constellations of representation, external sociopolitical forces, audience advocacy, and institutional reforms may be required—beyond the gravitational pull of the box office itself.

In sum, the works we assembled act like telescopes and spectrometers. They reveal a complex cinematic universe where demographic reality often bends under the weight of tradition, cultural myths, and economic expediency. True demographic alignment might not guarantee a bigger cosmic payoff, but the pursuit of a cinema that mirrors its audience’s diversity might still resonate with Earth’s evolving sense of justice and authenticity.
