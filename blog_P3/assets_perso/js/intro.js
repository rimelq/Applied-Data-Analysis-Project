document.addEventListener("DOMContentLoaded", () => {
    const title = "The Reel World vs. The Real World: Is Cinema Holding a True Mirror to Society?";
    const firstPart = title.split(":")[0] + ":"; // Text before and including the colon
    const secondPart = title.split(":")[1]?.trim() || ""; // Text after the colon
    const line1 = document.querySelector("#typewriter-title .line1");
    const line2 = document.querySelector("#typewriter-title .line2");
    let index1 = 0;
    let index2 = 0;
  
    function typeLine1() {
      if (index1 < firstPart.length) {
        line1.textContent += firstPart[index1];
        index1++;
        setTimeout(typeLine1, 85); // Adjust speed if needed
      } else {
        setTimeout(typeLine2, 200); // Small delay before starting second line
      }
    }
  
    function typeLine2() {
      if (index2 < secondPart.length) {
        line2.textContent += secondPart[index2];
        index2++;
        setTimeout(typeLine2, 85); // Adjust speed if needed
      }
    }
  
    typeLine1(); // Start the typing effect

    // Listen for scroll events
    document.addEventListener("scroll", () => {
      const scrollPosition = window.scrollY;
      const transitionHeight = window.innerHeight * 0.15; // Start fading at 15% of the viewport height

      // Add or remove the 'scrolled' class based on scroll position
      if (scrollPosition > transitionHeight) {
        document.body.classList.add("scrolled");
      } else {
        document.body.classList.remove("scrolled");
      }
    });
  });
  