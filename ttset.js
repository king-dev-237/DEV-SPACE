// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor=>{
  anchor.addEventListener("click",function(e){
    e.preventDefault();
    document.querySelector(this.getAttribute("href"))
      .scrollIntoView({behavior:"smooth"});
  });
});

// Fake submit demo
document.getElementById("contactForm")
.addEventListener("submit", function(e){
  e.preventDefault();
  alert("Message submitted successfully!");
});