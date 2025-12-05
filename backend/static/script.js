// DOM elements
const loginBtn = document.getElementById("login-btn");
const loginSection = document.getElementById("login-section");
const tracksSection = document.getElementById("tracks-section");
const trackList = document.getElementById("track-list");
const subtitle = document.getElementById("subtitle");

// Redirect to login
loginBtn.onclick = () => {
  window.location.href = "/login";
};

// Load tracks from backend
async function loadTracks() {
  try {
    const res = await fetch("/tracks/sql");
    const data = await res.json();

    if (!data || data.length === 0 || data.error) {
      return; // Not logged in or empty DB
    }

    // Hide login, show tracks
    loginSection.style.display = "none";
    tracksSection.style.display = "block";
    subtitle.textContent = "Your Top 20 Songs This Week";

    trackList.innerHTML = "";

    data.forEach(track => {
      const li = document.createElement("li");
      li.className = "track-card";

      li.innerHTML = `
        <div class="track-info">
          <h3>${track.name}</h3>
          <p><strong>Artist:</strong> ${track.artist}</p>
          <p><strong>Album:</strong> ${track.album}</p>
          <p><strong>Release:</strong> ${track.release_date}</p>
        </div>
        <div class="track-meta">
          <p><strong>Popularity:</strong> ${track.popularity}</p>
          <p><strong>Duration:</strong> ${(track.duration_ms / 60000).toFixed(2)} min</p>
        </div>
      `;
      trackList.appendChild(li);
    });

  } catch (err) {
    console.error("Error loading tracks:", err);
  }
}

// Run on page load
loadTracks();
