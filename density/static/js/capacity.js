$(document).ready(function() {
    $('#alert-close').click(function() {
        $('.alert-container').css({maxHeight: 0, opacity: 0});
    });
});

//  '/feedback/<building_id>/<feedack_percentage>/<current_percentage>', methods =['POST'])
function retrieveDataOnClick(group_id, percentage, button_response) {   
    PERCENTAGES = [20,10,0,10,20]
    feedack_percentage = PERCENTAGES[button_response]
    console.log(group_id + " // " + feedack_percentage + " // " + percentage);
    $.post("/feedback/" + group_id + "/" + feedack_percentage + "/" + percentage, {
  });
  };

function closeFeedback() {
	var radio_buttons = $("input[name='capacity']");
	for (var i = 0; i < radio_buttons.length; i++) {
		radio_buttons[i].checked = false;
	}
	$('#feedback').hide();
}
function openFeedback(name, percent) {
	$('#feedback #building').html(name);
	$('#feedback #percentage').html(percent);
	$('#feedback').show();
}
function sendFeedback() {
	var group_id = $('#feedback #building').html();
	var percentage = $('#feedback #percentage').html();
	var button_response = $("input[name='capacity']:checked").val();
	if (button_response == undefined) {
		alert('Please select an option.');
		return;
	}
	retrieveDataOnClick(group_id, percentage, button_response);
	closeFeedback();
}
