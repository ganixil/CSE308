
function generate_map() {
	var mapOptions = {
	    center: new google.maps.LatLng(51.5, -0.12),
	    zoom: 10,
	    mapTypeId: google.maps.MapTypeId.HYBRID
	}
	var map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
generate_map();
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
		}


	});
}




function addManagerToTable(){
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
			if(bool ==false){
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


function exists(text, arr ){
	for( var i = 0; i < arr.length; i++){
		if(text == arr[i].value){
			return true;
		}
	}
	return false;
}
//
//<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBu-916DdpKAjTmJNIgngS6HL_kDIKU0aU&callback=myMap"></script>