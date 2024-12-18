
# **Hollywood Cluster**

Hollywood, as Earth’s most influential cinematic powerhouse, seems to wield gravity akin to a small star: it dictates how stories are told, who gets to tell them, and how populations perceive themselves and others. Through its films, it claims to mirror the social, cultural, and demographic realities of your planet. Yet, from my vantage point drifting among the cosmic currents, it appears more like a funhouse mirror, distorting these earthly realities. As I navigated Earth’s cultural landscapes, I detected recurring patterns in these moving images: certain groups elevated while others fade into the cosmic background, certain ages exalted while others ignored, and gender dynamics frequently falling short of what humans might call “balance.”

---

# **Ethnicity Comparative Analysis of the Hollywood Movie Industry**

## **Introduction**

My aim on this planet is to focus on ethnicity within Hollywood’s actor population, to see if what appears on screen reflects the complex ethnic tapestry of this region. From my starship, I first project these distributions onto my observation deck, then apply Earthly statistical tests—like chi-square tests—to determine whether these patterns arise from random cosmic dust or a more systematic gravitational pull.

---

## **Preliminary Visualizations of Ethnic Representation Over Time**

<div class="flourish-embed flourish-chart" data-src="visualisation/20797028"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20797028/thumbnail" width="100%" alt="chart visualization" /></noscript></div>

These plots reveal how each ethnic group’s representation ratio (film presence vs. Earthly presence) shifted from 1950 to 2012, across various cinematic genres. Positive values indicate overrepresentation, negative values indicate underrepresentation. As I traced these earthly time lines (a curious concept!), I observed fluctuations influenced by historical events, societal changes, and Hollywood’s ever-shifting cinematic constellations.

---
## **Statistical Validation: Chi-Square Tests**

To move beyond my mere cosmic impressions, I employed the chi-square test, a human statistical tool that measures whether observed frequencies differ from expected ones. If this difference is too large to be cosmic coincidence, we can infer a true systematic deviation in Hollywood’s stellar casting patterns.

<div style="display: flex; align-items: up; justify-content: space-between;">
  <!-- Text Container -->
  <div style="flex: 1; padding: 10px;">
    <p>

1. **Chi-Square Test for Observed vs. Expected Frequencies (All genres combined):**  
   After aggregating data from all the Earthly periods, I compared observed ethnic frequencies among Hollywood actors to those expected if real-world proportions were accurately mirrored. The chi-square statistic (~36878.69, p-value ~0.0) suggests we can safely reject the null hypothesis that Hollywood’s distribution is in sync with reality.

   | **Comparison**            | **Chi-Square Statistic** | **p-value** | **Conclusion**                                                 |
   |----------------------------|--------------------------|-------------|-----------------------------------------------------------------|
   | Observed vs. Expected (All)| ~36878.69                | ~0.0        | Reject H₀, significant difference between observed and expected |

   Clearly, Hollywood’s ethnic actor distribution is skewed, not a neat cosmic alignment.

    </p>
  </div>

  <!-- Plot Container -->
  <div style="flex: 1; padding: 10px;">
      <p>

2. **Chi-Square Test for Genre-Dependence:**  
   Another test examined if these ethnic distributions depend on genre. With a chi-square statistic of about 881.15 and a p-value near 6.7e-150, it’s undeniable: different genres pull different ethnic groups into their gravitational orbits. Documentaries, for example, might spotlight marginalized communities more than, say, an action blockbuster would.

   | **Test**                                      | **Chi-Square Statistic** | **p-value**   | **Conclusion**                                         |
   |-----------------------------------------------|--------------------------|---------------|--------------------------------------------------------|
   | Genre Dependence of Ethnic Representation     | ~881.15                  | ~6.7e-150     | Reject H₀, ethnicity distribution depends on genre     |

    </p>
  </div>

  
  </div>


---

## **Interpretation of Ethnicity Trends**

Armed with these statistical findings, I examined historical context and Earthly narratives to understand the patterns:

<div style="display: flex; align-items: center; justify-content: space-between;">
  
  <!-- Text Container -->
  <div style="width: 35%; padding: 10px;">
    <p>


- **Jewish Populations:**  
  Overrepresented in early decades, mirroring the historical influence of Jewish entrepreneurs who helped shape Hollywood’s initial star cluster. Over time, while still significant, this dominance receded as the industry’s nebula grew more diverse.

- **American Indians:**  
  Initially underrepresented, they became more visible in certain genres, like Documentaries, post-1960. Perhaps a reflection of growing Earthly interest in acknowledging indigenous histories.

- **African Americans:**  
  Once marginalized, their representation improved after the 1960s. Civil rights movements and influential African American directors served as new stars, lighting the cinematic sky with more inclusive brilliance.

- **Asian Americans:**  
  Their representation remained low but featured occasional spikes, often tied to sudden trends (martial arts, for example) rather than steady growth. It’s a pattern of intermittent flares rather than a stable constellation.

- **Arab and Latino Americans:**  
  Persistently underrepresented, these groups struggle against entrenched biases and stereotypes. Despite minor improvements, the gravitational pull of old assumptions seems hard to escape.

