// Define the global Flourish object to control behavior
window.Flourish = {
    disable_autoload: true 
};

// Load the Flourish embed script only once
let flourishScriptLoaded = false;

function loadFlourishScript(callback) {
    if (flourishScriptLoaded) {
        callback();
        return;
    }

    // Create the script tag for Flourish embed
    const script = document.createElement('script');
    script.src = "https://public.flourish.studio/resources/embed.js";
    script.async = true;

    script.onload = () => {
        console.log("Flourish script loaded successfully.");
        flourishScriptLoaded = true;
        callback();
    };

    script.onerror = () => {
        console.error("Failed to load Flourish script.");
    };

    document.head.appendChild(script);
}

// Function to initialize all Flourish visualizations in a container
function initializeFlourishVisualizations(container) {
    console.log('Initializing Flourish visualizations in container:', container);
    const flourishPlaceholders = container.querySelectorAll('.flourish-embed');
    console.log('Found Flourish placeholders:', flourishPlaceholders.length);
    
    flourishPlaceholders.forEach((placeholder, index) => {
        console.log(`Initializing Flourish visualization ${index + 1}`);
        if (window.Flourish && window.Flourish.loadEmbed) {
            window.Flourish.loadEmbed(placeholder);
        } else {
            console.warn(`Flourish.loadEmbed not available for visualization ${index + 1}`);
        }
    });
}

// Function to load default content (Hollywood)
function loadDefaultContent() {
    console.log('Loading default Hollywood content');
    const contentContainer = document.getElementById('main-content');
    
    if (!contentContainer) {
        console.error('Content container not found');
        return;
    }

    contentContainer.innerHTML = '<p>Loading Hollywood content...</p>';
    
    fetch('/assets/regions/US.md')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(markdown => {
            console.log('Markdown content loaded, converting to HTML');
            const htmlContent = marked.parse(markdown);
            contentContainer.innerHTML = htmlContent;
            
            // Add selectors after the content is loaded
            setTimeout(() => {
                console.log('Adding selectors');
                createPeriodSelector('hollywood', contentContainer);
                createChartTypeSelector('hollywood', contentContainer);
                createAgePeriodSelector('hollywood', contentContainer);
                createStatisticSelector('hollywood', contentContainer);
                createGenreSelector('hollywood', contentContainer);
                
                // Add regression plot widget
                createRegressionPlotWidget(contentContainer);

                loadFlourishScript(() => {
                    console.log('Initializing visualizations');
                    initializeFlourishVisualizations(contentContainer);
                });
            }, 0);
        })
        .catch(error => {
            console.error('Error loading default content:', error);
            contentContainer.innerHTML = '<p>Failed to load Hollywood content. Please try again later.</p>';
        });
}

// Add new function to create and handle the period selector for East Asia
function createEAPeriodSelector(container) {
    // Create a dedicated container for the selector and visualization
    const selectorContainerHTML = `
        <div class="ethnicity-analysis-container" style="margin: 40px 0;">
            <div class="period-selector-wrapper" style="margin-bottom: 20px; text-align: left;">
                <label for="ea-period-select" style="font-weight: bold;">Select Period: </label>
                <select id="ea-period-select" class="form-select">
                    <option value="All periods">All periods</option>
                    <option value="1950-1965">1950-1965</option>
                    <option value="1966-1980">1966-1980</option>
                    <option value="1981-1995">1981-1995</option>
                    <option value="1996-2012">1996-2012</option>
                </select>
            </div>
            <div id="ea-visualization-container">
                <div class="flourish-embed flourish-chart" data-src="visualisation/20792125">
                    <noscript>
                        <img src="https://public.flourish.studio/visualisation/20792125/thumbnail" 
                             width="100%" 
                             alt="chart visualization" />
                    </noscript>
                </div>
            </div>
        </div>
    `;

    // Find the introduction section using Array.from and find
    const headers = Array.from(container.getElementsByTagName('h2'));
    const introSection = headers.find(header => header.textContent.includes('Introduction'));

    if (introSection) {
        // Insert after the paragraph following the introduction
        let targetElement = introSection;
        while (targetElement.nextElementSibling && targetElement.nextElementSibling.tagName === 'P') {
            targetElement = targetElement.nextElementSibling;
        }
        targetElement.insertAdjacentHTML('afterend', selectorContainerHTML);
    } else {
        // Fallback: insert at a specific location
        const visualizationPlaceholder = container.querySelector('.flourish-embed');
        if (visualizationPlaceholder) {
            visualizationPlaceholder.insertAdjacentHTML('beforebegin', selectorContainerHTML);
        } else {
            // If no suitable location is found, append to the container
            container.insertAdjacentHTML('beforeend', selectorContainerHTML);
        }
    }

    // Add event listener to the selector
    document.getElementById('ea-period-select').addEventListener('change', function(e) {
        const selectedPeriod = e.target.value;
        updateEAVisualization(selectedPeriod);
    });
}

