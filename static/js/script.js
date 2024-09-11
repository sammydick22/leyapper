const fileInput = document.getElementById("file-upload");
const fileChosenSpan = document.getElementById("file-chosen");

fileInput.addEventListener("change", function() {
  const fileName = fileInput.files[0].name;
  fileChosenSpan.textContent = fileName;
});

async function handleInput() {
    const fileInput = document.getElementById("file-upload").files[0];
    const formData = new FormData();
      const analysisResultDiv = document.getElementById("analysis-result");
    const speakerScoresContainer = document.getElementById("speaker-scores-container");

  // Add file input to formData
  if (fileInput) {
    formData.append("file", fileInput);
  }

  // Display a loading animation
  analysisResultDiv.innerHTML = `
    <div class="loading-animation">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
            </div>
    `;
  speakerScoresContainer.innerHTML = "";

  // Send the data to the Flask backend
  try {
    const response = await fetch("http://127.0.0.1:5001/get_lebroniest", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log("Result:", result);

    const lebroniestSpeaker = result.lebroniest_speaker;
    const scores = result.scores;

    // Normalize the scores
    const minScore = 0.12;
    const maxScore = 0.3;
    const normalizedScores = {};
    for (const speaker in scores) {
      const rawScore = scores[speaker];
      const normalizedScore = (rawScore - minScore) / (maxScore - minScore);
      normalizedScores[speaker] = Math.max(0, Math.min(1, normalizedScore)); // Clamp the score to [0, 1]
    }

    // Update the HTML elements with the result
    analysisResultDiv.innerHTML = `
      <h2>Lebroniest Speaker: ${lebroniestSpeaker}</h2>
    `;

    speakerScoresContainer.innerHTML = `
      ${Object.keys(normalizedScores).map((speaker, index) => `
        <div class="speaker-score">
          <div class="score-bar-container">
            <div class="score-bar" style="width: ${normalizedScores[speaker] * 100}%;">
              <span class="speaker-letter">${String.fromCharCode(65 + index)}</span>
              <span class="score">${normalizedScores[speaker].toFixed(2)}</span>
            </div>
          </div>
        </div>
      `).join('')}
    `;
  } catch (error) {
    console.error("Error:", error);
    analysisResultDiv.innerHTML = `
      <p>Error: ${error.message}</p>
    `;
  }
}
