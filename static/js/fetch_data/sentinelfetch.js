document.getElementById("coordinate_type").addEventListener("change", function() {
var xyFields = document.getElementById("xy_fields");
var lonlatFields = document.getElementById("lonlat_fields");

if (this.value === "xy") {
    xyFields.style.display = "block";
    lonlatFields.style.display = "none";
} else if (this.value === "lonlat") {
    xyFields.style.display = "none";
    lonlatFields.style.display = "block";
}
});

document.getElementById("date_type").addEventListener("change", function() {
var start_endFields = document.getElementById("Date_fields_start_end");
var ndaysFields = document.getElementById("Date_fields_ndays_before");

if (this.value === "start_end") {
    start_endFields.style.display = "block";
    ndaysFields.style.display = "none";
} else if (this.value === "days_before") {
    start_endFields.style.display = "none";
    ndaysFields.style.display = "block";
}
});