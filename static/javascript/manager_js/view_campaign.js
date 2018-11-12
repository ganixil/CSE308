$(document).ready(function () {
    var table = $('#camp-table').DataTable();
    $(".detail").click(function(){
    	var index = this.closest('tr').rowIndex;
    	var campaign = $('#camp-table tr:eq('+index+') td:eq(0)').text();
    	$("#campaign-name").prop("value", campaign.trim());
    	$("#detail-container").show();
    	$("#user-table").hide();
    	$("#other-table").hide();
    });

});