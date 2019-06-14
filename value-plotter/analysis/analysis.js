

$( document ).ready(function() {
	/* when running on server, will want to implement this
	d3.json("./responses/2019-06-14/2:33:18.json", function(error, data) {
		console.log(data);
	});
	*/

	const data = JSON.parse('{"comparison":{"Love":["Curiosity","Adventure","Wisdom","Responsibility","Knowledge","Optimism"],"Curiosity":["Knowledge"],"Authenticity":["Responsibility","Curiosity","Optimism","Love","Adventure","Wisdom","Knowledge"],"Responsibility":["Curiosity","Knowledge","Optimism"],"Adventure":["Curiosity","Knowledge","Responsibility","Optimism"],"Optimism":["Curiosity","Knowledge"],"Wisdom":["Responsibility","Curiosity","Optimism","Knowledge","Adventure"]},"dragged":["Love","Knowledge","Optimism","Responsibility","Curiosity","Adventure","Authenticity","Wisdom"],"first_sending":"true"}')["comparison"];
	const dataset = {
		nodes: [],
		edges: []
	};

	const keys = Object.keys(data);
	let temp_nodes = [];
	let node_dict = {};

	// Create nodes
	for (let i = 0; i < keys.length; i++) {
		const children = data[keys[i]];
		for (let j = 0; j < children.length; j++) {
			if (!temp_nodes.includes(children[j])) {
				temp_nodes.push(children[j]);
				dataset.nodes.push({name:children[j]});
			}
		}
		if (!temp_nodes.includes(keys[i])) {
			temp_nodes.push(keys[i]);
			dataset.nodes.push({name:keys[i]});
		}
	}

	for (let i = 0; i < keys.length; i++) {
		const children = data[keys[i]];
		for (let j = 0; j < children.length; j++) {
			dataset.edges.push({source:temp_nodes.indexOf(keys[i]), target:temp_nodes.indexOf(children[j])});
		}
	}


	console.log(dataset);
	const width = window.innerWidth / 2;
	const height = window.innerHeight;

	const svg = d3.select('svg')
		.attr('width', width)
		.attr('height', height)

	let force = d3.forceSimulation(dataset.nodes)
		.force("charge", d3.forceManyBody().strength(-300))
		.force("link", d3.forceLink(dataset.edges).strength(0.05))
		.force("center", d3.forceCenter().x(width/2).y(height/2));

	let edges = svg.selectAll("line")
		.data(dataset.edges)
		.enter()
		.append("line")
		.style("stroke", "#ff5555")
		.style("stroke-width", 2);

	let nodes = svg.selectAll("circle")
		.data(dataset.nodes)
		.enter()
		.append("circle")
		.attr("r", 10)
		.style("fill", "#aaaaaa")
		.call(d3.drag().on("start", dragStart)
			.on("drag", dragging)
			.on("end", dragEnd));

	let text = svg.selectAll('text')
		.data(dataset.nodes)
		.enter().append('text')
		.text(node => node.name)
		.attr('font-size', 20)
		.attr('dx', 15)
		.attr('dy', 4);

	function dragStart(d) {
		if (!d3.event.active) force.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	function dragging(d) {
		d.fx = d3.event.x;
		d.fy = d3.event.y;
	}

	function dragEnd(d) {
		if (!d3.event.active) force.alphaTarget(0).restart();
		d.fx = null;
		d.fy = null;
	}

	force.on("tick", function() {
		edges.attr("x1", function(d) {return d.source.x;})
			.attr("y1", function(d) {return d.source.y;})
			.attr("x2", function(d) {return d.target.x;})
			.attr("y2", function(d) {return d.target.y;})

		nodes.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });

		text.attr("x", node => node.x)
			.attr("y", node => node.y);



	
	});

});
