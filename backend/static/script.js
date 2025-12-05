li.innerHTML = `
  <div class="track-info">
    <h3>${track.name}</h3>
    <p><strong>ID:</strong> ${track.id}</p>
    <p><strong>Artist:</strong> ${track.artist}</p>
    <p><strong>Album:</strong> ${track.album}</p>
    <p><strong>Release:</strong> ${track.release_date}</p>
  </div>
  <div class="track-meta">
    <p><strong>Popularity:</strong> ${track.popularity}</p>
    <p><strong>Duration:</strong> ${(track.duration_ms / 60000).toFixed(2)} min</p>
  </div>
`;

