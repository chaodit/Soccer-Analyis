var margin = { left:80, right:100, top:30, bottom:30 };
var height = 450 - margin.top - margin.bottom;
var width = 800 - margin.left - margin.right;
var g = d3.select("#line-area")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + 
            ", " + margin.top + ")");

// var color = d3.scaleOrdinal(d3.schemeDark2);
g.append("text")
    .attr("class","x-axis lable")
    .attr("x", width / 3)
    .attr("y", height + 20)
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .text("Total Conceded Goals")

g.append("text")
    .attr("class","y-axis lable")
    .attr("x", -(height / 2))
    .attr("y", -40)
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Total Goals");

var seasonLabel = g.append("text")
    .attr("y", height -80)
    .attr("x", width - 80)
    .attr("font-size", "20px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text("2015");
var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        console.log(d)
        var text = "Club： <span style='color:red'>" + d.club + "</span><br>";   
        text += "Total Goals： <span style='color:red'>" + d.total_goals + "</span><br>";
        text += "Total Conceded Goals： <span style='color:red'>" + d.conceded_goal + "</span><br>";
        return text;
});
g.call(tip);

var xScale = d3.scaleLinear()
        .domain([25,85])
        .range([0, width * 3 / 4])
var yScale = d3.scaleLinear()
            .domain([20,110])
            .range([0, height * 3 / 4]);      
var yaxisScale = d3.scaleLinear()
                .domain([110,20])
                .range([0, height * 3 / 4]);
var yAxisCall = d3.axisRight(yaxisScale)
            .ticks(5)
                .tickFormat(function(d){
                    return d ;
                });
var xAxisCall = d3.axisBottom(xScale)
                .ticks(20)
                .tickFormat(function(d){
                    return d;
                });                  
var xAxis = g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(-15, " + 315 + ")") 
        .call(xAxisCall)
        .selectAll("text")
            .attr("y", "10")
            .attr("x", "-5")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-40)");
g.append("g")
    .attr("class", "y-axis")
    .attr("transform","translate(-16," + 15 + ")")
    .call(yAxisCall);
var color = d3.scaleOrdinal()
    .range(d3.schemeCategory10);

var LinePath = d3.line()
                .x(function(d){
                    return xScale(d.conceded_goal);
                })
                .y(function(d){
                    return 450 * 3 / 4 -  margin.bottom - yScale(d.total_goals);
                })

// pie Chart Area

var margin2 = { left:0, right:0, top:40, bottom:0 };
var width2 = 250 - margin2.left - margin2.right,
    height2 = 250 - margin2.top - margin2.bottom,
    radius = Math.min(width2, height2) / 2;

var pie = d3.pie()
		.padAngle(0.03)
		.value(function(d) { return d.total_goals; })
        .sort(null);
        
var varc = d3.arc()
    .innerRadius(radius - 60)
    .outerRadius(radius - 30);
    
var svg2 = d3.select("#club-area1")
    .append("svg")
    .attr("width", width2 + margin2.left + margin2.right)
    .attr("height", height2 + margin2.top + margin2.bottom);

var g2 = svg2.append("g")
    .attr("transform", "translate(" + (margin2.left + (width2 / 2)) + 
        ", " + (margin2.top + (height2 / 2)) + ")");

g2.append("text")
    .attr("y", -height2/2)
    .attr("x", -width2/2)
    .attr("font-size", "15px")
    .attr("text-anchor", "start")
    .text("Season Goals");

var tip2 = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "Season： <span style='color:red'>" + d.data.year + "</span><br>";   
        text += "Total Goals： <span style='color:red'>" + d.data.total_goals + "</span><br>";
        return text;
});
g2.call(tip2)

//pie chart area 2
var svg3 = d3.select("#club-area2")
    .append("svg")
    .attr("width", width2 + margin2.left + margin2.right)
    .attr("height", height2 + margin2.top + margin2.bottom);

var g3 = svg3.append("g")
    .attr("transform", "translate(" + (margin2.left + (width2 / 2)) + 
        ", " + (margin2.top + (height2 / 2)) + ")");
var pie2 = d3.pie()
    .padAngle(0.03)
    .value(function(d) { return d.conceded_goal; })
    .sort(null);

