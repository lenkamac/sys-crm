// Automatically hide alert messages after 3 seconds (3000 milliseconds)
document.addEventListener('DOMContentLoaded', function() {
setTimeout(function() {
  document.querySelectorAll('.alert').forEach(function(alert) {
    // Fade out for a smooth effect (optional)
    alert.style.transition = "opacity 0.5s linear";
    alert.style.opacity = 0;
    setTimeout(function() { alert.remove(); }, 500); // remove from DOM after fade out
  });
}, 3000); // Show message for 3 seconds
});
