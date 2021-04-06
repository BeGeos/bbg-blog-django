const hamburger = document.querySelector(".hamburger");
const mobileNavbar = document.querySelector(".navbar__mobile");

hamburger.addEventListener("click", () => {
  mobileNavbar.classList.toggle("open");
});

const showShareIcons = () => {
  const socialWindow = document.querySelector(".social__window");
  socialWindow.classList.toggle("hidden");
};

const switchOff = () => {
  let message = document.querySelector(".message");
  message.classList.add("switch-off");
};

const showCancelOptions = () => {
  let options = document.querySelector(".cancel__action");
  options.style.display = "flex";
};

const cancelNoOption = () => {
  let options = document.querySelector(".cancel__action");
  options.style.display = "none";
};

const cancelYesOption = (slug) => {
  let options = document.querySelector(".cancel__action");
  options.style.display = "none";

  // console.log(slug);
};
