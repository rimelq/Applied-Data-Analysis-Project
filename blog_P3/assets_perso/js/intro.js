document.addEventListener("DOMContentLoaded", () => {
    const title = "From Script to Reality: Does Cinema Mirror Life or Rewrite it?";
    const firstPart = title.split(":")[0] + ":"; // Text before and including the colon
    const secondPart = title.split(":")[1]?.trim() || ""; // Text after the colon
    const line1 = document.querySelector("#typewriter-title .line1");
    const line2 = document.querySelector("#typewriter-title .line2");
    let index2 = 0;
  
    // Display first line immediately without animation
    line1.textContent = firstPart;

    // Only animate the second line
    function typeLine2() {
      if (index2 < secondPart.length) {
        line2.textContent += secondPart[index2];
        index2++;
        setTimeout(typeLine2, 70); 
      }
    }
  
    // Start the typing effect for second line
    setTimeout(typeLine2, 150); 
  
    // Listen for scroll events
    document.addEventListener("scroll", () => {
      const scrollPosition = window.scrollY;
      const transitionHeight = window.innerHeight * 0.15; 

      // Add or remove the 'scrolled' class based on scroll position
      if (scrollPosition > transitionHeight) {
        document.body.classList.add("scrolled");
      } else {
        document.body.classList.remove("scrolled");
      }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth'
          });
        }
      });
    });

  });
  