const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {

  let currentScroll = window.scrollY;

  if(currentScroll > 50){
    navbar.classList.add("nav-effect");
    navbar.classList.add("nav-small");
  }else{
    navbar.classList.remove("nav-effect");
    navbar.classList.remove("nav-small");
  }

});