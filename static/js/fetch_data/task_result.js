$(document).ready(function() {
  $(".sortable").click(function() {
    var sortField = $(this).data("sort-field");
    var sortDirection = $(this).data("sort-direction") || "asc";

    // Toggle sort direction
    if (sortDirection === "asc") {
      sortDirection = "desc";
    } else {
      sortDirection = "asc";
    }

    // Update sort direction data attribute
    $(this).data("sort-direction", sortDirection);

    // Add or remove sorting indicator classes
    $(".sortable").removeClass("sorted-asc sorted-desc");
    $(this).addClass("sorted-" + sortDirection);

    // Call the sorting function with the selected field and direction
    sortTable(sortField, sortDirection);
  });

  function sortTable(field, direction) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.querySelector("#example");
    switching = true;

    while (switching) {
      switching = false;
      rows = Array.from(table.rows).slice(1); // Exclude the table header row

      for (i = 0; i < rows.length - 1; i++) {
        shouldSwitch = false;
        x = rows[i].querySelectorAll("td")[field].innerText;
        y = rows[i + 1].querySelectorAll("td")[field].innerText;

        if (direction === "asc") {
          if (parseFloat(x) > parseFloat(y)) {
            shouldSwitch = true;
            break;
          }
        } else if (direction === "desc") {
          if (parseFloat(x) < parseFloat(y)) {
            shouldSwitch = true;
            break;
          }
        }
      }

      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }
});