g3.append("text")
    .attr("y", -height2/2)
    .attr("x", -width2/2)
    .attr("font-size", "15px")
    .attr("text-anchor", "start")
    .text("Season Conceded Goals");


var tip3 = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "Season： <span style='color:red'>" + d.data.year + "</span><br>";   
        text += "Total Conceded Goals： <span style='color:red'>" + d.data.conceded_goal + "</span><br>";
        return text;
});
g3.call(tip3)

d3.json("http://18.191.239.122/wordpress/wp-content/uploads/2019/06/team_all_season_all_info.json").then(function(data){
    // Prepare and clean data
    formattedData = data.map(function(season){
        return season["info"].filter(function(info){
            var dataExists = (info.total_goals && info.club);
            return dataExists
        }).map(function(info){
            info.total_goals = +info.total_goals;
            info.conceded_goal = + info.conceded_goal;
            return info;            
        })
    });
    max_goal = d3.max(formattedData[0],function(d){
        return d.total_goals;
    });
    season_changed(formattedData[0]);
})

$("#season-select")
    .on("change", function(){
        g.selectAll("circle").remove();
        season_changed(formattedData[0]);
    })

$("#club-select")
    .on("change", function() { 
        g.selectAll("circle").remove();
        season_changed(formattedData[0])
    })

function season_changed(data) {
        // Standard transition time for the visualization
    
    var year = $("#season-select").val();
    var club = $("#club-select").val();

    var dataseason = data.filter(function(d){
        return d.year == year;
    })

    var clubdata = data.filter(function(d){
        return d.club == club;
    })

    var dataclub = data.filter(function(d){
        if(club == "all"){return true;}
        else{
        return d.year == year && d.club == club;}
    })

    var circles = g.selectAll("circle")
        .data(dataseason,function(d){
            return d;
        }) 
    var l = [{"conceded_goal":25,"total_goals":20},
            {"conceded_goal":dataclub[0].conceded_goal,"total_goals":dataclub[0].total_goals},
            {"conceded_goal":dataclub[0].conceded_goal,"total_goals":20},
            {"conceded_goal":25,"total_goals":20}]

    g.selectAll("path").remove();
    g2.selectAll("path").remove();
    g3.selectAll('path').remove();
    g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(-15, " + 315 + ")") 
        .call(xAxisCall)
        .selectAll("text")
            .attr("y", "10")
            .attr("x", "-5")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-40)");
    g.append("g")
        .attr("class", "y-axis")
        .attr("transform","translate(-16," + 15 + ")")
        .call(yAxisCall);
    if(club != "all"){
        g.append('path')
                .attr('class', 'line')
                .attr('d', LinePath(l))
                .attr('fill', 'green')
                .attr('stroke-width', 1)
                .attr('stroke', 'black');

        var arcs=g2.selectAll("arc") 
                .data(pie(clubdata)) 
                .enter()
                .append("g")
                .attr("class","arc");

        arcs.append("path")
                .attr("fill-opacity",function(d){
                    return (d.data.year == year) ? 1:0.3;})
                .attr("d",varc)
                .style("fill",function(d){return color(d.data.year)})
                .on("mouseover", tip2.show)
                .on("mouseout",tip2.hide);
        
        var arcs2=g3.selectAll("arc") 
                .data(pie2(clubdata)) 
                .enter()
                .append("g")
                .attr("class","arc");

        arcs2.append("path")
                .attr("fill-opacity",function(d){
                    return (d.data.year == year) ? 1:0.3;})
                .attr("d",varc)
                .style("fill",function(d){return color(d.data.year)})
                .on("mouseover", tip3.show)
                .on("mouseout",tip3.hide);
    }

    circles.enter()
        .append("circle")
        // .attr("class", "enter")
        .attr("cy",function(d){
            return 450 * 3 / 4 -  margin.bottom - yScale(d.total_goals);
        })
        .attr("cx", function(d){ return xScale(d.conceded_goal);})
        .attr("r", 8)
        .attr("fill","green")
        .on("mouseover",tip.show)
        .on("mouseout",tip.hide)
    seasonLabel.text(year)
}




