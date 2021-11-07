 
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())

})

let autocomplete_a;
let autocomplete_b;

function initAutocomplete() {
 
  autocomplete_a = new google.maps.places.Autocomplete(
   document.getElementById('id-google-address-a'),
   {
       types: ['address'],
       componentRestrictions: {'country': ['fr']},
   })
  
  autocomplete_a.addListener('place_changed', function(){
    onPlaceChanged('a')
  });
 

  autocomplete_b = new google.maps.places.Autocomplete(
   document.getElementById('id-google-address-b'),
   {
       types: ['address'],
       componentRestrictions: {'country': ['fr']},
   })
  
  autocomplete_b.addListener('place_changed', function(){
    onPlaceChanged('b')
  });

}
//deafak
function onPlaceChanged (addy){

    let auto
    let el_id
    let lat_id
    let long_id

    if ( addy === 'a'){
        auto = autocomplete_a
        el_id = 'id-google-address-a'
        lat_id = 'id-lat-a'
        long_id = 'id-long-a'
    }
    else{
        auto = autocomplete_b
        el_id = 'id-google-address-b'
        lat_id = 'id-lat-b'
        long_id = 'id-long-b'
    }

    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById(el_id).value

    geocoder.geocode( { 'address': address}, function(results, status) {
       
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#' + lat_id).val(latitude) 
            $('#' + long_id).val(longitude) 
            document.getElementById("submit").addEventListener("click", () => {
               
                CalcRoute()
               
            });
           
        } 
    }); 
}

function validateForm() {
    try{

       var valid = true;
        $('.geo').each(function () {
            if ($(this).val()=='') {
                valid = false;
                // return false;
                throw new Error("adresses non renseignées")
            }
           
        });
        return valid
    }
    catch (err) {
        alert(err.message)
    }
}

function CalcRoute(){
vitesse=document.getElementById('vitesse_id')
soc=document.getElementById('soc_id')
// waypoints=document.getElementById('waypoints')
// console.log(vitesse,soc)
try {
    
    // if ( validateForm() == false){
    //     throw new Error("adresses non renseignées")
    // }
    if ( validateForm() == true){
        if (vitesse.value==0 | soc.value==0){ 
            throw new Error("le soc et la vitesse doivent etre superieures à 0")
        }
        var params = {
            lat_a: $('#id-lat-a').val(),
            long_a: $('#id-long-a').val(),
            lat_b: $('#id-lat-b').val(),
            long_b: $('#id-long-b').val(),
            vitesse : vitesse.value, 
            soc:soc.value,
        };


        var esc = encodeURIComponent;
        var query = Object.keys(params)
            .map(k => esc(k) + '=' + esc(params[k]))
            .join('&');
        
        url = '/map?' + query
    
        
        window.location.assign(url)
    }
 
    
    } 
    
        // } catch (error) {
        //     alert("attention")
    
        catch (err) {
           alert(err.message)
        }
}

