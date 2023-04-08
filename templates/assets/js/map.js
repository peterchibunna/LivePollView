const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors <br>Other Information: <a href=''>Project Details</a>";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });
var center = L.latLng(9.14006268023974, 9.041748046875002);

const map = L.map("map", {
	layers: [layer],
	zoom: 7,
	center: center,
});
document.addEventListener('DOMContentLoaded', function () {
	var myModalEl = document.querySelector('#votesModal');
	var modal = bootstrap.Modal.getOrCreateInstance(myModalEl);
	myModalEl.addEventListener('shown.bs.modal', function (event) {

	});
	fetch('/api/v1/state/?limit=50').then(response=>response.json()).then(function (response) {
		// console.log(response.objects);
		var states = response.objects;
		for (var i = 0; i < states.length; i++) {
			var marker = new L.Marker([states[i].location.coordinates[0], states[i].location.coordinates[1]], {
				radius: 20,
			})
				//.bindPopup(states[i].name)
				.addTo(map);
			let url = states[i].id;
			marker.on('click', function (e) {
				loadInto('get-votes?state_id='+url+'&election_id='+$('#election-types select').val() || 1, '#votesModal');
				modal.show();
			})
		}
	});

	fetch('/api/v1/election').then(response=>response.json()).then(function (response) {
		var data = response.objects;
		var electionTypes = '';
		for (var i = 0; i < data.length; i++) {
			electionTypes += '<option value="'+data[i].id+'">'+data[i].name+'</option>';
		}
		$('#election-types select').html(electionTypes);
	})
});

/** @source https://stackoverflow.com/questions/10585029/parse-an-html-string-with-js#55046067 */
const parseHTML = Range.prototype.createContextualFragment.bind(document.createRange());

const loadInto = function (url, modal) {
	var contentArea = document.querySelector(modal + ' .modal-content');
	new Promise((resolve, reject) => {
		resolve();
	}).then(function () {
		//console.log('1...clearing content...')
		contentArea.innerHTML = '';
	}).then(function () {
		//console.log('2...putting loader content...')
		contentArea.innerHTML = '<div class="modal-body d-flex justify-content-center align-items-center p-5 flex-column"><div class="spinner"><div class="dot1"></div><div class="dot2"></div></div><a href="#" data-bs-dismiss="modal">Cancel</a></div>';
	}).then(function () {
		//console.log('3...putting ajax content...')
		fetch(url, {
			method: 'GET', // *GET, POST, PUT, DELETE, etc.
			mode: 'same-origin', // no-cors, *cors, same-origin
			cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
			credentials: 'same-origin', // include, *same-origin, omit
		})
			.then((response) => response.text())
			.then((html) => {
				contentArea.replaceWith(parseHTML('<div class="modal-content">' + html + '</div>'));
			})
			.catch((error) => {
				console.warn(error);
			}).finally(() => {});

	})
};
//map.fitWorld();
