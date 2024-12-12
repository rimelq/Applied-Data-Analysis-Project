document.addEventListener("DOMContentLoaded", () => {
  // Select the map container
  const mapContainer = document.getElementById("map-container");

  // Get the position of the map relative to the page
  const mapOffsetTop = mapContainer.offsetTop;

  const pipMapContainer = document.getElementById("map-container");
  const dragButton = document.getElementById("drag-pip");

  let isDragging = false;
  let startX, startY, initialX, initialY;


  // Add a scroll event listener to the window
  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    // Check if the user has scrolled past the map
    if (scrollPosition > mapOffsetTop + mapContainer.offsetHeight) {
      mapContainer.classList.add("pip"); // Add PiP class
    } else {
      mapContainer.classList.remove("pip"); // Remove PiP class
    }
  });

  // Start dragging when the drag button is pressed
  dragButton.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX; // Record mouse X-coordinate
    startY = e.clientY; // Record mouse Y-coordinate
    initialX = pipMapContainer.offsetLeft; // Current X of PiP container
    initialY = pipMapContainer.offsetTop; // Current Y of PiP container
    pipMapContainer.style.transition = "none"; // Disable smooth transitions while dragging
    dragButton.style.cursor = "grabbing"; // Change cursor to grabbing
    document.body.style.userSelect = "none"; // Disable text selection during drag
    e.preventDefault(); // Prevent default behavior (e.g., text selection)
  });

  // Move the container while dragging
  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const deltaX = e.clientX - startX; // Horizontal movement
      const deltaY = e.clientY - startY; // Vertical movement
      pipMapContainer.style.left = `${initialX + deltaX}px`; // Update X position
      pipMapContainer.style.top = `${initialY + deltaY}px`; // Update Y position
    }
  });

  // Stop dragging when the mouse button is released
  document.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      pipMapContainer.style.transition = "all 0.3s ease"; // Re-enable transitions
      dragButton.style.cursor = "grab"; // Reset cursor to grab
      document.body.style.userSelect = ""; // Re-enable text selection
    }
  });


});
