(function(){

var bounds = [
  [-84.592237, 33.549660],
    [-84.145166, 33.984207]     
  ];

mapboxgl.accessToken = 'pk.eyJ1IjoibW94eXBlZCIsImEiOiJjaWgydGpwdmYweHJydnFtMzZzOXpmNjg3In0.5TXWYv0Z7nsOZHneIQOhxg';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/moxyped/cjdmf6fvu1jq02snw8ej5ttan',
    center: [-84.380378, 33.767279],
    zoom: 4,
    maxBounds: bounds,
    customAttribution: ['<a href=https://www.regenerative-planners.com/ target=_blank>Regenerative Planners</a>']
});




map.on('load', function() {


 /* map.addSource('gacounties', {
    'type' : 'geojson',
    'data' : 'data/gacounties.json' 
  })
  
  map.addLayer({'id' : 'gacounties',
    'type' : 'fill',
    'source': 'gacounties', 
    'paint' : {
      'fill-color':'#c5c5b5',
      'fill-opacity': 0.01,
      'fill-outline-color' : '#ffffff'
    }
  })
  
  
  map.addSource('AtlantaCityLimits', {
    'type' : 'geojson',
    'data' : 'data/AtlantaCityLimits.json' 
  })
  
  map.addLayer({'id' : 'AtlantaCityLimits',
    'type' : 'fill',
    'source': 'AtlantaCityLimits', 
    'paint' : {
      'fill-color':'#b8c7c7',
      'fill-opacity': 0.20,
      'fill-outline-color' : '#96a2a2'
    }
  })
  
  
  map.addSource('gisosmpoisafree1', {
    'type' : 'geojson',
    'data' : 'data/gisosmpoisafree1.json' 
  })
  
  map.addLayer({'id' : 'gisosmpoisafree1',
    'type' : 'fill',
    'source': 'gisosmpoisafree1', 
    'paint' : {
      'fill-color':'#67c985',
      'fill-opacity':1.0, 
      'fill-outline-color' : '#5cb477'
    }
  })
  
  map.addSource('garoads', {
    'type' : 'geojson',
    'data' : 'data/garoads.json' 
  })
  
  map.addLayer({'id' : 'garoads',
    'type' : 'line',
    'source': 'garoads', 
    'paint' : {
      'line-color':'#92b1d2',
      'line-opacity':1.0, 
    }
  })*/


  map.addSource('BeltLine', {
    'type' : 'geojson',
    'data' : 'data/BeltLine.json' 
  })

  map.addLayer({'id' : 'BeltLine',
    'type' : 'line',
    'source': 'BeltLine', 
    'paint' : {
      'line-color':'#5cb477',
      'line-opacity':1.0, 
    }
  })


  map.addSource('AcceleratedPlanforSaferStreets', {
    'type' : 'geojson',
    'data' : 'data/AcceleratedPlanforSaferStreets.json' 
  })

  map.addLayer({'id' : 'AcceleratedPlanforSaferStreets',
    'type' : 'line',
    'source': 'AcceleratedPlanforSaferStreets', 
    'paint' : {
      'line-color':'#3aaed8',
      'line-opacity':1.0, 
    }
  })

  



  map.addSource('ProposedLanes', {
    'type' : 'geojson',
    'data' : 'data/ProposedLanes.json' 
  })

  map.addLayer({'id' : 'ProposedLanes',
    'type' : 'line',
    'source': 'ProposedLanes', 
    'paint' : {
      'line-color':'#e31a1c',
      'line-opacity':1.0, 
    }
  })

  
  map.addSource('ProtectedBikeLane', {
    'type' : 'geojson',
    'data' : 'data/ProtectedBikeLane.json' 
  })

  map.addLayer({'id' : 'ProtectedBikeLane',
    'type' : 'line',
    'source': 'ProtectedBikeLane', 
    'paint' : {
      'line-color':'#757575',
      'line-opacity':1.0, 
    }
  })

  
  map.addSource('scooterroutesjoinedcopycopy', {
    'type' : 'geojson',
    'data' : 'data/scooterroutesjoinedcopycopy.json' 
  })

  map.addLayer({'id' : 'scooterroutesjoinedcopycopy',
    'type' : 'line',
    'source': 'scooterroutesjoinedcopycopy', 
    'paint' : {
      'line-color':'#FCAF58',
      'line-opacity':1.0, 
    }
  })

  map.addSource('UnprotectedBikeLane', {
    'type' : 'geojson',
    'data' : 'data/UnprotectedBikeLane.json' 
  })

  map.addLayer({'id' : 'UnprotectedBikeLane',
    'type' : 'line',
    'source': 'UnprotectedBikeLane', 
    'paint' : {
      'line-color':'#fdbf6f',
      'line-opacity':1.0, 
    }
  })


});

map.on('click','BeltLine', function(e){
  var features = map.queryRenderedFeatures(e.point);
  console.log(e);
  updateArea(features);
})

var draw = new MapboxDraw({
    displayControlsDefault: false,

    controls: {
      point: true,
      polygon: true,
      trash: true
    }
});

function updateArea(e){
  var features = e;
  document.getElementById('netET').innerHTML = features[0].properties.Net_ET;
  document.getElementById('oneYear').innerHTML = features[0].properties.Inches_2;
  document.getElementById('ecoRegion').innerHTML = features[0].properties.NA_L3NAME;
  document.getElementById('jobs2housing').innerHTML = features[0].properties.Job2House;
}

map.addControl(new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    country: 'us',
    region: 'Georgia',
    bbox:  [-86.010452, 30.537327, -80.771171, 35.210589] ,
}), 'top-right');

map.on('click', function(e){
  if(event.altKey){
    console.log("The alt was pressed!")
    var urlIsochrone = 'https://api.mapbox.com/isochrone/v1/mapbox/walking/'+e.lngLat.lng+','+e.lngLat.lat+'?contours_minutes=5,10&contours_colors=6706ce,04e813&polygons=true&access_token=pk.eyJ1IjoibW94eXBlZCIsImEiOiJjaWgydGpwdmYweHJydnFtMzZzOXpmNjg3In0.5TXWYv0Z7nsOZHneIQOhxg'
    map.getSource('isochrone').setData(urlIsochrone);
  } 
});

var scale = new mapboxgl.ScaleControl({
    maxWidth: 100,
    unit: 'imperial'
});
map.addControl(scale, 'bottom-right');
scale.setUnit('imperial');
map.addControl(new mapboxgl.NavigationControl(), 'top-right');
map.addControl(draw, 'top-right');

function addFields(){
  var number = draw.getAll().features.length;
  var json = draw.getAll().features;

  var container = document.getElementById("user-input-container");
    while (container.hasChildNodes()) {
      container.removeChild(container.lastChild);
    }
    for (i=0;i<number;i++){
      container.appendChild(document.createTextNode("Feature " + (i+1) + (" ")));
      var feature_id = "Feature_"+(i+1);
      var input = document.createElement("input");
      input.type = "text";
      input.id = feature_id;
      input.value = json[i].id;
      container.appendChild(input);
      container.appendChild(document.createElement("br"));
    }
}

})();
