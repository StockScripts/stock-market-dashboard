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

var createSVG = function(stats, attribute) {
	var STARTING = 100, ENDING = 2900;
	var stats = JSON.parse(stats);
	var width = (ENDING - STARTING) / 25;
	var COORDS = [];
	var current = 100;
	var sorted_keys = Object.keys(stats).sort(function(a, b) {
		return parseInt(a) - parseInt(b);
	});
	var maxAttr = stats[sorted_keys[0]][attribute];
	var minAttr = maxAttr;
	for (var i = 1; i < 25; i++) {
		var temp = stats[sorted_keys[i]][attribute];
		if (temp > maxAttr) {
			maxAttr = temp;
		}
		if (temp < minAttr) {
			minAttr = temp;
		}
	}
	var step = (maxAttr - minAttr) / 10.0, ystepval = maxAttr;
	for (var a = 0; a < 10; a++) {
		document.getElementById('stocksvg').innerHTML += `
			<text x="20" y="${100 + a * 160}" style="fill: black;">
				${ystepval.toFixed(2)}
			</text>
		`;
		ystepval -= step;
	}
	var scaleY = d3.scaleLinear().domain([minAttr - 100, maxAttr]).range([0, 1600]);
	for (var i = 0; i < 25; i++) {
		COORDS.push({
			'horizontal': [current + 25, current + width],
			'attribute': scaleY(stats[sorted_keys[i]][attribute]),
			'timestamp': stats[sorted_keys[i]]['timestamp'],
		});
		current += width;
	}
	for (var i = 0; i < COORDS.length; i++) {
		document.getElementById('stocksvg').innerHTML += `
			<rect
				x="${COORDS[i]['horizontal'][0]}"
				y="${1700 - COORDS[i]['attribute']}"
				width="${width - 25}"
				height="${COORDS[i]['attribute']}"
				title="${COORDS[i]['attribute']}"
				style="fill: #303f9f;"
				data-tooltip="${stats[sorted_keys[i]][attribute]} at ${COORDS[i]['timestamp']}"
			/>
			<text x="${COORDS[i]['horizontal'][0]}" y="1750" style="fill: black;">
				<tspan x="${COORDS[i]['horizontal'][0]}" y="1750">${COORDS[i]['timestamp'].split('T')[0]}</tspan>
				<tspan x="${COORDS[i]['horizontal'][0]}" y="1770">${COORDS[i]['timestamp'].split('T')[1]}</tspan>
			</text>
		`;
	}
	$('rect').hover(function() {
		var string = $(this).attr('data-tooltip').split(' at ');
		$('#x-val').html(parseFloat(string[0]).toFixed(2));
		$('#y-val').html(string[1]);
	}, function() {
		$('#x-val').html('<i>hover over graph</i>');
		$('#y-val').html('<i>hover over graph</i>');
	});
};
