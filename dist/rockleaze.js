function setVenueAttributes(container) {
    const CLUB = "Rockleaze";

    container.querySelectorAll("tr").forEach(row => {
      const cells = row.querySelectorAll("td");
      // This will be the time and date
      if (cells.length < 4) {
        row.dataset.venue = "home";
        return;
      }

      const homeTeam = cells[1].textContent.trim();
      row.dataset.venue = homeTeam.startsWith(CLUB) ? "home" : "away";
    });
}

function showHome() {
  document.querySelectorAll("tbody tr").forEach(row => {
    row.style.display = row.dataset.venue === "home" ? "" : "none";
  });
}

function showAll() {
  document.querySelectorAll("tbody tr").forEach(row => {
    row.style.display = "";
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // Find the fixture table and apply an observer
  const container = document.querySelector(".fixturetablediv");
  const observer = new MutationObserver(() => {
    const table = container.querySelector('table');
    if (table) {
      const body = table.querySelector('tbody');
      setVenueAttributes(body);
      // disconnect observer once styles are applied
      observer.disconnect();
    }
  });

  observer.observe(container, {
    childList: true,
    subtree: true
  });
});


