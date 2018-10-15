$(function(){
    // Instantiate UI tabs vertical
    $( "#tabs-collapsible" ).tabs({
        collapsible: true
    });

    $("#globalButton").click(function()
    {
    	var current_day = $("#day_value").text();
    	var choice_day = $("#avgworkday option:selected").val();

    	var current_speed = $("#speed_value").text();
    	var choice_speed = $("#avgmovspeed option:selected").val();

    	if( ((choice_day).trim() == (current_day).trim())  && ((choice_speed).trim()==(current_speed).trim()) ){
            alert("You did not change anything !");
    	}
    	else{
    		alert("Update The Global Parameters Successfully!");
    	}

    	});
});


