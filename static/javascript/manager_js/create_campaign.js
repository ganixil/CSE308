var map;
var today = new Date();
today.setHours(0,0,0,0);

$(document).ready(function () {
	var managers = document.getElementById('managers');
   	 multi( managers, {
                non_selected_header: 'Unselected Managers',
                selected_header: 'Selected Managers'
            });

	var canvassers = document.getElementById('canvassers');
   	multi( canvassers, {
                non_selected_header: 'Unselected Canvassers',
                selected_header: 'Selected Canvassers'
            });

   // Generate Map 
   var mapOptions = {
		    center: new google.maps.LatLng(40.758896, -73.985130),
		    zoom: 13
		}

	map = new google.maps.Map(document.getElementById("map"), mapOptions);
  geocoder = new google.maps.Geocoder();

	var input = document.getElementById('location');
	var searchBox = new google.maps.places.SearchBox(input);

	var markers = [];
        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];

          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }

          var infowindow = new google.maps.InfoWindow({
          		content: place.formatted_address
          });
            // Create a marker for each place.
            var single_marker = new google.maps.Marker({
              map: map,
              animation: google.maps.Animation.DROP,
              title: place.name,
              position: place.geometry.location

            });

            markers.push(single_marker);
            infowindow.open(map, single_marker);

           single_marker.addListener('click', function() {
              infowindow.open(map, single_marker);
        });


            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
          });
          map.fitBounds(bounds);
        });

        google.maps.event.addListener(map, 'click', function(event) {
           geocoder.geocode({
            'latLng': event.latLng
              }, function (results, status) {
                  if (status == google.maps.GeocoderStatus.OK) {
                      if (results[0]) {
                         document.getElementById('location').value = results[0].formatted_address;
                         var trigger = new Event('change');
                         document.getElementById('location').dispatchEvent(trigger);
                      } else {
                          alert('No results found');
                      }
                  } else {
                      alert('Geocoder failed due to: ' + status);
                  }
        });
  });

        // Initial Current Date to start date
        document.getElementById('start_date').value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
});

function validDates(){
     var start_date = document.getElementById('start_date');
     var end_date = document.getElementById('end_date');
     // If Both dates are not empty, check if they are invalid
     if(start_date.value && end_date.value){
          start = start_date.value.replace(/-/g,'/');
          end = end_date.value.replace(/-/g,'/');
          start_obj = new Date(start);
          end_obj = new Date(end);
          if(start_obj.getTime() < today.getTime()){
                start_date.value =today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
                end_date.value='';
               alert("Invalid Date Setttings, please make sure dates should start from current date, and in valid ranges!!");
          }else if(start_obj.getTime() > end_obj.getTime()){
                  start_date.value =today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
                  end_date.value='';
               alert("Invalid Date Setttings, please make sure dates should start from current date, and in valid ranges!!");
          }

     }
}

// Toggle Add Question Button
function toggle_question(){
    if(document.getElementById('question').value){
                document.getElementById('add_question').classList.remove("disabled");
                document.getElementById('add_question').disabled = false;
            }
    else{     
                document.getElementById('add_question').classList.add("disabled");
                document.getElementById('add_question').disabled = true;
  } 
}


// Toggle Add LocationButton
function toggle_location(){
    if(document.getElementById('location').value){
                document.getElementById('add_location').classList.remove("disabled");
                document.getElementById('add_location').disabled = false;
            }
    else{     
                document.getElementById('add_location').classList.add("disabled");
                document.getElementById('add_location').disabled = true;
  } 
}

function add_question(){
   var question = document.getElementById('question').value;
   var question_list = document.getElementById('question_list');
   var all_options = question_list.options;
   var add = true;
    for(var i=0; i < all_options.length; i++)
     {
        if(all_options[i].value == question){
             alert("The question does already exist!!");
             document.getElementById('question').value ='';
                add= false;  // We do not need to create option
                break;
        }
     }
     if(add){
      // Need to add new question
         var option = document.createElement("option");
         option.value = question.trim();
         option.text = question.trim();
         question_list.add(option);
         document.getElementById('question').value ='';
         // Toggle Remove question button
         document.getElementById('remove_question').classList.contains('disabled');
         document.getElementById('remove_question').classList.remove("disabled");
         document.getElementById('remove_question').disabled = false;
      }
        var trigger = new Event('change');
        document.getElementById('question').dispatchEvent(trigger);
}


