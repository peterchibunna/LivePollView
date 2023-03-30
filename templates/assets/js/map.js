<<<<<<< HEAD
<<<<<<< HEAD
const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });
var center = L.latLng(9.14006268023974, 9.041748046875002);

const map = L.map("map", {
	layers: [layer],
	zoom: 7,
	center: center,
});
document.addEventListener('DOMContentLoaded', function () {
	fetch('/api/v1/state/?limit=50').then(response=>response.json()).then(function (response) {
		console.log(response.objects);
		var states = response.objects;
		for (var i = 0; i < states.length; i++) {
			marker = new L.marker([states[i].location.coordinates[0], states[i].location.coordinates[1]])
				.bindPopup(states[i].name)
				.addTo(map);
			marker.on('click', function (e) {
				alert("Test click on marker");
			})
		}
	});
});

//map.fitWorld();
=======
=======
<<<<<<< HEAD
>>>>>>> 257c758 (Feat: update te django FW)
=======
>>>>>>> 257c758c56f055315cb141d7aecc0fc5cd2e7200
>>>>>>> 1d7f2d655ca1101ea3263e7527726639a9168e7e
const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [layer] });
map.fitWorld();
<<<<<<< HEAD
>>>>>>> 257c758 (Feat: update te django FW)
=======
<<<<<<< HEAD
>>>>>>> 257c758 (Feat: update te django FW)
=======
>>>>>>> 257c758c56f055315cb141d7aecc0fc5cd2e7200
>>>>>>> 1d7f2d655ca1101ea3263e7527726639a9168e7e
