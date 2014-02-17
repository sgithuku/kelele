// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
// $(document).foundation();

// jQuery mapping goodness

jQuery(document).ready(function($) {


  //Set up the variables for our HTML elements

  function exportPosition(position) {

    // Get the geolocation properties and set them as variables
    latitude = position.coords.latitude;
    longitude  = position.coords.longitude;

    // Insert the google maps iframe and change the location using the variables returned from the API
    // jQuery('#map').html('<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.co.uk/?ie=UTF8&amp;ll='+latitude+','+longitude+'&amp;spn=0.332359,0.617294&amp;t=m&amp;z=11&amp;output=embed"></iframe>');

    //Make a call to the Google maps api to get the name of the location
    jQuery.ajax({
      url: 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latitude+','+longitude+'&sensor=true',
      type: 'POST',
      dataType: 'json',
      success: function(data) {
        //If Successful add the data to the 'location' div
       var elem = document.getElementById("location");
       elem.value = data.results[0].formatted_address;
      },
      error: function(xhr, textStatus, errorThrown) {
             errorPosition();
      }
    });
    
  }

  function errorPosition() {
            alert('Sorry couldn\'t find your location');
        }


//Check if the browser support geolocation

if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(exportPosition, errorPosition);

} else {
  alert('Sorry your browser doesn\'t support the Geolocation API'); 
}

});