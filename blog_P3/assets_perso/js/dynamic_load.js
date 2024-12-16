/*function loadRegionContent(region) {
  const contentContainer = document.getElementById('main-content');

  // Clear existing content
  contentContainer.innerHTML = `<p>Loading content for ${region}...</p>`;

  // Fetch the markdown file for the selected region
  fetch(`/assets/regions/${region}.md`)
      .then(response => {
          if (!response.ok) {
              throw new Error(`Failed to load content for region: ${region}`);
          }
          return response.text();
      })
      .then(markdown => {
          // Convert markdown to HTML using marked.js
          const htmlContent = marked.parse(markdown);
          contentContainer.innerHTML = htmlContent;
      })
      .catch(error => {
          // Handle errors (e.g., file not found)
          console.error(error);
          contentContainer.innerHTML = `<p>Failed to load content for ${region}. Please try again later.</p>`;
      });
}*/

// Function to load the Flourish script dynamically
function loadFlourishScript(callback) {
    const existingScript = document.querySelector('script[src="https://public.flourish.studio/resources/embed.js"]');

    // Remove the script if it already exists (to reload it cleanly)
    if (existingScript) {
        existingScript.remove();
    }

    // Create a new script tag
    const script = document.createElement('script');
    script.src = "https://public.flourish.studio/resources/embed.js";
    script.async = true;

    // On script load, execute the callback to initialize Flourish
    script.onload = () => {
        console.log("Flourish script loaded successfully");
        if (callback && typeof callback === 'function') {
            callback();
        }
    };

    script.onerror = () => {
        console.error("Failed to load Flourish script.");
    };

    // Append the script to the document head
    document.head.appendChild(script);
}

// Function to load Markdown content, parse it, and initialize Flourish embeds
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
        .then(markdownContent => {
            // Convert Markdown to HTML using marked.js
            const htmlContent = marked.parse(markdownContent);

            // Inject the parsed HTML content
            contentContainer.innerHTML = htmlContent;

            // Reload the Flourish script to ensure embeds are initialized
            loadFlourishScript(() => {
                if (window.Flourish && typeof window.Flourish.embed === "object") {
                    Flourish.embed.init();
                    console.log("Flourish embeds re-initialized");
                } else {
                    console.warn("Flourish failed to initialize.");
                }
            });
        })
        .catch(error => {
            console.error(error);
            contentContainer.innerHTML = `<p>Failed to load content for ${region}. Please try again later.</p>`;
        });
}


