[...document.getElementsByClassName("day-picker")].forEach(
  (element, index, array) => {
    let o = element.getElementsByTagName("option");
  for (var i=0; i<o.length; i++) {
    if (o[i].value == (new Date()).getDay())
      o[i].selected = true;
    }
  }
);
