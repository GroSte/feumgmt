/**
 * Created by steve on 10.06.2016.
 */

function initMap(mapId, lat, long, text) {
    var mymap = L.map(mapId).setView([lat, long], 18);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
        maxZoom: 20,
        id: 'mapbox.streets'
    }).addTo(mymap);

    var marker = L.marker([lat, long]).addTo(mymap);
    marker.bindPopup(text).openPopup();
}
