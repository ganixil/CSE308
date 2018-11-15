
var map;
$(document).ready(function () {

   // Generate Map 
   var mapOptions = {
		    center: new google.maps.LatLng(40.9256538, -73.140943),
		    zoom: 13
		}
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    
  });