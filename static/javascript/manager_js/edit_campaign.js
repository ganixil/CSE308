
function generate_map() {
	var mapOptions = {
	    center: new google.maps.LatLng(51.5, 40.12),
	    zoom: 10,
	    mapTypeId: google.maps.MapTypeId.HYBRID
	}
	var map = new google.maps.Map(document.getElementById("map"), mapOptions);
}


function displayEdit(){
	var a = document.getElementById("scampaign_name");
	//alert(a.value)
	document.getElementById("new_campaign_name").value = a.value; 
	document.getElementById("createCampaign").submit();

}

//<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBu-916DdpKAjTmJNIgngS6HL_kDIKU0aU&callback=myMap"></script>
