// DOM elements
const loginBtn = document.getElementById("login-btn");
const loginSection = document.getElementById("login-section");
const tracksSection = document.getElementById("tracks-section");
const trackList = document.getElementById("track-list");

// Redirect user to Spotify OAuth login
loginBtn.onclick = () => {
    window.location.href = "/login";
};

// Load tracks from backend
async function loadTracks() {
    try {
        const res = await fetch("/tracks/sql");
        const data = await res.json();

        if (!data || data.length === 0) return;

        // Hide login, show tracks
        loginSection.style.display = "none";
        tracksSection.style.display = "block";

        trackList.innerHTML = "";

        data.forEach(track => {
            const card = document.createElement("div");
            card.className = "track-card";

            card.innerHTML = `
                <div class="track-left">
                    <h3>${track.name}</h3>
                    <p class="artist">${track.artist}</p>
                    <p class="album">${track.album}</p>
                </div>

                <div class="track-right">
                    <p><strong>Popularity:</strong> ${track.popularity}</p>
                    <p><strong>Duration:</strong> ${(track.duration_ms / 60000).toFixed(2)} min</p>
                    <p><strong>Release:</strong> ${track.release_date}</p>
                </div>
            `;

            trackList.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading tracks:", error);
    }
}

// Try loading tracks on page load
loadTracks();