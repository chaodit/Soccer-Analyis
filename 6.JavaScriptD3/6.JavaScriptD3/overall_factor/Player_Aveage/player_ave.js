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
    .attr("x", width / 3)
    .attr("y", height + 140)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Player Average Age")

g.append("text")
    .attr("class","y-axis lable")
    .attr("x", -(height / 2))
    .attr("y", -20)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Performance");

var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "Player Average Age： <span style='color:red'>" + d.ave_age + "</span><br>";   
        text += "Performance： <span style='color:red'>" + d3.format(".2f")(d.performance) + "</span><br>";
        return text;
    });
g.call(tip);

d3.json("visual_data/player_aveage_new.json").then(function(data){
    console.log(data)  
    data.forEach(function(d){
        d.ave_age = +d.ave_age;
        d.performance = +d.performance;
    })
    var xScale = d3.scaleLinear()
        .domain([18,d3.max(data,function(d){
            return d.ave_age;
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
            return xScale(d.ave_age);
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
                return xScale(d.ave_age);
            })
            .attr("cy",function(d){
                return yScale(d.performance);
            })
            .attr("r", 2)
            .on("mouseover",tip.show)
            .on("mouseout",tip.hide)
})