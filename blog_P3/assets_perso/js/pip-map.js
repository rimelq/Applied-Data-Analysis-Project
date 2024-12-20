document.addEventListener("DOMContentLoaded", () => {
  // Select the map container and buttons
  const mapContainer = document.getElementById("map-container");
  const pipContainer = document.getElementById("pip-map-container");
  const map = document.getElementById("map");
  const placeholder = document.getElementById("placeholder");
  const dragButton = document.getElementById("drag-pip");
  const closeButton = document.getElementById("close-pip");
  const resizeHandles = document.querySelectorAll(".resize-handle"); // Resizing handles
  const mapOffsetTop = mapContainer.offsetTop;

  let isDragging = false;
  let isResizing = false;
  let startX, startY, initialX, initialY, startWidth, startHeight;
  let currentHandle; // To track the active handle
  let pipModeEnabled = false; // Track if PiP is already enabled


  
  let offsetThreshold;
  let debounceTimer = null;
  let lastScrollY = 0;

  // --- Function to Check if the Bottom of the Map is Out of View ---
  const isMapOutOfView = () => {
    const mapRect = mapContainer.getBoundingClientRect();
    return mapRect.bottom <= 0 ;
  };

  // --- MODIFICATION: Ensure essential elements exist ---
  if (!mapContainer || !dragButton || !closeButton || resizeHandles.length === 0) {
    console.error("Essential elements for PiP functionality are missing.");
    return;
  }

  window.addEventListener("load", () => {
    console.log("Page fully loaded. Initializing PiP scroll logic...");
    const mapHeight = mapContainer.offsetHeight;
    const viewportHeight = window.innerHeight;
    const savedScrollPosition = localStorage.getItem("scrollPosition");
    loadDefaultContent()
    if (savedScrollPosition) {
      window.scrollTo(0, parseInt(savedScrollPosition, 10)); // Scroll to saved position
      localStorage.removeItem("scrollPosition"); // Clear saved position
    }
  });


  // --- Enable PiP mode on scroll ---
  window.addEventListener("scroll", () => {
    const currentScroll = window.scrollY;
    //console.warn("Current scroll:", currentScroll, "Threshold:", offsetThreshold);


  // Debounce to prevent rapid state changes during scroll jumps
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      if (Math.abs(currentScroll - lastScrollY) < 50) {
        // Ignore small scroll jumps (less than 50px)
        return;
      }

      if (isMapOutOfView() && !pipModeEnabled) {
        // Enter PiP mode
        placeholder.style.width = `${mapContainer.offsetWidth}px`;
        placeholder.style.height = `${mapContainer.offsetHeight}px`;
        placeholder.style.background = "transparent"; // Transparent to match the design
        mapContainer.appendChild(placeholder);
        pipModeEnabled = true;
        pipContainer.appendChild(map);
        pipContainer.style.display = "block";
        dragButton.style.display = "block";
        closeButton.style.display = "block";

        if (!pipContainer.style.width || !pipContainer.style.height) {
          pipContainer.style.width = "200px";
          pipContainer.style.height = "150px";
          console.log("PiP activated with initial dimensions.");
        }
      } else if ((!isMapOutOfView()) && pipModeEnabled) {
        // Exit PiP mode
        pipModeEnabled = false;
        console.warn("Before PiP mode:", {
          width: mapContainer.offsetWidth,
          height: mapContainer.offsetHeight,
        });
        mapContainer.removeChild(placeholder)
        mapContainer.appendChild(map);
        console.warn("After PiP mode:", {
          width: mapContainer.offsetWidth,
          height: mapContainer.offsetHeight,
        });
        pipContainer.style.display = "none";
        dragButton.style.display = "none";
        closeButton.style.display = "none";
      }

      // Update the last stable scroll position
      lastScrollY = currentScroll;
    }, 100); // Debounce interval: 100ms
  });


  // Attach an event listener to the window resize event
let resizeTimeout; // To prevent excessive reloads during resizing
window.addEventListener("resize", () => {

    console.log("Window resized. Reloading the page...");
    const scrollPosition = window.scrollY; // Get current scroll position
    localStorage.setItem("scrollPosition", scrollPosition); // Save to localStorage

    location.reload();
});

  

  // --- Dragging logic for the PiP window ---
  dragButton.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    initialX = pipContainer.offsetLeft;
    initialY = pipContainer.offsetTop;
    pipContainer.style.transition = "none"; // Disable transitions during dragging
    dragButton.style.cursor = "grabbing";
    document.body.style.userSelect = "none"; // Disable text selection
    e.preventDefault();
  });

  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      pipContainer.style.left = `${initialX + deltaX}px`;
      pipContainer.style.top = `${initialY + deltaY}px`;
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
        pipContainer.style.width = `${startWidth + deltaX}px`;
        pipContainer.style.height = `${startHeight + deltaY}px`;
      }

      // Prevent the container from collapsing below minimum size
      const newWidth = Math.max(400, parseInt(pipContainer.style.width));
      const newHeight = Math.max(2000, parseInt(pipContainer.style.height));
      pipContainer.style.width = `${newWidth}px`;
      pipContainer.style.height = `${newHeight}px`;
    }
  });



  document.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      pipContainer.style.transition = "all 0.3s ease";
      dragButton.style.cursor = "grab";
      document.body.style.userSelect = ""; // Re-enable text selection
    }if (isResizing) {
      isResizing = false;
      currentHandle.style.cursor = ""; // Reset cursor
      console.log("Resizing complete. Final dimensions:", {
        width: pipContainer.offsetWidth,
        height: pipContainer.offsetHeight,
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
      startWidth = pipContainer.offsetWidth;
      startHeight = pipContainer.offsetHeight;
      initialX = pipContainer.offsetLeft;
      initialY = pipContainer.offsetTop;
      handle.style.cursor = "nwse-resize";
      pipContainer.style.transition = "none"; // Disable transitions during resize
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
      pipContainer.style.width = `${newWidth}px`;
      pipContainer.style.height = `${newHeight}px`;

      // Debugging: Log the new dimensions
      console.log("Resizing to:", { width: newWidth, height: newHeight });
    }
  });

  document.addEventListener("mouseup", () => {
    if (isResizing) {
      isResizing = false;
      pipContainer.style.transition = "all 0.3s ease";
      console.log("Resizing complete. Final dimensions:", {
        width: pipContainer.offsetWidth,
        height: pipContainer.offsetHeight,
      });
    }
  });

  // --- Close button functionality ---
  closeButton.addEventListener("click", () => {
    pipContainer.style.display = "none";
    closeButton.style.display = "none";
    dragButton.style.display = "none";
    resetPiPPosition(); // Reset position when closed
    mapContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  // --- Helper function to reset PiP position ---
  function resetPiPPosition() {
    pipContainer.style.left = ""; // Reset left position
    pipContainer.style.top = ""; // Reset top position
    pipContainer.style.width = ""; // Reset width
    pipContainer.style.height = ""; // Reset height
    pipContainer.style.display = "block"; // Ensure the map remains visible
    console.log("PiP position and size reset.");
  }

  // --- DEBUGGING LOGS ---
  console.log("Resize handles detected:", resizeHandles);
  console.log("Initial PiP dimensions:", {
    width: pipContainer.offsetWidth,
    height: pipContainer.offsetHeight,
  });
});
