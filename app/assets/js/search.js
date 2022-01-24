let searchParams = new URLSearchParams(window.location.search);
let search = searchParams.toString().split("=")[1];
const searchInput = document.getElementById("search");

const orderBy = document.getElementById("order_by");
const direction = document.getElementById("direction");

let stewards = document.getElementsByClassName("card");

if (!!search) {
  searchInput.value = search;
  filterStewards(search);
}

searchInput.addEventListener("keyup", function (event) {
  const search = event.target.value.toLowerCase();

  searchParams.set("search", search);

  if (window.history.replaceState) {
    const url =
      window.location.protocol +
      "//" +
      window.location.host +
      window.location.pathname +
      "?" +
      searchParams.toString();

    window.history.replaceState(
      {
        path: url,
      },
      "",
      url
    );

    filterStewards(search);
  }
});

function filterStewards(value) {
  for (i = 0; i < stewards.length; i++) {
    const name = getInnerHtml(stewards[i], "name truncate");

    const address = getInnerHtml(stewards[i], "steward_address");

    const workStream = getInnerHtml(stewards[i], "workstream_name");

    const searchParams = [name, address, workStream].join(" ").toLowerCase();

    if (!searchParams.includes(value)) {
      stewards[i].style.display = "none";
    } else {
      stewards[i].style.display = "list-item";
    }
  }
}

orderBy.addEventListener("change", function (event) {
  const type = event.target.value;

  let stewardsArray = nodeListToArray(stewards);
  let sortedStewardsArray = [];

  if (type === "name") {
    sortedStewardsArray = sortArray(stewardsArray, "name truncate");
  }

  if (type === "date") {
    sortedStewardsArray = sortArray(stewardsArray, "steward_since");
  }

  if (type == "posts") {
    sortedStewardsArray = sortArray(stewardsArray, "forum_post");
  }

  if (type == "participation") {
    sortedStewardsArray = sortArray(stewardsArray, "participation percentage");
  }

  if (type == "weight") {
    sortedStewardsArray = sortArray(stewardsArray, "weight percentage");
  }

  if (type == "health") {
    sortedStewardsArray = sortArray(stewardsArray, "health_score");
  }

  stewards = joinArryToHtml(sortedStewardsArray);
});

direction.addEventListener("change", function (event) {
  const order = event.target.value;

  let stewardsArray = nodeListToArray(stewards);
  let sortedStewardsArray = [];

  if (order == "descending") {
    stewardsArray.reverse();
  }

  return joinArryToHtml(sortedStewardsArray);
});

function nodeListToArray(nodes) {
  return [].slice.call(nodes);
}

function joinArryToHtml(array) {
  let html = "";

  array.forEach((element) => {
    html += element;
  });

  return html;
}

function getInnerHtml(element, className) {
  return element.getElementsByClassName(className)[0].innerHTML;
}

function sortArray(array, key) {
  return array.sort((a, b) => {
    return getInnerHtml(a, key) < getInnerHtml(b, key) ? 1 : -1;
  });
}
