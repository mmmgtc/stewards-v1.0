function search_stewards() {
  let input = document.getElementById("search").value;
  input = input.toLowerCase();
  let stewards = document.getElementsByClassName("card");

  for (i = 0; i < stewards.length; i++) {
    const name =
      stewards[i].getElementsByClassName("name truncate")[0].innerHTML;

    const address =
      stewards[i].getElementsByClassName("steward_address")[0].innerHTML;

    const workStream =
      stewards[i].getElementsByClassName("workstream_name")[0].innerHTML;

    const searchParams = [name, address, workStream].join(" ").toLowerCase();

    if (!searchParams.includes(input)) {
      stewards[i].style.display = "none";
    } else {
      stewards[i].style.display = "list-item";
    }
  }
}
