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


