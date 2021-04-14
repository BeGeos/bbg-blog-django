const baseUrl = "http://localhost:8000/_api/";

const showMobileNavbar = () => {
  const mobileNavbar = document.querySelector(".navbar__mobile");
  mobileNavbar.classList.toggle("open");
};

const hamburger = document.querySelector(".hamburger");
if (hamburger) {
  hamburger.addEventListener("click", showMobileNavbar);
}

const showShareIcons = () => {
  const socialWindow = document.querySelector(".social__window");
  socialWindow.classList.toggle("hidden");
};

const switchOff = () => {
  let message = document.querySelector(".message");
  message.classList.add("switch-off");
};

const showCancelOptions = (slug) => {
  let options = document.querySelector(".cancel__action");
  let link = document.querySelector(".yes-button");
  options.style.display = "flex";
  link.href = `delete/${slug}`;
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

// Check if email field is valid function return true or false
const emailCheck = (email) => {
  // not empty nor invalid address
  return /\S+@\S+.\S+/gi.test(email);
};

// Subscibe API call from main page and single page
const subscribe = async () => {
  let newsletterForm = document.querySelector(".newsletter__form");
  let address = document.querySelector(".newsletter__form input");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let output = document.querySelector(".ajax-response");
  let url = baseUrl + "newsletter/subscribe";

  if (!emailCheck(address.value)) {
    output.innerHTML = "<small>Address is not valid</small>";
    return;
  }

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      email: address.value,
    }),
  });

  const response = await request.json();

  if (request.status == 200) {
    newsletterForm.innerHTML =
      "<h3>Thank you for your subscription</h3> <p>I am happy to have you on board!</p>";
    // window.location.href("http://localhost:8000")
  } else {
    output.innerHTML = `<small>${response.message}</small>`;
  }
};

const singleSubscribe = async () => {
  let newsletterForm = document.querySelector(".newsletter");
  let address = document.querySelector(".subscription__form input");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let output = document.querySelector(".ajax-response");
  let url = baseUrl + "newsletter/subscribe";

  // console.log(emailCheck(address.value));
  if (!emailCheck(address.value)) {
    output.innerHTML = "<small>Address is not valid</small>";
    return;
  }

  // Spinning loading thing

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      email: address.value,
    }),
  });

  const response = await request.json();

  if (request.status == 200) {
    newsletterForm.innerHTML =
      "<h3>Newsletter</h3>" +
      "<h4 style='text-align: center; margin-top: 3rem'>Thank you for your subscription</h4>" +
      "<p style='text-align: center; margin-top: 2rem'>I am happy to have you on board!</p>";
    // window.location.href("http://localhost:8000")
  } else {
    output.innerHTML = `<small>${response.message}</small>`;
  }
};

// Add likes to post or news
const addPostLike = async (slug) => {
  let likeNum = document.querySelector(".likes");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let url = baseUrl + "post/like/" + slug;

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  const response = await request.json();
  if (request.status == 200) {
    likeNum.textContent = "Likes: " + response.likes;
  } else {
    console.log(response.message);
  }
};

const addNewsLike = async (slug) => {
  let likeNum = document.querySelector(".likes");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let url = baseUrl + "news/like/" + slug;

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  const response = await request.json();
  if (request.status == 200) {
    likeNum.textContent = "Likes: " + response.likes;
  } else {
    console.log(response.message);
  }
};

// Add views to posts and news
const addPostViews = async (slug) => {
  // let views = document.querySelector(".views");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let url = baseUrl + "post/views/" + slug;

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  });

  const response = await request.json();
  console.log(response.message);
};

const addNewsViews = async (slug) => {
  // let views = document.querySelector(".views");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let url = baseUrl + "news/views/" + slug;

  const request = await fetch(url, {
    method: "POST",
    mode: "same-origin",
    headers: {
      "X-CSRFToken": csrfToken,
    },
  });

  const response = await request.json();
  console.log(response.message);
};
