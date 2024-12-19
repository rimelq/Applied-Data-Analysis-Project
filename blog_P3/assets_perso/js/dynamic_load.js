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

// Function to load the hierarchy visualization
function loadHierarchyPlot() {
    console.log('Loading hierarchy plot');
    const hierarchyContainer = document.getElementById('hierarchy-plot');
    
    if (!hierarchyContainer) {
        console.error('Hierarchy container not found');
        return;
    }

    const hierarchyHTML = `
        <div class="flourish-embed flourish-hierarchy" 
             data-src="visualisation/20799079"
             style="width: 90%; height: 900px; margin: 0 auto;">
            <noscript>
                <img src="https://public.flourish.studio/visualisation/20799079/thumbnail" 
                     width="100%" 
                     alt="hierarchy visualization" />
            </noscript>
        </div>
    `;


    hierarchyContainer.innerHTML = hierarchyHTML;

    // Initialize Flourish for the hierarchy plot
    loadFlourishScript(() => {
        initializeFlourishVisualizations(hierarchyContainer);
    });
}

// New function to load default content (Hollywood)
function loadDefaultContent() {
    console.log('Loading default Hollywood content');
    const contentContainer = document.getElementById('main-content');
    
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
            
            // Initialize all Flourish visualizations in the content
            loadFlourishScript(() => {
                initializeFlourishVisualizations(contentContainer);
            });
        })
        .catch(error => {
            console.error('Error loading default content:', error);
            contentContainer.innerHTML = '<p>Failed to load Hollywood content. Please try again later.</p>';
        });
}

function loadRegionContent(region) {
    console.log(`Loading content for region: ${region}`);
    const contentContainer = document.getElementById('main-content');
    contentContainer.innerHTML = `<p>Loading content for ${region}...</p>`;

    fetch(`/assets/regions/${region}.md`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load content for region: ${region}`);
            }
            return response.text();
        })
        .then(markdown => {
            const htmlContent = marked.parse(markdown);
            contentContainer.innerHTML = htmlContent;
            
            // Initialize all Flourish visualizations in the new content
            loadFlourishScript(() => {
                initializeFlourishVisualizations(contentContainer);
            });
        })
        .catch(error => {
            console.error(error);
            contentContainer.innerHTML = `<p>Failed to load content for ${region}. Please try again later.</p>`;
        });
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization');
    
    // Load Flourish script first
    loadFlourishScript(() => {
        console.log('Flourish script ready - Loading content');
        // Then load hierarchy plot
        loadHierarchyPlot();
        // Then load default content
        setTimeout(() => {
            loadDefaultContent();
        }, 1000); 
    });
});

