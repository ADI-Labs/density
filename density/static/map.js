// vanilla js document.ready bc we are kool kids
document.addEventListener("DOMContentLoaded", function() {

    document.getElementById('map').addEventListener("load", function(){
        //Iterate through locations and display their data
        var data = document.querySelector("#data");
        var locations = JSON.parse(data.dataset.locations);
        var map = document.getElementById('map');
        var innerSvg = map.contentDocument;
        var popup = document.getElementById('locationPopup');

        var initialOffsetTop = map.getBoundingClientRect().top + window.scrollY;
        var initialOffsetLeft = map.getBoundingClientRect().left + window.scrollX;
        
        //Create a mapping from parent_id --> text representation
        var parentToText = new Object();
        //Create a mapping from parent_id --> list full %s for elements inside (e.g. floors of a building)
        var parentToList = new Object();
        //Create a mapping from parent_id --> query (http://....hours)
        var parentToQuery = new Object();
        
        for(var i = 0; i < locations.length; i++){ 
            if(locations[i].name != "Butler Library stk"){ //We're skipping this out of non-use]
                if(parentToList[locations[i].parentId] == null){
                    parentToList[locations[i].parentId] = new Object();
                }
                if(parentToText[locations[i].parentId] == null){
                    parentToText[locations[i].parentId] = "<b>" + locations[i].parentName + "</b><br />" +
                        "<em>Click to view hours</em><br /><br />";
                }
                if(parentToQuery[locations[i].parentId] == null){
                    parentToQuery[locations[i].parentId] = "https://www.google.com/#q=" + escape("Columbia University " + locations[i].parentName + " hours");
                }
                
                parentToList[locations[i].parentId][locations[i].name] = locations[i].fullness;
                parentToText[locations[i].parentId] += locations[i].name + ": " + locations[i].fullness + "%" + "<br />";
            }
        }

        //Iterate through mappings keys to set opacity for the element by fullness and better data on mouseover
        var keySet = Object.keys(parentToList);

        for(var key in keySet){
            var keyValue = keySet[key];
            var list = parentToList[keyValue];
            
            //find average fullness for location (this is for locations w/ multiple floors)
            var count = 0;
            var totalFullness = 0;
            for(var entry in list){
                totalFullness += parentToList[keyValue][entry];
                count++;
            }

            //number of pixels offset to separate popup from mouse
            var mouseOffset = 4;
            
            if(count != 0){
                var percent = (totalFullness / count); //Should be from [0, 100]
                var buildingElement = innerSvg.getElementById('parent_' + keyValue); //e.g. parent_43
                if(buildingElement != null){
                    buildingElement.style.opacity = percent / 100;
                }
                
                //opens new window with google search for hours
                buildingElement.onmousedown = function(event){
                    var location = this.id.replace("parent_", "");
                    var query = parentToQuery[location];
                    window.open(query);
                }

                //displays popup at location of mouse
                buildingElement.onmouseenter = function(event){
                    popup.style.visibility = 'visible';
                    var leftPosition = (initialOffsetLeft + event.clientX - 
                        (popup.offsetWidth/2)).toString() + "px"; // divide by 2 centers it (half of width)
                    var topPosition = (initialOffsetTop - mouseOffset + event.clientY -
                        (popup.offsetHeight)).toString() + "px";
                    popup.style.top = topPosition;
                    popup.style.left = leftPosition;
                    var location = this.id.replace("parent_", "");
                    popup.innerHTML = parentToText[location];
                }

                buildingElement.onmouseout = function(){
                    popup.style.visibility = 'hidden';
                }

                //moves popup with mouse
                buildingElement.onmousemove = function(event){
                    var leftPosition = (initialOffsetLeft + event.clientX - 
                        (popup.offsetWidth/2)).toString() + "px"; // divide by 2 centers it (half of width)
                    var topPosition = (initialOffsetTop - mouseOffset + event.clientY -
                        (popup.offsetHeight)).toString() + "px";
                    popup.style.top = topPosition;
                    popup.style.left = leftPosition;
                }
            }
        }
    });
});
