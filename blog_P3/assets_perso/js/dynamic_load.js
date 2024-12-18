// Define the global Flourish object to control behavior
window.Flourish = {
    disable_autoload: true // Prevent Flourish from automatically loading placeholders on script load
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


function loadRegionContent(region) {
    const contentContainer = document.getElementById('main-content');

    // Clear existing content
    contentContainer.innerHTML = `<p>Loading content for ${region}...</p>`;

    // Fetch the Markdown file for the selected region
    fetch(`/assets/regions/${region}.md`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load content for region: ${region}`);
            }
            return response.text();
        })
        .then(markdown => {
            // Convert Markdown to HTML (using marked.js or another library)
            const htmlContent = marked.parse(markdown);

            // Inject the converted HTML into the container
            contentContainer.innerHTML = htmlContent;

            // Dynamically load and process Flourish embeds
            loadFlourishScript(() => {
                const flourishPlaceholders = document.querySelectorAll('.flourish-embed');
                flourishPlaceholders.forEach(placeholder => {
                    if (window.Flourish && window.Flourish.loadEmbed) {
                        window.Flourish.loadEmbed(placeholder);
                    } else {
                        console.warn("Flourish.loadEmbed not available.");
                    }
                });
            });
        })
        .catch(error => {
            console.error(error);
            contentContainer.innerHTML = `<p>Failed to load content for ${region}. Please try again later.</p>`;
        });
}

