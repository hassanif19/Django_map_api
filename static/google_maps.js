
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)

})

const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 17;
let labelIndexc = 2;
// google.maps.event.addListener(map, "click", (event) => {
//   addMarker(event.latLng, map);
// });
function initMap() {
  var map = new google.maps.Map(document.getElementById('map-route'), {
    zoom: 7,
    center: {lat: lat_a, lng: long_a}
  });

    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer({
       draggable: true,
       map,
       panel: document.getElementById("right-panel"),
    });


     
   
    // const localContextMapView = new google.maps.localContext.LocalContextMapView({
    //   element: document.getElementById("map-route"),
    //   placeTypePreferences: [
    //     { type: "restaurant" },
    //     { type: "tourist_attraction" },
    //   ],
    //   maxPlaceCount: 12,
    // });
    // map.setOptions({
    //   center: {lat: lat_a, lng: long_a},
    //   zoom: 14,
    // });
    // const map = localContextMapView.map;


    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);
 
    // document.getElementById("submit").addEventListener("click", () => {
    //   calculateAndDisplayRoute(directionsService, directionsRenderer);
    // });
   
    
    // addMarkers({lat:49.087358,lng:1.510055});
    // addMarkers({lat:49.28214,lng:1.003392});
    // addMarker({lat:49.359123,lng:0.522731});
  
    
    // function addMarker(location, map) {
       
    //   new google.maps.Marker({
    //     position: location,
    //     label: labels[labelIndexc],
    //     map: map,
    //   });

    // }

    // //add marker function
    // function addMarkers(coords){
    //     var marker = new google.maps.Marker({
    //         position:coords,
    //         map:map,
    //         label: labels[labelIndex],
    //     });  
    // }
  
}

// function findNearestMarker(marker2) {
//   const marker1 =({lat:49.44014,lng:1.08941});
//   const marker2=({lat:49.44014,lng:1.08941});
//   var minDist = 1000,
//     // nearest_text = '*None*',
//     markerDist,
//     // get all objects added to the map
//     // objects = map.getObjects(),
//     // len = map.getObjects().length,
//     // i;

//   // iterate over objects and calculate distance between them
//   // for (i = 0; i < len; i += 1) {
//     markerDist = marker1.getGeometry().distance(marker2);
//     // if (markerDist < minDist) {
//       minDist = markerDist;
//       // nearest_text = objects[i].getData();
//     // }
//   // }

//   document.getElementById("total").innerHTML =('The nearest marker is: ' +minDist);
// }

function computeDistance(directionsService, waypt) {
  return new Promise((resolve, reject) => {
    directionsService.route({
      origin: origin,
      destination: destination,
      waypoints : [waypt],
      optimizeWaypoints: true,
      travelMode: 'DRIVING'
  }, (response, status) =>{console.log(response);
    if (status === "OK" && response){
        let total = 0;
        const myroute = response.routes[0];
        // computeTotalDistance(response)
        for (let i = 0; i < myroute.legs.length; i++) {
          total += myroute.legs[i].distance.value;
        }
        resolve({"distance": total, "response": response})
    } else {
      reject("Not able to calculate the distance");
    }
  });
  })
}

async function calculateAndDisplayRoute(directionsService,directionsDisplay) {
  const station=[]
  const listStations=JSON.parse(document.getElementById("listStations").innerText);
  displable = null
  minDist = 99999999999;
  try {
    for (let i = 0; i < listStations.length; i++) {
      const res = await computeDistance(directionsService, listStations[i])
      const {distance, response} = res
        if (minDist  > distance){
            minDist = distance;
            displable = response;
        }   
  }
  directionsDisplay.setDirections(displable);   
  } catch (error) {
    console.log(error);
            alert('Directions request failed due to ' + status);
          window.location.assign("/route");
  }
  
                

  
  //          distanceWaypoint(i);
           
  //      if (distanceWaypoint(i) < distanceWaypoint(i+1) {
  //           distanceWaypoint(i+1) = distanceWaypoint(i);
  //           satation[i+1]=station[i];
          
  //      }
  
  // }  

  // const wypts = JSON.parse(document.querySelectorAll("listStations").innerText);
  
  // console.log(wypts)
//  const waypts=[{"location": "5 Rue Edouard Poisson, Aubervilliers, France"}]; 
//  computeTotalDistance(response);
  
  // const waypts=[]
  // const checkboxArray = document.getEmentById("waypoints");
  // const wypts = [];

  // for (let i = 0; i < checkboxArray.length; i++) {
  //   if (checkboxArray.options[i].selected) {
  // const pars = JSON.parse(checkboxArray.options[i].value)
  // // console.log(pars)
   
  // wypts.push({
  //   location: checkboxArray[i].value,
  //   stopover: true,
  // });
  //   }
  // }  
 
  
 
    // directionsService.route({
    //     origin: origin,
      
         
    //     destination: destination,
    //     // waypoints:waypts,
         
    //     // optimizeWaypoints: true,
    //     travelMode: 'DRIVING'
    // }, 
    // function(response, status) {
    //   if (status === 'OK' && response) {
    //     directionsDisplay.setDirections(response);
    //   //   let total = 0;
    //   //   const myroute = response.routes[0];
    //   //   computeTotalDistance(response)
    //   //   for (let i = 0; i < myroute.legs.length; i++) {
    //   //     total += myroute.legs[i].distance.value;
    //   //   }
    //   //  total=total/1000; 
    //   //   document.getElementById("total").innerHTML = total + "km";
      
     
    //   } else {

    //     alert('Directions request failed due to ' + status);
    //     window.location.assign("/route")
    //   }
    // });
}
// function computeTotalDistance(response) {
//   let total = 0;
//   const myroute = reponse.routes[0];

//   if (!myroute) {
//     return;
//   }

//   for (let i = 0; i < myroute.legs.length; i++) {
//     total += myroute.legs[i].duration.value;
//   }
//  total=total/60; 
//   document.getElementById("total").innerHTML = total + " Minutes";
// }
 
 

