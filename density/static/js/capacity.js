$(document).ready(function() {
    $('#alert-close').click(function() {
        $('.alert-container').css({maxHeight: 0, opacity: 0});
    });
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