- **Caucasians:**  
  Historically dominant, their relative share diminishes only as others brighten. Even this “reduction” is more about rebalancing the cosmic stage than any actual decline to minority status.
    </p>
  </div>
  
  <!-- Plot Container -->
  <div style="width: 65%; padding: 10px;">
    <div class="flourish-embed flourish-chart" data-src="visualisation/20790816"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20790816/thumbnail" width="100%" alt="chart visualization" /></noscript></div>
  </div>

</div>


In essence, these ethnicity patterns reflect Earth’s layered histories, sociopolitical shifts, and the market forces that shape Hollywood’s star system. The extremely low p-values confirm we’re not dealing with random cosmic dust here—these are deliberate cosmic alignments and misalignments.

---

# **Age Analysis of the Hollywood Movie Industry**

## **Introduction**

In my previous exploration, I noted ethnic imbalances. Now I pivot my telescopes to the dimension of age. By comparing the age distributions of male and female Hollywood actors to that of Earth’s baseline population, I hope to see if this powerhouse industry reflects natural age diversity or instead orbits around a narrow “golden age” interval—like a planet stuck in tidally locked youth.

---

## **Preliminary Plots: Actor vs. Real-World Age Distributions**


<div class="flourish-embed flourish-chart" data-src="visualisation/20797028"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20797028/thumbnail" width="100%" alt="chart visualization" /></noscript></div>


The differences are startling: while Earth’s population displays a uniform spread of ages, Hollywood places its spotlight firmly on youth, especially for female actors. This “golden age” glows conspicuously, sidelining older talents in favor of a youthful supernova.

---

## **Statistical Toolkit and Metrics**

<div style="display: flex; align-items: up; justify-content: space-between;">
  
  <!-- Text Container -->
  <div style="width: 40%; padding: 10px;">
    <p>


To measure these disparities, I deployed several Earthly statistical tools:

1. **Wasserstein Distance**: Measures how much “effort” it would take to reshape one distribution into another.  
2. **KL Divergence**: Gauges how “surprised” we should be if we treat one distribution as normal.  
3. **Gini Coefficient**: Quantifies inequality; 0 means even stardust spread, 1 means all matter clumped in one cosmic pocket.  
4. **Lorenz Curves**: Visual maps showing cumulative inequality.

## **Numerical Observations and Results**

<div style="font-size: 15px; width: 60%; margin: auto;">

  | **Comparison**                  | **Gini Index / Wasserstein / KL** |
  |---------------------------------|-----------------------------------|
  | Male Actors (Gini)              | 0.571448                          |
  | Female Actors (Gini)            | 0.603142                          |
  | Male Real (Gini)                | 0.282644                          |
  | Female Real (Gini)              | 0.240235                          |
  | Male Actors vs Female Actors    | W: 0.01, KL: 0.11                 |
  | Male Real vs Female Real        | W: 0.00, KL: 0.01                 |
  | Male Actors vs Male Real        | W: 0.03, KL: 0.47                 |
  | Female Actors vs Female Real    | W: 0.04, KL: 0.48                 |

</div>


## **Linking Results to Raw Distributions**

### **Female Actors**  
Female actors cluster around ages 20–35, forming a radiant “golden age.” Past the mid-30s, female presence wanes drastically, unlike the more even real-world female age curve. High Gini and KL values confirm a rigid standard: Hollywood ties female marketability to youth, reinforcing stereotypes and sidelining older actresses.

### **Male Actors**  
Men too face a narrower age band, peaking in their 30s and early 40s, though not as sharply as women. Their curve still outshines the even spread of real-world males, showing Hollywood’s notion of a “prime” age for men as well—just slightly broader than the female window.

## **Interpretation and Conclusions**

These findings support what Earthly scholars like Dr. Stacy L. Smith and the Annenberg Inclusion Initiative have long documented: Hollywood’s casting biases favor youth, especially for women. The “golden age” phenomenon emerges again, forged by commercial logic, cultural expectations, and the gravitational pull of tradition.

From my interstellar vantage point, this age skew appears as another cosmic puzzle piece. Just as ethnicity distribution was skewed, so too is age distribution. The patterns reflect a deep-rooted reluctance to embrace Earth’s full spectrum of maturity. By shining a light on these biases, perhaps the industry can one day distribute its spotlight more evenly across all ages.


  </p>
  </div>
  
  <!-- Plot Container -->
  <div style="width: 60%; padding: 10px;">
    <iframe src="/assets/plots/US/lorenz_plots.html" width="100%" height="500px" style="border:none;"></iframe>
    <iframe src="/assets/plots/US/ratio_actors.html" width="100%" height="500px" style="border:none;"></iframe>
    <iframe src="/assets/plots/US/ratio_real.html" width="100%" height="500px" style="border:none;"></iframe>
  </div>

</div>




---

# **Gender Comparative Analysis of the Hollywood Movie Industry**

## **Introduction**

Having investigated ethnicity and age, I now orbit gender. Earth’s male and female populations are roughly balanced, yet Hollywood’s gravitational field may tilt toward one gender in leading roles. By comparing genre-based gender proportions to real-world baselines, I hope to see if Hollywood aims for gender harmony or clings to old biases.