function updateEAVisualization(period) {
    const visualizationIds = {
        'All periods': '20792125',
        '1950-1965': '20791642',
        '1966-1980': '20791740',
        '1981-1995': '20791774',
        '1996-2012': '20791794'
    };

    const newVisualizationId = visualizationIds[period];
    const container = document.getElementById('ea-visualization-container');
    
    if (container) {
        // Create new visualization HTML
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-chart" data-src="visualisation/${newVisualizationId}">
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" 
                         width="100%" 
                         alt="chart visualization" />
                </noscript>
            </div>
        `;
        
        // Replace the existing visualization
        container.innerHTML = newVisualizationHTML;
        
        // Reinitialize the visualization
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}

function createPeriodSelector(region, container) {
    const visualizationIds = {
        'bollywood': {
            'All periods': '20792116',
            '1950-1965': '20791501',
            '1966-1980': '20791556',
            '1981-1995': '20791616',
            '1996-2012': '20791634'
        },
        'hollywood': {
            'All periods': '20792106',
            '1950-1965': '20792225',
            '1966-1980': '20791365',
            '1981-1995': '20791451',
            '1996-2012': '20791472'
        }
    };

    const selectorContainerHTML = `
        <div class="ethnicity-analysis-container" style="margin: 40px 0;">
            <div class="period-selector-wrapper" style="margin-bottom: 20px; text-align: left;">
                <label for="${region}-period-select" style="font-weight: bold;">Select Period: </label>
                <select id="${region}-period-select" class="form-select">
                    <option value="All periods">All periods</option>
                    <option value="1950-1965">1950-1965</option>
                    <option value="1966-1980">1966-1980</option>
                    <option value="1981-1995">1981-1995</option>
                    <option value="1996-2012">1996-2012</option>
                </select>
            </div>
            <div id="${region}-visualization-container">
                <div class="flourish-embed flourish-chart" data-src="visualisation/${visualizationIds[region]['All periods']}">
                    <noscript>
                        <img src="https://public.flourish.studio/visualisation/${visualizationIds[region]['All periods']}/thumbnail" 
                             width="100%" 
                             alt="chart visualization" />
                    </noscript>
                </div>
            </div>
        </div>
    `;

    // Find the Preliminary Visualizations title
    const headers = Array.from(container.getElementsByTagName('h2'));
    const prelimTitle = headers.find(header => header.textContent.includes('Preliminary Visualizations'));

    if (prelimTitle) {
        prelimTitle.insertAdjacentHTML('afterend', selectorContainerHTML);
    }

    // Add event listener to the selector
    document.getElementById(`${region}-period-select`).addEventListener('change', function(e) {
        const selectedPeriod = e.target.value;
        updateVisualization(region, selectedPeriod, visualizationIds[region]);
    });
}

function updateVisualization(region, period, visualizationIds) {
    const newVisualizationId = visualizationIds[period];
    const container = document.getElementById(`${region}-visualization-container`);
    
    if (container) {
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-chart" data-src="visualisation/${newVisualizationId}">
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" 
                         width="100%" 
                         alt="chart visualization" />
                </noscript>
            </div>
        `;
        
        container.innerHTML = newVisualizationHTML;
        
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}

function createAgePeriodSelector(region, container) {
    const visualizationIds = {
        'hollywood': {
            'All periods': '20797028',
            '1950-1965': '20797024',
            '1966-1980': '20797034',
            '1981-1995': '20797039',
            '1996-2012': '20797045'
        },
        'bollywood': {
            'All periods': '20797096',
            '1950-1965': '20797100',
            '1966-1980': '20797103',
            '1981-1995': '20797111',
            '1996-2012': '20797118'
        },
        'eastasia': {
            'All periods': '20797056',
            '1950-1965': '20797063',
            '1966-1980': '20797061',
            '1981-1995': '20797058',
            '1996-2012': '20797059'
        },
        'europe': {
            'All periods': '20780324',
            '1950-1965': '20792399',
            '1966-1980': '20792243',
            '1981-1995': '20796749',
            '1996-2012': '20796924'
        }
    };

    const selectorContainerHTML = `
        <div class="age-analysis-container" style="margin: 40px 0;">
            <div class="period-selector-wrapper" style="margin-bottom: 20px; text-align: left;">
                <label for="${region}-age-period-select" style="font-weight: bold;">Select Period: </label>
                <select id="${region}-age-period-select" class="form-select">
                    <option value="All periods">All periods</option>
                    <option value="1950-1965">1950-1965</option>
                    <option value="1966-1980">1966-1980</option>
                    <option value="1981-1995">1981-1995</option>
                    <option value="1996-2012">1996-2012</option>
                </select>
            </div>
            <div id="${region}-age-visualization-container">
                <div class="flourish-embed flourish-chart" data-src="visualisation/${visualizationIds[region]['All periods']}">
                    <noscript>
                        <img src="https://public.flourish.studio/visualisation/${visualizationIds[region]['All periods']}/thumbnail" 
                             width="100%" 
                             alt="chart visualization" />
                    </noscript>
                </div>
            </div>
        </div>
    `;

    // Find the Age Distribution title
    const headers = Array.from(container.getElementsByTagName('h2'));
    const ageTitle = headers.find(header => header.textContent.includes('Preliminary Plots: Actor vs. Real-World Age Distributions'));

    if (ageTitle) {
        ageTitle.insertAdjacentHTML('afterend', selectorContainerHTML);
    }

    // Add event listener to the selector
    document.getElementById(`${region}-age-period-select`).addEventListener('change', function(e) {
        const selectedPeriod = e.target.value;
        updateAgeVisualization(region, selectedPeriod, visualizationIds[region]);
    });
}

function updateAgeVisualization(region, period, visualizationIds) {
    const newVisualizationId = visualizationIds[period];
    const container = document.getElementById(`${region}-age-visualization-container`);
    
    if (container) {
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-chart" data-src="visualisation/${newVisualizationId}">
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" 
                         width="100%" 
                         alt="chart visualization" />
                </noscript>
            </div>
        `;
        
        container.innerHTML = newVisualizationHTML;
        
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}

function createChartTypeSelector(region, container) {
    const visualizationIds = {
        'ethnicity': '20843178',
        'age': '20843122',
        'gender': '20843169'
    };

    const selectorContainerHTML = `
        <div class="chart-selector-container" style="text-align: center; margin-top: 20px;">
            <label for="${region}-chart-type-select" style="font-weight: bold;">Select Statistic: </label>
            <select id="${region}-chart-type-select" class="form-select">
                <option value="ethnicity">Ethnicity</option>
                <option value="age">Age</option>
                <option value="gender">Gender</option>
            </select>
        </div>
        <div id="${region}-chart-visualization-container" style="margin-top: 20px;">
            <div class="flourish-embed flourish-chart" data-src="visualisation/${visualizationIds['ethnicity']}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${visualizationIds['ethnicity']}/thumbnail" width="100%" alt="chart visualization" />
                </noscript>
            </div>
        </div>
    `;

    // Find the Combination Dual-Axis Charts title
    const headers = Array.from(container.getElementsByTagName('h2'));
    const chartTitle = headers.find(header => header.textContent.includes('Combination Dual-Axis Charts: Hollywood'));

    if (chartTitle) {
        chartTitle.insertAdjacentHTML('afterend', selectorContainerHTML);
        console.log(`Inserted chart selector for ${region}`);
    } else {
        console.error(`Chart title not found for ${region}`);
    }

    const selectElement = document.getElementById(`${region}-chart-type-select`);
    if (selectElement) {
        selectElement.addEventListener('change', function(e) {
            const selectedType = e.target.value;
            updateChartVisualization(region, selectedType, visualizationIds);
        });
    } else {
        console.error(`Select element not found for ${region}`);
    }
}

function updateChartVisualization(region, type, visualizationIds) {
    const newVisualizationId = visualizationIds[type];
    const container = document.getElementById(`${region}-chart-visualization-container`);
    
    if (container) {
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-chart" data-src="visualisation/${newVisualizationId}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" width="100%" alt="chart visualization" />
                </noscript>
            </div>
        `;
        container.innerHTML = newVisualizationHTML;
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}

function createStatisticSelector(region, container) {
    const visualizationIds = {
        'ethnicity': '20821631',
        'age': '20821662',
        'gender': '20821797'
    };

    const selectorContainerHTML = `
        <div class="statistic-selector-container" style="text-align: center; margin-top: 20px;">
            <label for="${region}-statistic-select" style="font-weight: bold;">Select Statistic: </label>
            <select id="${region}-statistic-select" class="form-select">
                <option value="ethnicity">Ethnicity</option>
                <option value="age">Age</option>
                <option value="gender">Gender</option>
            </select>
        </div>
        <div id="${region}-statistic-visualization-container" style="margin-top: 20px;">
            <div class="flourish-embed flourish-sankey" data-src="visualisation/${visualizationIds['ethnicity']}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${visualizationIds['ethnicity']}/thumbnail" width="100%" alt="sankey visualization" />
                </noscript>
            </div>
        </div>
    `;

    // Find the Representation Gaps title
    const headers = Array.from(container.getElementsByTagName('h2'));
    const statisticTitle = headers.find(header => header.textContent.includes('Representation Gaps and Box Office Revenue Impact: Hollywood'));

    if (statisticTitle) {
        statisticTitle.insertAdjacentHTML('afterend', selectorContainerHTML);
        console.log(`Inserted statistic selector for ${region}`);
    } else {
        console.error(`Statistic title not found for ${region}`);
    }

    const selectElement = document.getElementById(`${region}-statistic-select`);
    if (selectElement) {
        selectElement.addEventListener('change', function(e) {
            const selectedType = e.target.value;
            updateStatisticVisualization(region, selectedType, visualizationIds);
        });
    } else {
        console.error(`Select element not found for ${region}`);
    }
}

function updateStatisticVisualization(region, type, visualizationIds) {
    const newVisualizationId = visualizationIds[type];
    const container = document.getElementById(`${region}-statistic-visualization-container`);
    
    if (container) {
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-sankey" data-src="visualisation/${newVisualizationId}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" width="100%" alt="sankey visualization" />
                </noscript>
            </div>
        `;
        container.innerHTML = newVisualizationHTML;
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}

function createGenreSelector(region, container) {
    const visualizationIds = {
        'all': '20790816',
        'action': '20789903',
        'animation': '20791025',
        'comedy': '20790991',
        'documentary': '20790980',
        'drama': '20790976',
        'fantasy': '20790972',
        'horror': '20790943',
        'romance': '20790931',
        'scifi': '20790837',
        'thriller': '20790826'
    };

    const selectorContainerHTML = `
        <div class="genre-selector-container" style="text-align: center; margin-top: 20px;">
            <label for="${region}-genre-select" style="font-weight: bold;">Select Genre: </label>
            <select id="${region}-genre-select" class="form-select">
                <option value="all">All movie genres</option>
                <option value="action">Action & Adventure</option>
                <option value="animation">Animation & Family</option>
                <option value="comedy">Comedy</option>
                <option value="documentary">Documentary</option>
                <option value="drama">Drama</option>
                <option value="fantasy">Fantasy</option>
                <option value="horror">Horror</option>
                <option value="romance">Romance</option>
                <option value="scifi">Science Fiction</option>
                <option value="thriller">Thriller & Suspense</option>
            </select>
        </div>
        <div id="${region}-genre-visualization-container" style="margin-top: 20px;">
            <div class="flourish-embed flourish-chart" data-src="visualisation/${visualizationIds['all']}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${visualizationIds['all']}/thumbnail" width="100%" alt="chart visualization" />
                </noscript>
            </div>
        </div>
    `;

    // Find the Interpretation of Ethnicity Trends title
    const headers = Array.from(container.getElementsByTagName('h2'));
    const genreTitle = headers.find(header => header.textContent.includes('Interpretation of Ethnicity Trends'));

    if (genreTitle) {
        genreTitle.insertAdjacentHTML('afterend', selectorContainerHTML);
        console.log(`Inserted genre selector for ${region}`);
    } else {
        console.error(`Genre title not found for ${region}`);
    }

    const selectElement = document.getElementById(`${region}-genre-select`);
    if (selectElement) {
        selectElement.addEventListener('change', function(e) {
            const selectedGenre = e.target.value;
            updateGenreVisualization(region, selectedGenre, visualizationIds);
        });
    } else {
        console.error(`Select element not found for ${region}`);
    }
}

function updateGenreVisualization(region, genre, visualizationIds) {
    const newVisualizationId = visualizationIds[genre];
    const container = document.getElementById(`${region}-genre-visualization-container`);
    
    if (container) {
        const newVisualizationHTML = `
            <div class="flourish-embed flourish-chart" data-src="visualisation/${newVisualizationId}">
                <script src="https://public.flourish.studio/resources/embed.js"></script>
                <noscript>
                    <img src="https://public.flourish.studio/visualisation/${newVisualizationId}/thumbnail" width="100%" alt="chart visualization" />
                </noscript>
            </div>
        `;
        container.innerHTML = newVisualizationHTML;
        loadFlourishScript(() => {
            initializeFlourishVisualizations(container);
        });
    }
}


function createRegressionPlotWidget(container) {
    const visualizationPaths = {
        'hollywood': '/assets/plots/box-office/regression_plot_Hollywood.html',
        'bollywood': '/assets/plots/box-office/regression_plot_Bollywood.html',
        'eastasia': '/assets/plots/box-office/regression_plot_Eastasia.html',
        'europe': '/assets/plots/box-office/regression_plot_Europe.html'
    };

    const widgetHTML = `
        <div class="regression-plot-widget" style="margin: 40px 0;">
            <label for="region-select" style="font-weight: bold;">Select Region: </label>
            <select id="region-select" class="form-select">
                <option value="hollywood">Hollywood</option>
                <option value="bollywood">Bollywood</option>
                <option value="eastasia">East Asia</option>
                <option value="europe">Europe</option>
            </select>
            <div id="regression-plot-container" style="margin-top: 20px;">
                <iframe src="${visualizationPaths['hollywood']}" width="100%" height="400px" style="border:none;"></iframe>
            </div>
        </div>
    `;

    // Find the specific line to insert after
    const headers = Array.from(container.getElementsByTagName('h2'));
    const regressionTitle = headers.find(header => header.textContent.includes('4. Linear Regression Analyses'));

    if (regressionTitle) {
        regressionTitle.insertAdjacentHTML('afterend', widgetHTML);
        console.log('Inserted regression plot widget');
    } else {
        console.error('Regression title not found');
    }

    // Add event listener to the dropdown
    const selectElement = document.getElementById('region-select');
    selectElement.addEventListener('change', function(e) {
        const selectedRegion = e.target.value;
        const container = document.getElementById('regression-plot-container');
        container.innerHTML = `<iframe src="${visualizationPaths[selectedRegion]}" width="100%" height="400px" style="border:none;"></iframe>`;
    });
}

// Modify the loadRegionContent function to include the regression plot widget
function loadRegionContent(region) {

    const map = simplemaps_worldmap; // Reference to the map instance

    // Reset opacity for all regions
    Object.keys(map.mapdata.regions).forEach(key => {
        map.mapdata.regions[key]['color'] = "#5B3C89";
        if (map.mapdata.regions[key]['name'] == region) {
            map.mapdata.regions[key]['color'] = '#e66575';
            console.warn(`Region ${region} opacity updated to:`, map.mapdata.regions[key]['color']);
            }
    });



    // Reload the map to apply changes
    
    //map.load();


    // Reload the map to apply the changes
    //map.load();
  
    const contentContainer = document.getElementById('main-content');
    
    if (!contentContainer) {
        console.error('Content container not found');
        return;
    }

    contentContainer.innerHTML = `<p>Loading content for ${region}...</p>`;
    const markdownPath = `/assets/regions/${region}.md`;

    fetch(markdownPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(markdown => {
            console.log('Markdown content loaded successfully');
            const htmlContent = marked.parse(markdown);
            contentContainer.innerHTML = htmlContent;
            
            // Add period selectors based on region
            if (region === 'EA') {
                createEAPeriodSelector(contentContainer);
                createAgePeriodSelector('eastasia', contentContainer);
            } else if (region === 'IN') {
                createPeriodSelector('bollywood', contentContainer);
                createAgePeriodSelector('bollywood', contentContainer);
            } else if (region === 'US') {
                createPeriodSelector('hollywood', contentContainer);
                createAgePeriodSelector('hollywood', contentContainer);
            } else if (region === 'EU') {
                createAgePeriodSelector('europe', contentContainer);
            }
            
            // Add chart type selectors based on region
            if (region === 'EA') {
                createChartTypeSelector('eastasia', contentContainer);
            } else if (region === 'IN') {
                createChartTypeSelector('bollywood', contentContainer);
            } else if (region === 'US') {
                createChartTypeSelector('hollywood', contentContainer);
            } else if (region === 'EU') {
                createChartTypeSelector('europe', contentContainer);
            }
            
            // Add statistic selectors based on region
            if (region === 'EA') {
                createStatisticSelector('eastasia', contentContainer);
            } else if (region === 'IN') {
                createStatisticSelector('bollywood', contentContainer);
            } else if (region === 'US') {
                createStatisticSelector('hollywood', contentContainer);
            } else if (region === 'EU') {
                createStatisticSelector('europe', contentContainer);
            }
            
            // Add genre selectors
            if (region === 'US') {
                createGenreSelector('hollywood', contentContainer);
            }
            
            // Add regression plot widget
            createRegressionPlotWidget(contentContainer);
            
            loadFlourishScript(() => {
                initializeFlourishVisualizations(contentContainer);
            });
        })
        .catch(error => {
            console.error('Error loading region content:', error);
            contentContainer.innerHTML = `
                <div style="padding: 20px; text-align: center;">
                    <h2>Error Loading Content</h2>
                    <p>Failed to load content for ${region}. Please try again later.</p>
                    <p>Error details: ${error.message}</p>
                </div>
            `;
        });
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization');
    
    // Load Flourish script first
    loadFlourishScript(() => {
        console.log('Flourish script ready - Loading content');
        // Then load default content
        setTimeout(() => {
            loadDefaultContent();
        }, 1000); 
    });
});

