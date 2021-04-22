const baseUrl = "http://localhost:8000/_api/";
const sourceUrl = "http://localhost:8000/";
const staticUrl = "http://localhost:8000/staticfiles/";

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
  return /\S+@\S+\.\S+/i.test(email);
};

// Subscribe API call from main page and single page
const subscribe = async () => {
  let newsletterForm = document.querySelector(".newsletter__form");
  let address = document.querySelector(".newsletter__form input");
  let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let output = document.querySelector(".sub-response");
  let url = baseUrl + "newsletter/subscribe";

  if (!emailCheck(address.value)) {
    output.textContent = "*Address is not valid";
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
      "<h3 style='text-align: center'>Thank you for your subscription</h3>" +
      "<p style='text-align: center'>I am happy to have you on board!</p>" +
      `<div style="text-align: center"><img src='${staticUrl}images/check-green.svg' alt="check-mark" height="55px"></div>`;
    // window.location.href("http://localhost:8000")
  } else {
    output.textContent = `*${response.message}`;
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
    output.textContent = "*Address is not valid";
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
      "<h4 style='text-align: center; margin: 1rem 0'>Thank you for your subscription</h4>" +
      "<p style='text-align: center; margin-bottom: 1rem'>I am happy to have you on board!</p>" +
      `<div style="text-align: center"><img src='${staticUrl}images/check-green.svg' alt="check-mark" height="55px"></div>`;
    // window.location.href("http://localhost:8000")
  } else {
    output.textContent = `*${response.message}`;
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

// Add posts and news calls to API for most recent, viewed or liked
const getAllPosts = async (order, isSuper) => {
  let queryURL = baseUrl + "posts/all?order=" + order;
  let data = await fetch(queryURL, { method: "GET" });
  let postDiv = document.querySelector(".all-posts");

  let response = await data.json();

  let allCards = "";

  for (let post of response.data) {
    // let post = response.data[i];
    let postTags = "";

    // Create the Tags li
    for (let k = 0; k < post.tags.lenght; k++) {
      postTags += `<li>${post.tags[i]}</li>`;
    }

    let updateActions = "";

    // Create the user Update and Delete functions
    if (isSuper == "True") {
      updateActions += `<div class="post__actions">
      <a href="${sourceUrl}blog/update-post/${post.slug}">Update</a>
      <a onclick="showCancelOptions('${post.slug}')">Delete</a>
    </div>`;
    }

    let postCard = `<div class="single-post wide">
    <div class="post__img">
      <img src="${staticUrl}images/default.jpg" />
    </div>
    <div class="post__text">
      <h3>
        <a href="${sourceUrl}blog/post/${post.slug}">${post.title}</a>
      </h3>
      <p>${post.summary}</p>
      <div id="single-tag">
        <ul>
          ${postTags}
        </ul>
      </div>
      ${updateActions}
    </div>
    <div class="post__stats">
      <small
        >${post["created_on"]} <br />
        by ${post.author}</small
      >
      <div class="post__likes">
        <img src="${staticUrl}images/heart-fill.svg" />
        <p>${post.likes}</p>
        <img src="${staticUrl}images/eye.svg" alt="views" />
        <p>${post.views}</p>
      </div>
    </div>
  </div>`;

    allCards += postCard;
  }

  postDiv.innerHTML = allCards;
  // console.log("done!");
};
