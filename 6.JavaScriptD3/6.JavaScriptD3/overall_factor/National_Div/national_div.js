var margin = { left:100, right:10, top:10, bottom:150 };

var width = 800 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height",height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left 
            + ", " + margin.top + ")");

g.append("text")
    .attr("class","x-axis lable")
    .attr("x", width / 3.2)
    .attr("y", height + 140)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Performance")

g.append("text")
    .attr("class","y-axis lable")
    .attr("x", -(height / 1.5))
    .attr("y", -40)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("National Diversity");

var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "National Diversity： <span style='color:red'>" + d.national_div + "</span><br>";   
        text += "Performance： <span style='color:red'>" + d3.format(".2f")(d.performance) + "</span><br>";
        return text;
    });
g.call(tip);

d3.json("visual_data/nation_div_new.json").then(function(data){
    console.log(data)  
    data.forEach(function(d){
        d.national_div = +d.national_div;
        d.performance = +d.performance;
    })
    var xScale = d3.scaleLinear()
        .domain([0,d3.max(data,function(d){
            return d.national_div;
        })])
        .range([0, 400]);
    
    var yScale = d3.scaleLinear()
        .domain([d3.max(data,function(d){
            return d.performance;
        }),0])
        .range([0, 200]);

    var xAxisCall = d3.axisBottom(xScale)
                        .ticks(5)
                        .tickFormat(function(d){
                            return d
                        });


    g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + 210 + ")")
        .call(xAxisCall)
    .selectAll("text")
        .attr("y", "10")
        .attr("x", "-5")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-40)");


    var yAxisCall = d3.axisRight(yScale)
                    .ticks(5)
                    .tickFormat(function(d){
                        return d ;
                    });

    g.append("g")
        .attr("class", "y-axis")
        .call(yAxisCall);
      
    
    var line = d3.line()
        .x(function(d) {
            return xScale(d.national_div);
        })
        .y(function(d) {
            return yScale(d.performance);
        })

    g.append('path')
        .attr('class', 'line')
        .attr('d', line(data))
        .attr('fill', 'none')
        .attr('stroke-width', 1)
        .attr('stroke', 'black');

    var circles = g.selectAll("circle")
        .data(data)
        circles.enter()
        .append("circle")
            .attr("fill", "red")
            .attr("cx",function(d){
                return xScale(d.national_div);
            })
            .attr("cy",function(d){
                return yScale(d.performance);
            })
            .attr("r", 2)
            .on("mouseover",tip.show)
            .on("mouseout",tip.hide)
})