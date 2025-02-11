// Get the button:
let mybutton = document.getElementById("backToTop");

// When the user scrolls down 1500px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 1500 || document.documentElement.scrollTop > 1500) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 


// Hide video on main page
document.addEventListener("DOMContentLoaded", function() {
  const startVideoElement = document.getElementById('start_video');
  if (startVideoElement) {
    const videoId = startVideoElement.getAttribute('video_id');
    const startVidValue = localStorage.getItem(videoId);
      
      if (parseInt(startVidValue) > 1125) { 
          if (startVideoElement) {
              startVideoElement.remove();
          }
      }
}})

// category search
const searchInput = document.getElementById('search-input');
if (searchInput) {
  const categoryButtons = document.querySelectorAll('.category-button');

  searchInput.addEventListener('input', function() {
    const filter = searchInput.value.toLowerCase();

    categoryButtons.forEach(function(button) {
      const categoryText = button.textContent.toLowerCase();
      if (categoryText.includes(filter)) {
        button.style.display = "";
      } else {
        button.style.display = "none";
      }
    });
  })
};