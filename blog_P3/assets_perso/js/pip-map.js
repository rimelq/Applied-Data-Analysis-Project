document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("map-container");
  const dragButton = document.getElementById("drag-pip");
  const closeButton = document.getElementById("close-pip");

  if (!mapContainer || !dragButton || !closeButton) {
    console.error("Essential elements for PiP functionality are missing.");
    return;
  }

  const mapOffsetTop = mapContainer.offsetTop;
  let isDragging = false;
  let startX, startY, initialX, initialY;

  // Scroll listener for PiP activation and deactivation
  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition > mapOffsetTop + mapContainer.offsetHeight) {
      // Activate PiP mode and position in bottom-right corner
      mapContainer.classList.add("pip");
      if (!isDragging) { // Only set position if not being dragged
        mapContainer.style.left = `${window.innerWidth - mapContainer.offsetWidth - 16}px`; // 16px margin
        mapContainer.style.top = `${window.innerHeight - mapContainer.offsetHeight - 16}px`; // 16px margin
      }
    } else {
      // Deactivate PiP mode and reset position
      mapContainer.classList.remove("pip");
      mapContainer.style.left = ""; // Reset to default horizontal position
      mapContainer.style.top = "";  // Reset to default vertical position
    }
  });

  closeButton.addEventListener("click", () => {
    // Deactivate PiP mode
    mapContainer.classList.remove("pip");
    mapContainer.style.left = ""; // Reset horizontal position
    mapContainer.style.top = "";  // Reset vertical position
    // Scroll back to the main map
    window.scrollTo({ top: mapOffsetTop - 100, behavior: "smooth" });
  });

  // Start dragging
  dragButton.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    initialX = mapContainer.offsetLeft;
    initialY = mapContainer.offsetTop;
    mapContainer.style.transition = "none";
    dragButton.style.cursor = "grabbing";
    document.body.style.userSelect = "none";
    e.preventDefault();
  });

  // Drag logic
  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      mapContainer.style.left = `${initialX + deltaX}px`;
      mapContainer.style.top = `${initialY + deltaY}px`;
    }
  });

  // Stop dragging
  document.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      mapContainer.style.transition = "all 0.3s ease";
      dragButton.style.cursor = "grab";
      document.body.style.userSelect = "";
    }
  });
});
