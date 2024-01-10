const ws = new WebSocket("ws://localhost:8080"); //Depends if docker or localhost
console.log("WebSocket client running");

clientId = null;

ws.onopen = function () {
  console.log("Connected to WebSocket server");
  ws.send(JSON.stringify({ type: "register" })); // Register this player with the server
};

ws.onmessage = function (event) {
  console.log("Received message from server:", event.data);
  const json = JSON.parse(event.data);

  if (json.type === "clientId") {
    console.log("Client registered with ID:", json.clientId);

    const clientIdElement = document.getElementById("clientId");
    clientId = json.clientId;
    clientIdElement.innerText = `Your unique ID: ${json.clientId}`;
  } else if (json.type === "round") {
    console.log("Round changed");

    const roundNumberElement = document.getElementById("roundCounter");
    roundNumberElement.innerText = `Round: ${json.number}`;
  } else if (json.type == "result_score") {
    console.log("Received results:", json.results);
    const resultsContainer = document.getElementById("clientsScore");
    resultsContainer.innerHTML = "";
    //you should be on top
    Object.keys(json.results).forEach((key) => {
      const p = document.createElement("p");
      if (key == clientId) {
        p.innerText = `You: ${json.results[key]}`;
      } else {
        p.innerText = `Player ${key}: ${json.results[key]}`;
      }

      resultsContainer.appendChild(p);
    });
    ws.send(JSON.stringify({ type: "new_question" }));
  } else if (json.type == "result_each") {
  } else if (json.type === "question") {
    console.log("Received new question:", json.data.question);

    document.getElementById("questionText").innerText = json.data.question;
    document.getElementById("result").innerText = "";

    const choicesContainer = document.getElementById("choices");
    choicesContainer.innerHTML = "";

    json.data.answers.forEach((choice) => {
      const button = document.createElement("button");
      button.textContent = choice;
      button.addEventListener("click", function () {
        ws.send(JSON.stringify({ type: "answer", answer: choice }));
        console.log("Answer sent to server:", choice);
        const choiceButtons = document.querySelectorAll("#choices button");
        choiceButtons.forEach((btn) => {
          btn.disabled = true;
        });
      });
      choicesContainer.appendChild(button);
    });
  } else if (json.type === "response") {
    document.getElementById("result").innerText = json.response;
    // Attendre une question pendant 10 secondes
    setTimeout(() => {
      document.getElementById("questionText").innerText =
        "Waiting for the next question...";
      document.getElementById("result").innerText = "";
    }, 10000);
  } else if (json.type === "player_count") {
    document.getElementById(
      "playerCount"
    ).innerText = `Connected: ${json.count}`;
    if (json.count < 2) {
      document.getElementById("questionContainer").style.display = "none";
      document.getElementById("playerStatus").innerText =
        "Waiting for another player to join...";
    } else {
      document.getElementById("questionContainer").style.display = "block";
      document.getElementById("playerStatus").innerText = "";
    }
  }
};

ws.onclose = function () {
  console.log("WebSocket connection closed");
};
