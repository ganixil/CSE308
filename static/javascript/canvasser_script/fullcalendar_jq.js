// Get Today's Date
var today = new Date();

$(document).ready(function() {
		  
		/* initialize the external events
		-----------------------------------------------------------------*/
	
		$('#external-events div.external-event').each(function() {
		
			// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
			// it doesn't need to have a start or end
			var eventObject = {
				title: $.trim($(this).text()) // use the element's text as the event title
			};
			
			// store the Event Object in the DOM element so we can get to it later
			$(this).data('eventObject', eventObject);
			
			// make the event draggable using jQuery UI
			$(this).draggable({
				zIndex: 999,
				revert: true,      // will cause the event to go back to its
				revertDuration: 0  //  original position after the drag
			});
			
		});
		//for loop converting fetched jason
		var cEvents = JSON.parse(canvasEvents);
		//Check there're some data need to be loaded first
		if(cEvents){
			var clength = cEvents.length;
			for (var i=0;i<clength;i++){
				var startRaw = cEvents[i]["start"];
				alert(startRaw)
				alert(typeof startRaw);
				var start = new Date(Date.parse(startRaw));
				cEvents[i]["start"] = start;

			}
	}
		/* initialize the calendar
		-----------------------------------------------------------------*/
		var calendar =  $('#calendar').fullCalendar({
			header: {
				left: 'title',
				center: 'month',
				right: 'prevYear,prev,next,nextYear today'
			},
			buttonText:{
				month:'Month Calendar'
			},
			editable: true,
			firstDay: 1, //  1(Monday) this can be changed to 0(Sunday) for the USA system
			selectable: true,
			defaultView: 'month',
			
			columnFormat: {
                month: 'ddd'   // Mon
            },
            titleFormat: {
                month: 'MMMM yyyy' // September 2009
            },
			allDaySlot: false,
			selectHelper: true,
			select: function(start, end, allDay) {
				// Temp_date will be used to manipulate each date between strat and end
				var temp_date = new Date(start);
				var end_date = new Date(end);
				// Start Date must be greater than the today date
				if(temp_date.getTime() < today.getTime()){
					alert("Cannot set avaliablity on past dates !! ")
				}else{
				// Check if the 'temp_date' can be set avaliablity or not
						while(temp_date <= end_date){
						if(isAvaliable(temp_date)){
							 calendar.fullCalendar('renderEvent',
								{
									title: "Avaliable",
									start: temp_date,
									constraint: 'Ava', //an event ID
									textColor:'black !important',
									backgroundColor: "#FF3B30!important"
								},
								true // make the event "stick"
							);
						$.getJSON($SCRIPT_ROOT + '/canvasser/update_ava',
						{
							title: "Free",
							start: start,
							end: end,
							allDay: allDay
						},function(data){

						}
						)
						}
						temp_date = new Date(temp_date.getTime() + 86400000); // + 1 day in ms
					}
				}
				calendar.fullCalendar('unselect');
			},
			droppable: true, // this allows things to be dropped onto the calendar !!!
			drop: function(date, allDay) { // this function is called when something is dropped
			
				// retrieve the dropped element's stored Event Object
				var originalEventObject = $(this).data('eventObject');
				
				// we need to copy it, so that multiple events don't have a reference to the same object
				var copiedEventObject = $.extend({}, originalEventObject);
				
				// assign it the date that was reported
				copiedEventObject.start = date;
				copiedEventObject.allDay = allDay;
				
				// render the event on the calendar
				// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
				$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
				
				// is the "remove after drop" checkbox checked?
				if ($('#drop-remove').is(':checked')) {
					// if so, remove the element from the "Draggable Events" list
					$(this).remove();
				}
				
			},
			
			events: cEvents,			
		});
		
		
	});


function isAvaliable(check_date){
	var events = $('#calendar').fullCalendar('clientEvents', function (event) {
		alert("Cehck");
    //  for (var i=0; i < events.length, i++){
    //  	alert(events);
    // 	// alert(events[i].title);
    // }
  });
	return true;

}