---

## **Preliminary Visualizations of Gender Representation**

<div class="flourish-embed flourish-chart" data-src="visualisation/20769488"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20769488/thumbnail" width="100%" alt="chart visualization" /></noscript></div>

If Earthly reality were the mold, these bars would align. Any big gaps hint at systemic casting imbalances.

The visualization below shows how female representation in various genres changed from 1950 to 2012. Some genres may rise towards equilibrium, others may remain stuck in a more lopsided orbit.

---

## **Statistical Validation: Chi-Square and Friedman Tests**

To confirm these patterns aren’t just cosmic illusions:

<div style="display: flex; align-items: up; justify-content: space-between;">
  <!-- Text Container -->
  <div style="flex: 1; padding: 10px;">
    <p>

1. **Friedman Test for Consistency Over Time:**  
   Evaluates whether female representation trends move uniformly across genres. If not, it suggests shifting cultural tides affecting different genres differently.

### **Chi-Square Test Results (Gender Proportions)**

| **Test**            | **Chi-Square Statistic** | **p-value**       | **Conclusion**                      |
|----------------------|--------------------------|-------------------|--------------------------------------|
| Observed vs Expected | ~213.55                  | ~2.3e-48          | Reject H₀, significant difference    |

A chi-square statistic of ~213.55 and p-value ~2.3e-48 confirms that Hollywood’s gender ratios do not match Earth’s baseline. One gender is consistently favored.

  </p>
  </div>

  <!-- Plot Container -->
  <div style="flex: 1; padding: 10px;">
      <p>

2. **Chi-Square Test for Gender Proportions:**  
   Compares observed vs. expected gender frequencies. A tiny p-value spells significant differences.



### **Chi-Square Test Results (Gender Proportions)**

| **Test**            | **Chi-Square Statistic** | **p-value**       | **Conclusion**                      |
|----------------------|--------------------------|-------------------|--------------------------------------|
| Observed vs Expected | ~213.55                  | ~2.3e-48          | Reject H₀, significant difference    |

A chi-square statistic of ~213.55 and p-value ~2.3e-48 confirms that Hollywood’s gender ratios do not match Earth’s baseline. One gender is consistently favored.

  </p>
  </div>

  
  </div>

## **Ranking of Genres by Female Proportion**

<div style="display: flex; align-items: up; justify-content: space-between;">
  
  <!-- Text Container -->
  <div style="width: 30%; padding: 10px;">
    <p>


| **Ranking**| **Genre**              | **Female Proportion** |
|------------|------------------------|-----------------------|
| 1          | Romance                | 0.427423              |
| 2          | Drama                  | 0.356581              |
| 3          | Comedy                 | 0.354458              |
| 4          | Horror                 | 0.353176              |
| 5          | Thriller/Suspense      | 0.326688              |
| 6          | Animation/Family       | 0.319435              |
| 7          | Fantasy                | 0.294314              |
| 8          | Science Fiction (Sci-Fi)| 0.270763             |
| 9          | Documentary            | 0.236453              |
| 10         | Action/Adventure       | 0.236415              |


  </p>
  </div>
  
  <!-- Plot Container -->
  <div style="width: 70%; padding: 10px;">
    <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/20791376"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/20791376/thumbnail" width="100%" alt="bar-chart-race visualization" /></noscript></div>
  </div>

</div>

Romance leads the female presence race, while Action/Adventure and Documentary cling to male-dominant scripts, forging gender imbalances into their narrative DNA.

## **Interpretation and Conclusions**

Across ethnicity, age, and now gender, Hollywood’s patterns form a familiar constellation of bias. Women appear underrepresented, and their visibility swings unpredictably with time and genre. Once again, this echoes the “golden age” concept—Hollywood confines actresses to a youthful prime and restricts their appearance by genre.

Historical studies, like Lauzen’s *The Celluloid Ceiling*, consistently confirm these patterns. Add age-related biases, and you have a constellation of inequalities that Earth’s activists, scholars, and industry reformers have struggled to realign.

---

### **Linking Back to Visual and Historical Observations**

Time-based graphs show that some genres respond to shifts in cultural awareness—like comets passing through new fields of influence—while others resist or lag behind. This ranking and variability suggest that the future of gender parity in Hollywood is still being forged in the fires of shifting tastes, advocacy, and policy changes.

---

### **Conclusion: Situating Gender Findings Alongside Ethnicity and Age**

With this gender analysis, my cosmic survey of Hollywood is nearly complete. Across ethnicity, age, and gender, I found skewed distributions—marginalizing certain ethnicities, concentrating actors in a narrow youthful band, and constraining female representation. These patterns aren’t accidental star dust; they’re shaped by entrenched legacies, cultural codes, and economic gravitational pulls.

Yet, like planets that can realign or stars that can go supernova, there is always the potential for change. By recognizing these patterns, Earthly decision-makers might adjust their cinematic lens. If Hollywood strives to reflect its planet’s true complexity, future Earthlings—and friendly cosmic visitors like myself—may witness storytelling as vast and varied as the universe itself.

---