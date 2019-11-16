(function(){

var bounds = [
  [-84.592237, 33.549660],
    [-84.145166, 33.984207]     
  ];

mapboxgl.accessToken = 'pk.eyJ1IjoibW94eXBlZCIsImEiOiJjaWgydGpwdmYweHJydnFtMzZzOXpmNjg3In0.5TXWYv0Z7nsOZHneIQOhxg';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/moxyped/ck31zgoyh0ssb1cn787jlai36',    
    center: [-84.380378, 33.767279],
    zoom: 14,
    maxBounds: bounds,
    customAttribution: ['<a href=https://www.regenerative-planners.com/ target=_blank>Regenerative Planners</a>']
});


var toggleableLayerIds = [ 'Unprotected Bike Lanes', 'Protected Bike Lanes', 'Proposed Bike Lanes','Accelerated Plan for Safer Streets','Beltline','Scooter Trip Counts' ];
 
var popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
  });


  map.addControl(new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    country: 'us',
    region: 'Georgia',
    bbox:  [-86.010452, 30.537327, -80.771171, 35.210589] ,
}), 'top-right');

var scale = new mapboxgl.ScaleControl({
    maxWidth: 100,
    unit: 'imperial'
});

map.addControl(scale, 'bottom-right');
scale.setUnit('imperial');
map.addControl(new mapboxgl.NavigationControl(), 'top-right');


map.on('load', function() {

  map.addSource('Beltline', {
    'type' : 'geojson',
    'data' : 'data/BeltLine.json' 
  })

  map.addLayer({'id' : 'Beltline',
    'type' : 'line',
    'source': 'Beltline', 
    'layout': {
      'visibility': 'none'
      },
    'paint' : {
      'line-color':'#5cb477',
      'line-opacity':1.0 
    }
  })


  map.addSource('Accelerated Plan for Safer Streets', {
    'type' : 'geojson',
    'data' : 'data/AcceleratedPlanforSaferStreets.json' 
  })

  map.addLayer({'id' : 'Accelerated Plan for Safer Streets',
    'type' : 'line',
    'source': 'Accelerated Plan for Safer Streets', 
    'layout': {
      'visibility': 'none'
      },
    'paint' : {
      'line-color':'#3aaed8',
      'line-opacity':1.0 
    }
  })

  



  map.addSource('Proposed Bike Lanes', {
    'type' : 'geojson',
    'data' : 'data/ProposedLanes.json' 
  })

  map.addLayer({'id' : 'Proposed Bike Lanes',
    'type' : 'line',
    'source': 'Proposed Bike Lanes', 
    'layout': {
      'visibility': 'none'
      },
    'paint' : {
      'line-color':'#e31a1c',
      'line-opacity':1.0,
      'line-width' : 2
    }
  })

  
  map.addSource('Protected Bike Lanes', {
    'type' : 'geojson',
    'data' : 'data/ProtectedBikeLane.json' 
  })

  map.addLayer({'id' : 'Protected Bike Lanes',
    'type' : 'line',
    'source': 'Protected Bike Lanes', 
    'layout': {
      'visibility': 'none'
      },
    'paint' : {
      'line-color':'#757575',
      'line-opacity':1.0
    }
  })

    map.addSource('Unprotected Bike Lanes', {
    'type' : 'geojson',
    'data' : 'data/UnprotectedBikeLane.json' 
  })

  map.addLayer({'id' : 'Unprotected Bike Lanes',
    'type' : 'line',
    'source': 'Unprotected Bike Lanes', 
    'layout': {
      'visibility': 'none'
      },
    'paint' : {
      'line-color':'#fdbf6f',
      'line-opacity':1.0, 
    }
  })

  
  map.addSource('Scooter Trip Counts', {
    'type' : 'geojson',
    'data' : 'data/atl-scooter-counts.geojson' 
  })

  map.addLayer({'id' : 'Scooter Trip Counts',
    'type' : 'line',
    'source': 'Scooter Trip Counts', 
    'paint' : {
      'line-color': 'white',
      'line-opacity':0.0, 
      'line-width' : 2
    }
  })
});


for (var i = 0; i < toggleableLayerIds.length; i++) {
  var id = toggleableLayerIds[i];
  
  var link = document.createElement('a');
  link.href = '#';
  link.className = 'active';
  link.textContent = id;
  
  link.onclick = function (e) {
    var clickedLayer = this.textContent;
    e.preventDefault();
    e.stopPropagation();
    
    var visibility = map.getLayoutProperty(clickedLayer, 'visibility');
    
    if (visibility === 'visible') {
      map.setLayoutProperty(clickedLayer, 'visibility', 'none');
      this.className = '';
    } else {
      this.className = 'active';
      map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
    }
  };
  
  var layers = document.getElementById('menu');
  layers.appendChild(link);
  
}

for (var i = 0; i < toggleableLayerIds.length; i++) {
  var id = toggleableLayerIds[i];
  
  var link = document.createElement('a');
  link.href = '#';
  link.className = 'active';
  link.textContent = id;
  
  link.onclick = function (e) {
    var clickedLayer = this.textContent;
    e.preventDefault();
    e.stopPropagation();
    
    var visibility = map.getLayoutProperty(clickedLayer, 'visibility');
    
    if (visibility === 'visible') {
      map.setLayoutProperty(clickedLayer, 'visibility', 'none');
      this.className = '';
    } else {
      this.className = 'active';
      map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
    }
  };
  
  var layers2 = document.getElementById('menu2');
  layers2.appendChild(link);
  
}


map.on('click','atlScooterCounts', function(e){
  var features = map.queryRenderedFeatures(e.point);
  map.getCanvas().style.cursor = 'pointer';
  

  var description = e.features[0].properties.name;
  var count = e.features[0].properties.SctrCnt;


  popup.setLngLat(e.lngLat)
  .setHTML("<p>Street Name: "+description+"</p>"+"<p>Scooter Count: "+count+"</p>")
  .addTo(map);//
})




})();
