$(document).ready(function() {

    $('#alert-close').click(function() {
    	$('.alert-container').css({maxHeight: 0, opacity: 0});
    });

	// About container is truncated on mobile view.
	// This function expands the about container to
	// the reveal additional information available on
	// a non-mobile view.
	$("#expand-collapse").click(function() {
		if(! $("#learn-more").hasClass("open")) {
			$("#learn-more").html("<strong>COLLAPSE</strong>");
			$("#learn-more").addClass("open");
			$("#expandable").addClass("expanded");
		}
		else {
			$("#learn-more").html("<strong>LEARN MORE</strong>");
			$("#learn-more").removeClass("open");
			$("#expandable").removeClass("expanded");
		}
	});

});