const passNetworkButton = document.getElementById("passnetworkBtn");
const passmapButton = document.getElementById("passmapBtn");
const heatmapButton = document.getElementById("heatmapBtn");
const individualButton = document.getElementById("individualButton");
const teamOptionButton = document.getElementById("teamOptionButton");
const teamButton = document.getElementById("teamButton");
const playerDropdown = document.getElementById("playerDropdown");
const confirmButton = document.getElementById("confirmbtn");
const playerDropdowndiv = document.getElementById('playerDropdowndiv');
const imageElement = document.getElementById('imagemodels');
let currentState = "Team1";
let activeButton = null;
let selectedGlobalVariable = null;

teamButton.addEventListener("click", () => {
  if (currentState === team1) {
    teamButton.textContent = team2;
    currentState = team2;
    playerDropdown.innerHTML = '';
    for (var i = 0; i < awayplayers.length; i++){
      var option = document.createElement('option');
      option.value = awayplayers[i];
      option.text = awayplayers[i];
      playerDropdown.appendChild(option)
    }
  } else {
    teamButton.textContent = team1;
    currentState = team1;
    playerDropdown.innerHTML = '';
    for (var i = 0; i < homeplayers.length; i++){
      var option = document.createElement('option');
      option.value = homeplayers[i];
      option.text = homeplayers[i];
      playerDropdown.appendChild(option)
    }
  }
});

function setActiveButton(buttonName) {
  if (activeButton) {
    activeButton.style.background = "#0E1117"; // Reset background color of previous active button
  }

  // Find the button by its name
  const buttonId = buttonName.replace(/\s+/g, "").toLowerCase() + "Btn";
  const button = document.getElementById(buttonId);

  button.style.background = "#FF5733"; // Highlight current active button
  activeButton = button;
  selectedGlobalVariable = buttonName;
}





passmapButton.addEventListener("click", () => {
  hideElements(
    teamButton,
    teamOptionButton,
    individualButton,
    playerDropdowndiv,
    confirmButton
  );
  toggleVisibility(individualButton);
  toggleVisibility(teamButton);
  toggleVisibility(teamOptionButton);
});
function toggleVisibility(element) {
  element.classList.toggle("d-none");
}

function hideElements(...elements) {
  elements.forEach((element) => {
    element.classList.add("d-none");
  });
}
passNetworkButton.addEventListener("click", () => {
  hideElements(
    teamButton,
    teamOptionButton,
    individualButton,
    playerDropdowndiv,
    confirmButton
  );
  toggleVisibility(teamButton);
  toggleVisibility(confirmButton);

});
heatmapButton.addEventListener("click", () => {
  hideElements(
    teamButton,
    teamOptionButton,
    individualButton,
    playerDropdowndiv,
    confirmButton
  );
  toggleVisibility(individualButton);
  toggleVisibility(teamButton);
});
teamOptionButton.addEventListener("click", () => {
  hideElements(confirmButton,playerDropdowndiv);
  team =teamButton.textContent;
  console.log(team);
  if (selectedGlobalVariable == 'Passmap'){
    fetch('/get_passmapteam', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ team:team })
  })
  .then(response => response.json())
  .then(data => {
      hideElements(imageElement);
      imageElement.src = 'data:image/jpeg;base64,' + data.image_data;
      toggleVisibility(imageElement);
  })
  .catch(error => console.error('Error fetching image:', error));
  }
});
individualButton.addEventListener("click",()=> {
  hideElements(playerDropdowndiv,confirmButton);
  toggleVisibility(playerDropdowndiv);
  toggleVisibility(confirmButton);
});

confirmButton.addEventListener("click",()=>{
  const player = playerDropdown.value;
  if (selectedGlobalVariable == 'Passmap'){
    fetch('/get_passmapplayer', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ player:player })  
  })
  .then(response => response.json())
  .then(data => {
      hideElements(imageElement);
      imageElement.src = 'data:image/jpeg;base64,' + data.image_data;
      toggleVisibility(imageElement);
  })
  .catch(error => console.error('Error fetching image:', error));
  } else if (selectedGlobalVariable == 'PassNetwork'){
    team =teamButton.textContent;
    fetch('/get_passnetwork', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ team:team })  
  })
  .then(response => response.json())
  .then(data => {
      hideElements(imageElement);
      imageElement.src = 'data:image/jpeg;base64,' + data.image_data;
      toggleVisibility(imageElement);
  })
  .catch(error => console.error('Error fetching image:', error));

  } else if (selectedGlobalVariable == 'Heatmap'){
    const player = playerDropdown.value;
    fetch('/get_heatmap', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ player:player })  
    })
    .then(response => response.json())
    .then(data => {
        hideElements(imageElement);
        imageElement.src = 'data:image/jpeg;base64,' + data.image_data;
        toggleVisibility(imageElement);
    })
    .catch(error => console.error('Error fetching image:', error));

    }
});
