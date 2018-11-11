String.prototype.replaceAll = function(search, replacement) {
	var target = this;
	return target.split(search).join(replacement);
};

var changeDropdown = function(data) {
	var data = JSON.parse(data);
	for (var item = 0; item < Object.keys(data).length; item++) {
		var presentHTML = $('#dropdown1').html();
		document.getElementById('dropdown1').innerHTML
		= presentHTML + `<li tabindex="${item}"><a id="item-${item}">${data[item]}</a></li>`;
	}
	setTimeout(function() {
		for (var item = 0; item < Object.keys(data).length; item++) {
			var elem = document.querySelector(`#item-${item}`);
			elem.onclick = function() {
				document.querySelector('input#search')['value'] = this.innerHTML;
			};
		}
	}, 200);
	$('.dropdown-trigger').dropdown({
		coverTrigger: false,
		onOpenStart: function() {
			setTimeout(function() {
				$('input#search').focus();
			}, 500);
		},
	});
};
