$(document).ready(function() {
  // Handle click event on the rows with data-toggle="collapse"
  $('tr[data-toggle="collapse"]').click(function() {
    // Toggle the visibility of the next row with class "details-row"
    $(this).next('.details-row').toggleClass('show');
  });
});