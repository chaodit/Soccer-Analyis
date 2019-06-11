var margin = { left:100, right:10, top:10, bottom:135 };

var width = 800 - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height",height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left 
            + ", " + margin.top + ")");

var formattedData;
var season = 0;
var max_goal;

var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "Club： <span style='color:red'>" + d.club + "</span><br>";   
        text += "Total Goals： <span style='color:red'>" + d3.format(".2f")(d.total_goals) + "</span><br>";
        text += "Market Value： <span style='color:red'>" + d3.format(".2f")(d.total_market_value / 1000000) + "Million </span><br>";
        return text;
    });
g.call(tip);

var xScale = d3.scaleBand()
        .range([0, width * 3 / 4])
        .paddingInner(0.3)
        .paddingOuter(0.3);
var yScale = d3.scaleLinear()
            .domain([50,650])
            .range([0, height]);

var yaxisScale = d3.scaleLinear()
                .domain([650,50])
                .range([0, height]);

var yAxisCall = d3.axisRight(yaxisScale)
            .ticks(5)
                .tickFormat(function(d){
                    return d ;
                });


var xAxisCall = d3.axisBottom()
        .ticks(20)
            
var xAxis = g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + 420 + ")") 

g.append("g")
.attr("class", "y-axis")
.attr("transform","translate(-20," + 10 + ")")
.call(yAxisCall);
var continentColor = d3.interpolateYlGn;

g.append("text")
    .attr("class","x-axis lable")
    .attr("x", width / 3)
    .attr("y", height + 130)
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .text("Club Name")

g.append("text")
    .attr("class","y-axis lable")
    .attr("x", -(height / 2))
    .attr("y", -40)
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Club Market Value (Million)");

var seasonLabel = g.append("text")
    .attr("y", height -10)
    .attr("x", width - 20)
    .attr("font-size", "20px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text("2015");

var goals = ["Most", "Least"];

var legend = g.append("g")
    .attr("transform", "translate(" + (width - 10) + 
        "," + (height - 125) + ")");

var legendLeast = legend.append("g")
    .attr("transform", "translate(0, " + (20) + ")");
    legendLeast.append("circle")
        .attr("cy", 10)
        .attr("cx", 10)
        .attr("r", 8)
        .attr("fill", continentColor(0.2));
    legendLeast.append("text")
        .attr("x", -10)
        .attr("y", 10)
        .attr("text-anchor", "end")
        .style("text-transform", "capitalize")
        .text("Goal Least");

var legendMost = legend.append("g")
    .attr("transform", "translate(0, " + (40) + ")");
    legendMost.append("circle")
        .attr("cy", 10)
        .attr("cx", 10)
        .attr("r", 8)
        .attr("fill", continentColor(1));
    legendMost.append("text")
        .attr("x", -10)
        .attr("y", 10)
        .attr("text-anchor", "end")
        .style("text-transform", "capitalize")
        .text("Goal Most");

d3.json("http://18.191.239.122/wordpress/wp-content/uploads/2019/06/team_all_season_all_info_new.json").then(function(data){

    formattedData = data.map(function(season){
        return season["info"].filter(function(info){
            var dataExists = (info.total_goals && info.club);
            return dataExists
        }).map(function(info){
            info.total_market_value = +info.total_market_value;
            info.total_goals = +info.total_goals;
            return info;            
        })
    });
    max_goal = d3.max(formattedData[0],function(d){
        return d.total_goals;
    });
    update(formattedData[0]);
})


$("#season-select")
    .on("change", function(){
        update(formattedData[0]);
    })

function update(data) {
    // Standard transition time for the visualization

    var year = $("#season-select").val();

    var data = data.filter(function(d){
        return d.year == year;  
    })

    xScale.domain(data.map(function(d){ 
        return d.club;
    }));

    xAxisCall.scale(xScale);
    xAxis.call(xAxisCall.tickFormat(function(d){return d;}))
        .selectAll("text")
            .attr("y", "10")
            .attr("x", "-5")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-40)");

    g.selectAll("rect")
        .remove()        
    var rects = g.selectAll("rect")
        .data(data,function(d){
            return d;
        })

    rects.enter()
        .append("rect")
        .attr("class", "enter")
        .attr("y",function(d){
            return 550 -  margin.bottom - yScale(d.total_market_value / 1000000);
        })
        .attr("x", function(d){ return xScale(d.club); })
        .attr("width", 10)
        .attr("height", function(d){ return yScale(d.total_market_value / 1000000)})
        .attr("fill",function(d){
            return d3.interpolateYlGn(d.total_goals / max_goal);
        })
        .on("mouseover",tip.show)
        .on("mouseout",tip.hide)
    
    seasonLabel.text(year)
}