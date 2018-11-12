var map;
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
});


// function addManagerToTable(){
// 	console.log("Im here and b = ");
// 	var a = document.getElementById("manager_selector");
// 	var b = a.value;
	
// 	if(b != "null"){
// 		var ob = document.getElementsByName("flaskManager");
// 		if(ob.length == 0){
// 			var node = document.getElementById("insertManager");//insertManager is name of table
// 			var trNode = document.createElement("input");
// 			trNode.setAttribute("name", "flaskManager");
// 			trNode.setAttribute("type", "text");
// 			trNode.setAttribute("class", "dis");
// 			trNode.setAttribute("value", b)
// 			node.appendChild(trNode);
// 			console.log(node)
			
// 		}else{
// 			var bool = exists(b, ob);
// 			if(bool ==false){
// 				var node = document.getElementById("insertManager");//insertManager is name of table
// 				var trNode = document.createElement("input");
// 				trNode.setAttribute("name", "flaskManager");
// 				trNode.setAttribute("type", "text");
// 				trNode.setAttribute("class", "dis");
// 				trNode.setAttribute("value", b)
// 				node.appendChild(trNode);

// 			}
// 		}	
// 	}
// 	a.selectedIndex= -1;

// }

// function addCanvasserToTable(){
// 	var a = document.getElementById("canvasser_selector");
// 	var b = a.value;
// 	if(b != "null"){
// 		var ob = document.getElementsByName("flaskCanvasser");
// 		if(ob.length == 0){
// 			var node = document.getElementById("insertCanvasser");//insertManager is name of table
// 			var trNode = document.createElement("input");
// 			trNode.setAttribute("name", "flaskCanvasser");
// 			trNode.setAttribute("type", "text");
// 			trNode.setAttribute("class", "dis");
// 			trNode.setAttribute("value", b)
// 			node.appendChild(trNode);
			

// 		}else{
// 			var bool = exists(b, ob);
// 			if(bool == false){
// 				var node = document.getElementById("insertCanvasser");//insertManager is name of table
// 				var trNode = document.createElement("input");
// 				trNode.setAttribute("name", "flaskCanvasser");
// 				trNode.setAttribute("type", "text");
// 				trNode.setAttribute("class", "dis");
// 				trNode.setAttribute("value", b)
// 				node.appendChild(trNode);
				
// 			}
// 		}	
// 	}
// 	a.selectedIndex= -1;

// }
// function addLocationToTable(){

// 	var a = document.getElementById("address");
// 	var b = a.value;

//     geocoder = new google.maps.Geocoder();
    
//     var exit = false;
//     geocoder.geocode({'address':b},function(results,status){
//     	if(status == 'OK'){
//     		map.setCenter(results[0].geometry.location);
// 	    	var marker = new google.maps.Marker({
//             	map: map,
//             	position: results[0].geometry.location
//         	});


// 	    	if(b != "null"){
// 				var ob = document.getElementsByName("flaskLocation");
// 				if(ob.length == 0){
// 					var node = document.getElementById("insertLocation");
// 					var trNode = document.createElement("input");
// 					trNode.setAttribute("name","flaskLocation");
// 					trNode.setAttribute("type", "text");
// 					trNode.setAttribute("class", "dis");
// 					trNode.setAttribute("value", b)	
// 					node.appendChild(trNode);	
// 				}else{
// 					var bool = exists(b, ob);
// 					if(bool ==false){
// 						var node = document.getElementById("insertLocation");
// 						var trNode = document.createElement("input");
// 						trNode.setAttribute("name", "flaskLocation");
// 						trNode.setAttribute("type", "text");
// 						trNode.setAttribute("class", "dis");
// 						trNode.setAttribute("value", b)
// 						node.appendChild(trNode);
						
// 					}
// 				}
// 				a.selectedIndex = -1;	
// 			}
// 	    }else {
// 	    	exit = true;
//         	alert('There is no such place on Earth: ');
        	
//       	}
//     });
     
   

	
// }

// function addQuestionToTable(){
// 	var a = document.getElementById("questions");
// 	var b = a.value;
// 	if(b != "null"){
// 		var ob = document.getElementsByName("flaskQuestion");
// 		if(ob.length == 0){
// 			var node = document.getElementById("insertQuestions");
// 			var trNode = document.createElement("input");
// 			trNode.setAttribute("name","flaskQuestion");
// 			trNode.setAttribute("type", "text");
// 			trNode.setAttribute("class", "dis");
// 			trNode.setAttribute("value", b)	
// 			node.appendChild(trNode);	
// 		}
// 		else{
// 			var bool = exists(b, ob);
// 			if(bool ==false){
// 				var node = document.getElementById("insertQuestions");
// 				var trNode = document.createElement("input");
// 				trNode.setAttribute("name", "flaskQuestion");
// 				trNode.setAttribute("type", "text");
// 				trNode.setAttribute("class", "dis");
// 				trNode.setAttribute("value", b)
// 				node.appendChild(trNode);
				
// 			}
// 		}
// 	a.selectedIndex = -1;	
// 	}
// }

// function exists(text, arr ){
// 	for( var i = 0; i < arr.length; i++){
// 		if(text == arr[i].value){
// 			return true;
// 		}
// 	}
// 	return false;
// }