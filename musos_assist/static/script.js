
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/singles/");
        const singles = await response.json();
        if (singles.length > 0) {
            const single = singles[0]; // Assuming we want the first single for now

            document.getElementById("artwork").src = single.artwork_url;
            document.getElementById("audio").src = single.audio_preview_url;
            const sanitizedLyrics = single.lyrics.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>");
            document.getElementById("lyrics").innerHTML = sanitizedLyrics;
            document.getElementById("title").textContent = single.title;
            document.getElementById("artist").textContent = single.artist_names.join(", ");
            document.getElementById("release-date").textContent = single.release_date;
            document.getElementById("genre").textContent = single.genres.join(", ");
            document.getElementById("subgenres").textContent = single.subgenres.join(", ");
            document.getElementById("credits").textContent = single.credits;
            document.getElementById("isrc").textContent = single.isrc;
            document.getElementById("label").textContent = single.label;
            document.getElementById("version").textContent = single.version;
            document.getElementById("formats").textContent = single.formats.join(", ");
            document.getElementById("duration").textContent = single.duration;
            document.getElementById("catalog_number").textContent = single.catalog_number;
            document.getElementById("composers").textContent = single.composers.join(", ");
            document.getElementById("producers").textContent = single.producers.join(", ");
            document.getElementById("language").textContent = single.language;
            document.getElementById("notes").textContent = single.notes.replace(/\n/g, "<br>");
        }
    } catch (error) {
        console.error("Error fetching singles:", error);
    }
});
