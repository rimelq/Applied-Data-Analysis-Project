document.addEventListener("DOMContentLoaded", () => {
  // Select the map container and buttons
  const mapContainer = document.getElementById("map-container");
  const dragButton = document.getElementById("drag-pip");
  const closeButton = document.getElementById("close-pip");
  const resizeHandles = document.querySelectorAll(".resize-handle"); // Resizing handles
  const mapOffsetTop = mapContainer.offsetTop;

  let isDragging = false;
  let isResizing = false;
  let startX, startY, initialX, initialY, startWidth, startHeight;
  let currentHandle; // To track the active handle
  let scrollTimeout;

  // --- MODIFICATION: Ensure essential elements exist ---
  if (!mapContainer || !dragButton || !closeButton || resizeHandles.length === 0) {
    console.error("Essential elements for PiP functionality are missing.");
    return;
  }

  
  // --- Enable PiP mode on scroll ---
  window.addEventListener("scroll", () => {
    clearTimeout(scrollTimeout);

    // const scrollPosition = window.scrollY;
    // const mapOffsetTop = mapContainer.offsetTop;
    // const mapHeight = mapContainer.offsetHeight;
    // const viewportHeight = window.innerHeight;
    // const offsetThreshold = mapOffsetTop + mapHeight - viewportHeight + 2700;
    const scrollPosition = window.scrollY;
    const mapOffsetTop = mapContainer.offsetTop;
    const mapHeight = mapContainer.offsetHeight;
    const viewportHeight = window.innerHeight;
    const offsetThreshold = mapOffsetTop + mapHeight - viewportHeight;

    if (scrollPosition > offsetThreshold) {
      scrollTimeout = setTimeout(() => {
        mapContainer.classList.add("pip");
        dragButton.style.display = "block";
        closeButton.style.display = "block";

        if (!mapContainer.style.width || !mapContainer.style.height) {
          mapContainer.style.width = "200px";
          mapContainer.style.height = "150px";
          console.log("Initial PiP dimensions set.");
        }
      }, 50);
    } else {
      mapContainer.classList.remove("pip"); // Remove PiP mode
      dragButton.style.display = "none"; // Hide drag button
      closeButton.style.display = "none"; // Hide close button
      resetPiPPosition(); // Reset PiP to its original position
    }
  });

  // --- Dragging logic for the PiP window ---
  dragButton.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    initialX = mapContainer.offsetLeft;
    initialY = mapContainer.offsetTop;
    mapContainer.style.transition = "none"; // Disable transitions during dragging
    dragButton.style.cursor = "grabbing";
    document.body.style.userSelect = "none"; // Disable text selection
    e.preventDefault();
  });

  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      mapContainer.style.left = `${initialX + deltaX}px`;
      mapContainer.style.top = `${initialY + deltaY}px`;
    }

    if (isResizing) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      // Adjust sides based on the handle being dragged
      /*if (currentHandle.classList.contains("top-left")) {
        mapContainer.style.width = `${startWidth - deltaX}px`;
        mapContainer.style.height = `${startHeight - deltaY}px`;
        mapContainer.style.left = `${initialX + deltaX}px`;
        mapContainer.style.top = `${initialY + deltaY}px`;
      } else if (currentHandle.classList.contains("top-right")) {
        mapContainer.style.width = `${startWidth + deltaX}px`;
        mapContainer.style.height = `${startHeight - deltaY}px`;
        mapContainer.style.top = `${initialY + deltaY}px`;
      } else if (currentHandle.classList.contains("bottom-left")) {
        mapContainer.style.width = `${startWidth - deltaX}px`;
        mapContainer.style.height = `${startHeight + deltaY}px`;
        mapContainer.style.left = `${initialX + deltaX}px`;
      } else */if (currentHandle.classList.contains("bottom-right")) {
        mapContainer.style.width = `${startWidth + deltaX}px`;
        mapContainer.style.height = `${startHeight + deltaY}px`;
      }

      // Prevent the container from collapsing below minimum size
      const newWidth = Math.max(400, parseInt(mapContainer.style.width));
      const newHeight = Math.max(2000, parseInt(mapContainer.style.height));
      mapContainer.style.width = `${newWidth}px`;
      mapContainer.style.height = `${newHeight}px`;
    }
  });

  document.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      mapContainer.style.transition = "all 0.3s ease";
      dragButton.style.cursor = "grab";
      document.body.style.userSelect = ""; // Re-enable text selection
    }if (isResizing) {
      isResizing = false;
      currentHandle.style.cursor = ""; // Reset cursor
      console.log("Resizing complete. Final dimensions:", {
        width: mapContainer.offsetWidth,
        height: mapContainer.offsetHeight,
      });
    }
  });

  // --- Resizing logic for the PiP window ---
  resizeHandles.forEach((handle) => {
    handle.addEventListener("mousedown", (e) => {
      isResizing = true;
      currentHandle = handle;
      startX = e.clientX;
      startY = e.clientY;
      startWidth = mapContainer.offsetWidth;
      startHeight = mapContainer.offsetHeight;
      initialX = mapContainer.offsetLeft;
      initialY = mapContainer.offsetTop;
      handle.style.cursor = "nwse-resize";
      mapContainer.style.transition = "none"; // Disable transitions during resize
      e.preventDefault();
    });
  });

  document.addEventListener("mousemove", (e) => {
    if (isResizing) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      // Update width and height of the PiP container
      const newWidth = Math.max(200, startWidth + deltaX); // Minimum width 200px
      const newHeight = Math.max(150, startHeight + deltaY); // Minimum height 150px
      mapContainer.style.width = `${newWidth}px`;
      mapContainer.style.height = `${newHeight}px`;

      // Debugging: Log the new dimensions
      console.log("Resizing to:", { width: newWidth, height: newHeight });
    }
  });

  document.addEventListener("mouseup", () => {
    if (isResizing) {
      isResizing = false;
      mapContainer.style.transition = "all 0.3s ease";
      console.log("Resizing complete. Final dimensions:", {
        width: mapContainer.offsetWidth,
        height: mapContainer.offsetHeight,
      });
    }
  });

  // --- Close button functionality ---
  closeButton.addEventListener("click", () => {
    mapContainer.classList.remove("pip");
    closeButton.style.display = "none";
    dragButton.style.display = "none";
    resetPiPPosition(); // Reset position when closed
    window.scrollTo({ top: mapOffsetTop - 50, behavior: "smooth" });
  });

  // --- Helper function to reset PiP position ---
  function resetPiPPosition() {
    mapContainer.style.left = ""; // Reset left position
    mapContainer.style.top = ""; // Reset top position
    mapContainer.style.width = ""; // Reset width
    mapContainer.style.height = ""; // Reset height
    mapContainer.style.display = "block"; // Ensure the map remains visible
    console.log("PiP position and size reset.");
  }

  // --- DEBUGGING LOGS ---
  console.log("Resize handles detected:", resizeHandles);
  console.log("Initial PiP dimensions:", {
    width: mapContainer.offsetWidth,
    height: mapContainer.offsetHeight,
  });
});
