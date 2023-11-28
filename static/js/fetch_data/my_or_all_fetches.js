// $(document).ready(function() {
//   // Handle click event on the rows with data-toggle="collapse"
//   $('tr[data-toggle="collapse"]').click(function() {
//     // Toggle the visibility of the next row with class "details-row"
//     $(this).next('.details-row').toggleClass('show');
//   });
// });


$('table tbody').on('click', 'td.details-control', function () {
  var tr = $(this).closest('tr');
  var row = table.row( tr );

  if ( row.child.isShown() ) {
      // This row is already open - close it
      row.child.hide();
      tr.removeClass('shown');
  }
  else {
      // Open this row
      row.child( format(row.data()) ).show();
      tr.addClass('shown');
  }
} );

