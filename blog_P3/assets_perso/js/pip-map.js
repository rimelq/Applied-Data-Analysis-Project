document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("map-container");
  const closeButton = document.getElementById("close-pip");
  const mapOffsetTop = mapContainer.offsetTop;

  // Add scroll listener to detect PiP mode
  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition > mapOffsetTop + mapContainer.offsetHeight) {
      mapContainer.classList.add("pip");
      closeButton.style.display = "block"; // Show the close button
    } else {
      mapContainer.classList.remove("pip");
      closeButton.style.display = "none"; // Hide the close button
    }
  });

  // Add click event listener for the close button
  closeButton.addEventListener("click", () => {
    mapContainer.classList.remove("pip");
    closeButton.style.display = "none"; // Hide the button
    window.scrollTo({ top: mapOffsetTop - 50, behavior: "smooth" }); // Scroll back to the map
  });
});
