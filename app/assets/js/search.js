let searchParams = new URLSearchParams(window.location.search);
let search = searchParams.toString().split("=")[1];
const searchInput = document.getElementById("search");

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
  let stewards = document.getElementsByClassName("card");

  for (i = 0; i < stewards.length; i++) {
    const name =
      stewards[i].getElementsByClassName("name truncate")[0].innerHTML;

    const address =
      stewards[i].getElementsByClassName("steward_address")[0].innerHTML;

    const workStream =
      stewards[i].getElementsByClassName("workstream_name")[0].innerHTML;

    const searchParams = [name, address, workStream].join(" ").toLowerCase();

    if (!searchParams.includes(value)) {
      stewards[i].style.display = "none";
    } else {
      stewards[i].style.display = "list-item";
    }
  }
}

// function orderStewards() {
//   orderby = document.getElementById("orderby").value;
//   direction = document.getElementById("direction").value;
//   // console.log(orderby, direction)

//   if (orderby == "health") {
//     window.stewards.sort((a, b) => (a.health < b.health ? 1 : -1));
//   }

//   if (orderby == "weight") {
//     window.stewards.sort((a, b) => (a.votingweight < b.votingweight ? 1 : -1));
//   }

//   if (orderby == "participation") {
//     window.stewards.sort((a, b) =>
//       a.participation_snapshot < b.participation_snapshot ? 1 : -1
//     );
//   }

//   if (orderby == "posts") {
//     window.stewards.sort((a, b) => (a.posts < b.posts ? 1 : -1));
//   }

//   // ascending - from low to high
//   if (direction == "ascending") {
//     window.stewards.reverse();
//   }
// }
