$(document).ready(function() {
    $('#alert-close').click(function() {
        $('.alert-container').css({maxHeight: 0, opacity: 0});
    });
});

//  '/feedback/<building_id>/<feedack_percentage>/<current_percentage>', methods =['POST'])
function retrieveDataOnClick(group_id, percentage, button_response) {
    
    PERCENTAGES = [20,10,0,10,20]
    feedack_percentage = PERCENTAGES[button_response]
    $.post("/feedback/" + group_id + "/" + button_response + "/" + percentage, {
  });
  };