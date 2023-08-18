let lastClickedButtonCountry = "";


function filterCountries() {
  // Get input value from the search bar
  const input = document.getElementById("searchBar").value.toLowerCase();

  // Get the list of all countries
  const countries = document.querySelectorAll("#countryList li");

  // Loop through each country in the list
  countries.forEach((country) => {
    const countryName = country.textContent.toLowerCase();

    // If the country name contains the input value, display it, otherwise hide it
    if (countryName.includes(input)) {
      country.style.display = "block";
    } else {
      country.style.display = "none";
    }
  });
}

function displayTeams(button) {
  const leagueName = button.textContent;

  fetch("/query_teams", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      leagueName: leagueName,
      lastClickedButtonCountry: lastClickedButtonCountry,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      //starts here
      replaceButtons();
      addNewButtonsClubs(data);
    });
}

function showCountryName(button) {
  const countryName = button.textContent;
  lastClickedButtonCountry = countryName;
  fetch("/query_country", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ countryName: countryName }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the server if needed
      data.forEach((comp) => {
        console.log(
          "Comp Name: " + comp.comp_name + "\nFlag URL: " + comp.logo_url
        );
      });
      replaceButtons();
      addNewButtonsLeague(data);
    })
    .catch((error) => {
      // Handle any errors that occurred during the request
      console.error("Error:", error);
    });
}

// Used to remove all the buttons in the countryList button area
function replaceButtons() {
  const countryList = document.getElementById("countryList");

  // Remove existing buttons
  while (countryList.firstChild) {
    countryList.removeChild(countryList.firstChild);
  }
}

// Function to add new buttons when clicking a button outside the div
function addNewButtonsLeague(leagues) {
  const countryList = document.getElementById("countryList");

  leagues.forEach((league) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.textContent = league.comp_name;
    button.onclick = function () {
      displayTeams(this);
    };
    const image = document.createElement("img");
    const imageUrl = league.logo_url;
    image.src = imageUrl;
    image.style.width = "50px";
    image.style.height = "50px";
    image.style.marginRight = "10px";

    li.appendChild(button);
    button.appendChild(image);
    countryList.appendChild(li);
  });

  // Update the filtered display with the new buttons
  filterCountries();
}

function addNewButtonsClubs(clubs) {
  const countryList = document.getElementById("countryList");

  clubs.forEach((club) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.textContent = club.team_name;
    button.onclick = function () {
      StoreSelectedTeam(this);
    };
    const image = document.createElement("img");
    const imageUrl = club.team_badge;
    image.src = imageUrl;
    image.style.width = "50px";
    image.style.height = "50px";
    image.style.marginRight = "10px";

    li.appendChild(button);
    button.appendChild(image);
    countryList.appendChild(li);
  });
  filterCountries();
}
function StoreSelectedTeam(team) {
  const teamName = team.textContent;

  fetch("/store_favteam", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ teamName: teamName }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the server if needed
      redirectToHome();
    });
}
// Store the original state for undo
let originalState;
originalState = countryList.innerHTML;
