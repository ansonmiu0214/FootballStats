function splitCompanyName(nameAndYear) {
  var compName = nameAndYear.textContent.split("-")[0].trim();
  var compYear = nameAndYear.textContent.split("-")[1].trim();
  console.log(compName);
  console.log(compYear);
  fetch("/get_comp_id&seasonid", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ compName: compName, compYear: compYear }),
  })
    .then((response) => response.json())
    .then((data) => {
      compId = data[0].compId;
      seasonId = data[0].seasonId;
      displayMatches(compId, seasonId);
    });
}

function displayMatches(compId, seasonId) {
  fetch("/get_selected_comp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ compId: compId, seasonId: seasonId }),
  })
    .then((response) => response.json())
    .then((data) => {
      const ButtonLayout =
        document.getElementsByClassName("container-buttons")[0];
      ButtonLayout.innerHTML = "";
      ButtonLayout.innerHTML = `
        <div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    <div class="scrollable-table">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Match Date</th>
                                    <th>Competition</th>
                                    <th>Season</th>
                                    <th>Home Team</th>
                                    <th>Away Team</th>
                                    <th>Home Score</th>
                                    <th>Away Score</th>
                                    <th>Match Data</th>
                                </tr>
                            </thead>
                            <tbody>
                              
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        `;

      const tableBody = document.querySelector("tbody");
      data.forEach((match) => {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${match.match_date}</td>
            <td>${match.competition}</td>
            <td>${match.season}</td>
            <td>${match.home_team}</td>
            <td>${match.away_team}</td>
            <td>${match.home_score}</td>
            <td>${match.away_score}</td>
            <td>
              <button class="view-match-button" data-match='${JSON.stringify(
                match
              )}'>View Match</button>
            </td>
              `;
        tableBody.appendChild(newRow);
      });

      const viewButtons = document.querySelectorAll(".view-match-button");
      viewButtons.forEach((button) => {
        button.addEventListener("click", () => {
          const matchData = JSON.parse(button.getAttribute("data-match"));
          console.log(matchData);
          match_home_team = matchData.home_team;
          match_away_team = matchData.away_team;
          match_home_score = matchData.home_score;
          match_away_score = matchData.away_score;
          match_id = matchData.match_id;
          fetch("/get_match_stats", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ match_id: match_id, match_home_team : match_home_team,match_away_team:match_away_team,match_home_score:match_home_score,match_away_score:match_away_score }),
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data);
              redirectToStats();
            });
        });
      });
    });
}
