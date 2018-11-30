/**
 * About container is truncated on mobile view.
 * This function expands the about container to
 * the reveal additional information available on
 * a non-mobile view.
 */
$('#expand-collapse').click(function() {
  if (! $('#learn-more').hasClass('open')) {
    $('#learn-more').html('<strong>COLLAPSE</strong>');
    $('#learn-more').addClass('open');
    $('#expandable').addClass('expanded');
  } else {
    $('#learn-more').html('<strong>LEARN MORE</strong>');
    $('#learn-more').removeClass('open');
    $('#expandable').removeClass('expanded');
  }
});

/**
 * Darkens a button in the nav bar corresponding to the current page.
 * Uses URL string parsing to determine which page the user is on.
 */
$(document).ready(function() {
  var url = window.location.href;
  var darken = function darken(id) {
    document.getElementById(id).style.backgroundColor = '#2285c6';
  }

  if (url.indexOf('map') !== -1) {
    darken('nav-map');
  } else if (url.indexOf('docs') !== -1) {
    darken('nav-api');
  } else if (url.indexOf('about') !== -1) {
    darken('nav-about');
  } else if(url.indexOf('predict')!== -1) {
    darken('nav-predict')
  } else {
    darken('nav-home');
  }
});

function searchLocations() {
  var li = document.getElementsByTagName('li');
  var searchQuery = document.getElementById('search').value.toLowerCase();
  var locationFilter = '';
  var openFilter = '';

  var locationBtns = document.getElementsByName('location-filter');

  for(var i = 0; i < locationBtns.length; i++){
    if(locationBtns[i].checked){
      locationFilter = locationBtns[i].value;
     }
   }

  var openBtns = document.getElementsByName('open-filter');

  for(var i = 0; i < openBtns.length; i++){
    if(openBtns[i].checked){
      openFilter = openBtns[i].value;
     }
   }


  for (i = 0; i < li.length; i++) {
    var name = li[i].getAttribute('data-name').toLowerCase();
    var nickname = li[i].getAttribute('data-nickname').toLowerCase();
    var locationType = li[i].getAttribute('data-location-type');
    var openNow = li[i].getAttribute('data-open-now');

    if ((!name.includes(searchQuery) && !nickname.includes(searchQuery)) ||
        (locationFilter != '' && locationFilter != locationType) ||
        (openFilter != '' && openFilter != openNow)) {
      li[i].style.display = 'none';
    }
    else {
      li[i].style.display = 'block';
    }
  }
}

function clearFilter(name) {
  var ele = document.getElementsByName(name);
  for(var i=0; i<ele.length; i++)
    ele[i].checked = false;
  searchLocations();
}

//  '/feedback/<building_id>/<feedack_percentage>/<current_percentage>', methods =['POST'])
function retrieveDataOnClick(group_id, client_count, percentage, button_response) {
  $.post( "/feedback/" + group_id + "/" + button_response + "/" + percentage, {
    javascript_data: data 
});
}