function remove_question(){
      var question_list = document.getElementById('question_list');
      var i=0;
      var cout_unselect = 0;
      while(1){
          if(cout_unselect == question_list.options.length){
                break;
          }
          cout_unselect = 0;
          for (var i = 0; i < question_list.options.length; i++) {
              if(question_list.options[i].selected){
                alert("hre");
                  question_list.options[i]=null;
              }else{
                  cout_unselect ++;
              }
          }
      }
        if(question_list.options.length == 0){
                // Toggle Remove question button
               document.getElementById('remove_question').classList.add("disabled");
               document.getElementById('remove_question').disabled = true;
        }

}


function add_location(){
   var location = document.getElementById('location').value;
   var location_list = document.getElementById('location_list');
   var all_options = location_list.options;
   var add = true;
    for(var i=0; i < all_options.length; i++)
     {
        if(all_options[i].value ==location){
             alert("The location does already exist!!");
              document.getElementById('location').value ='';
              add= false;  // We do not need to create option
                break;
        }
     }
     if(add){
      // Need to add new location
      // Check if the string of address is valid or not
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': location}, function(results, status){
            if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
                // set it to the correct, formatted address if it's valid
                var option = document.createElement("option");
                var lat = results[0].geometry.location.lat();
                var lng = results[0].geometry.location.lng();
                option.value = results[0].formatted_address.trim()+'|'+lat+'|'+lng;
                option.text = results[0].formatted_address.trim();
                location_list.add(option);
                         // Toggle Remove location button
               document.getElementById('remove_location').classList.contains('disabled');
               document.getElementById('remove_location').classList.remove("disabled");
               document.getElementById('remove_location').disabled = false;
            }else {
              alert("Invalid address");
          }
        });
         document.getElementById('location').value ='';
      }
        var trigger = new Event('change');
        document.getElementById('location').dispatchEvent(trigger);
}

function remove_location(){
      var location_list = document.getElementById('location_list');
      var i=0;
      var cout_unselect = 0;
      while(1){
         alert(cout_unselect);
          if(cout_unselect == location_list.options.length){
                break;
          }
          cout_unselect = 0;
          for (var i = 0; i < location_list.options.length; i++) {
              if(location_list.options[i].selected){
                  location_list.options[i]=null;
              }else{
                  cout_unselect ++;
              }
          }
      }
        if(location_list.options.length == 0){
                // Toggle Remove question button
               document.getElementById('remove_location').classList.add("disabled");
               document.getElementById('remove_location').disabled = true;
        }

}


function  check_submit(){
  // Check if there're some managers
    var managers = document.getElementById('managers');
    var has_managers= false;
    for (var i = 0; i < managers.options.length; i++) {
      if (managers.options[i].selected) {
            has_managers= true;
             break;
      }
    }
    if(! has_managers){
        alert("Failed to create, Please Select at least one manager!!");
        return false;
    }
    // Check if there're some canvassers
    var canvassers = document.getElementById('canvassers');
    var has_canvassers= false;
    for (var i = 0; i < canvassers.options.length; i++) {
      if (canvassers.options[i].selected) {
            has_canvassers= true;
             break;
      }
    }
    if(!has_canvassers){
       alert("Failed to create, Please Select at least one canvasser!!");
       return false;
    }

    // Mark all options to be true for questions and locations
    var question_list = document.getElementById('question_list');
        for (var i = 0; i <  question_list.options.length; i++) {
              question_list.options[i].selected = true;
            }

    var location_list = document.getElementById('location_list');
        for (var i = 0; i <  location_list.options.length; i++) {
              location_list.options[i].selected = true;
            }

}