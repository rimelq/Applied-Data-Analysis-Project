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

function loadRegionContent(region) {
    const contentContainer = document.getElementById('main-content');

    // Clear existing content
    contentContainer.innerHTML = `<p>Loading content for ${region}...</p>`;

    // Fetch the HTML file for the selected region
    fetch(`/assets/regions/${region}.html`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load content for region: ${region}`);
            }
            return response.text();
        })
        .then(htmlContent => {
            // Inject the HTML content
            contentContainer.innerHTML = htmlContent;

            // Manually trigger Flourish re-initialization after content load
            if (window.Flourish && typeof window.Flourish.embed === "object") {
                Flourish.embed.init();
                console.log("Flourish embeds re-initialized");
            } else {
                console.warn("Flourish script not loaded properly.");
            }
        })
        .catch(error => {
            console.error(error);
            contentContainer.innerHTML = `<p>Failed to load content for ${region}. Please try again later.</p>`;
        });
}

