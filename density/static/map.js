// vanilla js document.ready bc we are kool kids
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('map').addEventListener('load', function() {
    
    //Iterate through locations and display their data
    var data = document.querySelector('#data');
    var locations = JSON.parse(data.dataset.locations);
    var map = document.getElementById('map');
    var innerSvg = map.contentDocument;
    var popup = document.getElementById('locationPopup');

    var initialOffsetTop = map.getBoundingClientRect().top + window.scrollY;
    var initialOffsetLeft = map.getBoundingClientRect().left + window.scrollX;
    
    //Create a mapping from parent_id --> text representation
    var buildingStrings = {};
    
    //Create a mapping from parent_id --> list full %s for elements inside (e.g. floors of a building)
    var buildingFloors = {};

    //Create a mapping from parent_id --> query (http://....hours)
    var buildingHours = {};
    
    locations.forEach(function(location) {
      if (location.name != 'Butler Library stk') { //We're skipping this out of non-use]
        if (buildingFloors[location.parentId] == null) {
          buildingFloors[location.parentId] = {};
        }
        if (buildingStrings[location.parentId] == null) {
          buildingStrings[location.parentId] = '<b>' + location.parentName + '</b><br />' +
            '<em>Click to view hours</em><br /><br />';
        }
        if (buildingHours[location.parentId] == null) {
          buildingHours[location.parentId] = 'https://www.google.com/#q=' + escape('Columbia University ' + location.parentName + ' hours');
        }
        
        buildingFloors[location.parentId][location.name] = location.fullness;
        buildingStrings[location.parentId] += location.name + ': ' + location.fullness + '%' + '<br />';
      }
    });

    //Iterate through mappings keys to set opacity for the element by fullness and better data on mouseover
    var buildings = Object.keys(buildingFloors);

    for (var i in buildings) {
      var building = buildings[i];
      var list = buildingFloors[building];
      
      //find average fullness for location (this is for locations w/ multiple floors)
      var totalFullness = 0;
      for (var entry in list){
        totalFullness += buildingFloors[building][entry];
      }

      //number of pixels offset to separate popup from mouse
      var mouseOffset = 4;
      var numFloorsInBuilding = Object.keys(list).length;

      var percent = (totalFullness / numFloorsInBuilding); //Should be from [0, 100]
      var buildingElement = innerSvg.getElementById('parent_' + building); //e.g. parent_43
      if(buildingElement != null) {
        buildingElement.style.opacity = percent / 100;
      }
      
      //opens new window with google search for hours
      buildingElement.onmousedown = function(event) {
        var location = this.id.replace('parent_', '');
        var query = buildingHours[location];
        window.open(query);
      }

      //displays popup at location of mouse
      buildingElement.onmouseenter = function(event) {
        popup.style.visibility = 'visible';
        var leftPosition = (initialOffsetLeft + event.clientX - 
          (popup.offsetWidth/2)).toString() + 'px'; // divide by 2 centers it (half of width)
        var topPosition = (initialOffsetTop - mouseOffset + event.clientY -
          (popup.offsetHeight)).toString() + 'px';
        popup.style.top = topPosition;
        popup.style.left = leftPosition;
        var location = this.id.replace('parent_', '');
        popup.innerHTML = buildingStrings[location];
      }

      buildingElement.onmouseout = function() {
        popup.style.visibility = 'hidden';
      }

      //moves popup with mouse
      buildingElement.onmousemove = function(event) {
        var leftPosition = (initialOffsetLeft + event.clientX - 
          (popup.offsetWidth/2)).toString() + 'px'; // divide by 2 centers it (half of width)
        var topPosition = (initialOffsetTop - mouseOffset + event.clientY -
          (popup.offsetHeight)).toString() + 'px';
        popup.style.top = topPosition;
        popup.style.left = leftPosition;
      }
    }
  });
});
