$(document).ready(function() {
    $('#alert-close').click(function() {
        $('.alert-container').css({maxHeight: 0, opacity: 0});
    });
<<<<<<< HEAD
    function closeFeedback() {
    	$('#feedback').hide();
    }
    function openFeedback(name, percent) {
    	$('#feedback #building').html(name);
    	$('#feedback #percentage').html(percent);
    	$('#feedback').show();
    }
    function sendFeedback() {
    	// Do something
    }
});
=======
});

//  '/feedback/<building_id>/<feedack_percentage>/<current_percentage>', methods =['POST'])
function retrieveDataOnClick(group_id, percentage, button_response) {
    $.post("/feedback/" + group_id + "/" + button_response + "/" + percentage, {
        
  });
  };
>>>>>>> 945ac5de19c77bb0f2a89b8bde29ef45bb0384b9
