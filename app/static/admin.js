function formSubmit(event) {
  var url = /* form */this.form.url; 
  
  event.preventDefault();

  var request = new XMLHttpRequest();
  request.open('POST', url, true);
  request.onload = function() { // request successful
  // we can use server response to our request now
    //console.log(request.responseText);
  };

  request.onerror = function() {
    // request failed
  };

  request.send(new FormData(event.target)); // create FormData from form that triggered event
  event.preventDefault();

  //location.reload();
}

// and you can attach form submit event like this for example
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form')
    .forEach(form => form.addEventListener("submit", formSubmit));
});