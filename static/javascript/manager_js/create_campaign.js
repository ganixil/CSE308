var map;
var geocoder;
var exit = 0;
function generate_map() {
		var mapOptions = {
		    center: new google.maps.LatLng(51.5, 40.12),
		    zoom: 10,
		    mapTypeId: google.maps.MapTypeId.HYBRID
		}
		map = new google.maps.Map(document.getElementById("map"), mapOptions);
	}
generate_map();
// <option value='{{show}}' selected="selected">{{show}}</option>
function displayEdit(){
	var a = document.getElementById("scampaign_name");
	document.getElementById("new_campaign_name").value = a.value; 
	document.getElementById("createCampaign").submit();

}
function a(){
	document.addEventListener("click", function(e){
		if(e.target.name == "flaskManager"){
			var value = e.target.value;
			var arr = document.getElementsByName('flaskManager');

			for(var i = 0; i < arr.length; i++){
						
				if(arr[i].value == value){
				 	arr[i].parentNode.removeChild(arr[i]);
				}
			}
		}else if(e.target.name == "flaskCanvasser"){
			var value = e.target.value;
			var arr = document.getElementsByName('flaskCanvasser');

			for(var i = 0; i < arr.length; i++){
				if(arr[i].value == value){
				 	arr[i].parentNode.removeChild(arr[i]);
				}
			}
		}else if(e.target.name == "flaskLocation"){
			var value = e.target.value;
			var arr = document.getElementsByName('flaskLocation');

			for(var i = 0; i < arr.length; i++){
				if(arr[i].value == value){
				 	arr[i].parentNode.removeChild(arr[i]);
				}
			}
		}else if(e.target.name == "flaskQuestion"){
			var value = e.target.value;
			var arr = document.getElementsByName('flaskQuestion');

			for(var i = 0; i < arr.length; i++){
				if(arr[i].value == value){
				 	arr[i].parentNode.removeChild(arr[i]);
				}
			}
		}
	});
}

function addManagerToTable(){
	console.log("Im here and b = ");
	var a = document.getElementById("manager_selector");
	var b = a.value;
	
	if(b != "null"){
		var ob = document.getElementsByName("flaskManager");
		if(ob.length == 0){
			var node = document.getElementById("insertManager");//insertManager is name of table
			var trNode = document.createElement("input");
			trNode.setAttribute("name", "flaskManager");
			trNode.setAttribute("type", "text");
			trNode.setAttribute("class", "dis");
			trNode.setAttribute("value", b)
			node.appendChild(trNode);
			console.log(node)
			
		}else{
			var bool = exists(b, ob);
			if(bool ==false){
				var node = document.getElementById("insertManager");//insertManager is name of table
				var trNode = document.createElement("input");
				trNode.setAttribute("name", "flaskManager");
				trNode.setAttribute("type", "text");
				trNode.setAttribute("class", "dis");
				trNode.setAttribute("value", b)
				node.appendChild(trNode);

			}
		}	
	}
	a.selectedIndex= -1;

}

function addCanvasserToTable(){
	var a = document.getElementById("canvasser_selector");
	var b = a.value;
	if(b != "null"){
		var ob = document.getElementsByName("flaskCanvasser");
		if(ob.length == 0){
			var node = document.getElementById("insertCanvasser");//insertManager is name of table
			var trNode = document.createElement("input");
			trNode.setAttribute("name", "flaskCanvasser");
			trNode.setAttribute("type", "text");
			trNode.setAttribute("class", "dis");
			trNode.setAttribute("value", b)
			node.appendChild(trNode);
			

		}else{
			var bool = exists(b, ob);
			if(bool == false){
				var node = document.getElementById("insertCanvasser");//insertManager is name of table
				var trNode = document.createElement("input");
				trNode.setAttribute("name", "flaskCanvasser");
				trNode.setAttribute("type", "text");
				trNode.setAttribute("class", "dis");
				trNode.setAttribute("value", b)
				node.appendChild(trNode);
				
			}
		}	
	}
	a.selectedIndex= -1;

}
function addLocationToTable(){

	var a = document.getElementById("address");
	var b = a.value;

    geocoder = new google.maps.Geocoder();
    
    var exit = false;
    geocoder.geocode({'address':b},function(results,status){
    	if(status == 'OK'){
    		map.setCenter(results[0].geometry.location);
	    	var marker = new google.maps.Marker({
            	map: map,
            	position: results[0].geometry.location
        	});


	    	if(b != "null"){
				var ob = document.getElementsByName("flaskLocation");
				if(ob.length == 0){
					var node = document.getElementById("insertLocation");
					var trNode = document.createElement("input");
					trNode.setAttribute("name","flaskLocation");
					trNode.setAttribute("type", "text");
					trNode.setAttribute("class", "dis");
					trNode.setAttribute("value", b)	
					node.appendChild(trNode);	
				}else{
					var bool = exists(b, ob);
					if(bool ==false){
						var node = document.getElementById("insertLocation");
						var trNode = document.createElement("input");
						trNode.setAttribute("name", "flaskLocation");
						trNode.setAttribute("type", "text");
						trNode.setAttribute("class", "dis");
						trNode.setAttribute("value", b)
						node.appendChild(trNode);
						
					}
				}
				a.selectedIndex = -1;	
			}
	    }else {
	    	exit = true;
        	alert('There is no such place on Earth: ');
        	
      	}
    });
     
   

	
}

function addQuestionToTable(){
	var a = document.getElementById("questions");
	var b = a.value;
	if(b != "null"){
		var ob = document.getElementsByName("flaskQuestion");
		if(ob.length == 0){
			var node = document.getElementById("insertQuestions");
			var trNode = document.createElement("input");
			trNode.setAttribute("name","flaskQuestion");
			trNode.setAttribute("type", "text");
			trNode.setAttribute("class", "dis");
			trNode.setAttribute("value", b)	
			node.appendChild(trNode);	
		}
		else{
			var bool = exists(b, ob);
			if(bool ==false){
				var node = document.getElementById("insertQuestions");
				var trNode = document.createElement("input");
				trNode.setAttribute("name", "flaskQuestion");
				trNode.setAttribute("type", "text");
				trNode.setAttribute("class", "dis");
				trNode.setAttribute("value", b)
				node.appendChild(trNode);
				
			}
		}
	a.selectedIndex = -1;	
	}
}

function exists(text, arr ){
	for( var i = 0; i < arr.length; i++){
		if(text == arr[i].value){
			return true;
		}
	}
	return false;
}