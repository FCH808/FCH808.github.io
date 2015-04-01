

d3.csv("data/nobel_ages.csv", function (data) {
	
	var map = data.map(function (i) {
		return parseInt(i.age);
	});

	var width = 800,
		height = 550,
		padding = 50;	

	var histogram = d3.layout.histogram()
		.bins(30)
		(map)

	var y = d3.scale.linear()
		.domain([0, d3.max(histogram.map(function(i) {return i.length; }))])
		.range([0, height]);

	var x = d3.scale.linear()
		.domain([0, d3.max(map)])
		.range([0, width])

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom")
		.ticks(20)

	var canvas = d3.select("body").append("svg")
		.attr("width", width)
		.attr("height", height + padding)
		.append("g")
			.attr("transform", "translate(20, 0)")

	var group = canvas.append("g")
		.attr("transform", "translate(0, " + height + ")")
		.call(xAxis)

	var bars = canvas.selectAll('.bar')
		.data(histogram)
		.enter()
		.append("g")

	bars.append("rect")
		.attr("x", function(d) {return x(d.x);})
		.attr("y", function(d) {return height - y(d.y); })
		.attr("width", function(d) {return x(d.dx); })
		.attr("height", function(d) {return y(d.y); })
		.attr("fill", "steelblue")

	bars.append("text")
		.attr("x", function(d) {return x(d.x)})
		.attr("y", function(d) {return height - y(d.y); })
		.attr("dy", "20px")
		.attr("dx", function (d) {return x(d.dx)/2; })
		.attr("font-size", "50%")
		.attr("fill", "#fff")
		.attr("text-anchor", "middle")
		.text(function (d) { return d.y;} )

})

var map = new Datamap({element: document.getElementById('container')});