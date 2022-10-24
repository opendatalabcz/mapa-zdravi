function getColor(d) {
    //  TODO update palette
    return d > 7  ? '#800026' :
           d > 6  ? '#BD0026' :
           d > 5  ? '#E31A1C' :
           d > 4  ? '#FC4E2A' :
           d > 3  ? '#FD8D3C' :
           d > 2  ? '#FEB24C' :
           d > 1  ? '#FED976' :
                    '#808080'; //'#FFEDA0';
                    
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.value),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

  
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);

}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();


}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}


var map = L.map("map").setView([49.85, 15.0], 8);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

geojson = L.geoJson(regionData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Počet lékařů</h4>' +  (props ?
        '<b>' + props.name + '</b><br/>Náhodně vygenerovaná hodnota: [' + props.value + ']'
        : 'Klikněte na okres');
};

info.addTo(map);


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [1, 2, 3, 4, 5, 6, 7, 'Data nedostupná'], // name
        labels = [];

    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + ((grades[i+2]) || (!grades[i+1]) ? '<br>' : '+<br>');
    }

    return div;
};

legend.addTo(map);
