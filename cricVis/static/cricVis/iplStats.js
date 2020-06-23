google.charts.load("current", {packages: ['corechart', 'bar', 'geochart']});
google.charts.setOnLoadCallback(drawChart);
var allChartData;

function getColour(key){
  if (key in allChartData["teamColour"]) return "color: " + allChartData["teamColour"][key];
  return "color: #FFBE7D";
}

function convertDataToMatrix(data,headers){
  let matrixData = []
  headers.push({ role: "style" });
  matrixData.push(headers);
  for (let xAxis in data){
    if (typeof(data[xAxis]) === "object"){
      let key = Object.keys(data[xAxis]);
      let colour = getColour(key[0]);
      matrixData.push([xAxis, data[xAxis][key[0]], key[0], colour]);
    }
    else {
      let colour = getColour(xAxis);
      matrixData.push([xAxis, data[xAxis], colour]);
    }
  }
  return matrixData;
}

function createDataPacket(chartData, chartHeaders, chartTitle, chartSubTitle, chartXAxisTitle, chartYAxisTitle){
  let data = {};
  data["chartData"] = chartData;
  data["headers"] = chartHeaders;
  data["chartTitle"] = chartTitle;
  data["chartSubTitle"] = chartSubTitle;
  data["chartXAxisTitle"] = chartXAxisTitle;
  data["chartYAxisTitle"] = chartYAxisTitle;
  return data;
}

function generateChartData(data,headers){
  let matrixData = convertDataToMatrix(data,headers);
  console.log(matrixData);
  let chartdata = google.visualization.arrayToDataTable(matrixData);
  return chartdata;
}

function generateOptions(chartTitle,chartSubtitle,chartXAxisTitle,chartYAxisTitle,chartWidth=900,chartHeight=300){
  let options = {
    title: chartTitle,
    subtitle: chartSubtitle,
    hAxis: {
      title: chartXAxisTitle,
    },
    vAxis: {
      title: chartYAxisTitle,
    },
    width: chartWidth,
    height: chartHeight,
    legend: {
      position: 'none'
    },
  }
  return options;
}

function plotBarChart(data, chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  chartOptions["bars"] = 'horizontal';
  var chart = new google.visualization.BarChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotColumnChart(data, chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  var chart = new google.visualization.ColumnChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotPieChart(data,chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  chartOptions["pieHole"] = 0.5;
  chartOptions["pieSliceText"] = 'label';
  var chart = new google.visualization.PieChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotBubbleChart(data,chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  var chart = new google.visualization.BubbleChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotLineChart(data,chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  var chart = new google.visualization.LineChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotGeoChart(data,chartDivID){
  let chartData = generateChartData(data["chartData"],data["headers"]);
  let chartOptions = generateOptions(data["chartTitle"],data["chartSubTitle"],data["chartXAxisTitle"],data["chartYAxisTitle"]);
  var chart = new google.visualization.GeoChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotMostWinsChart(chartData){
  let data = createDataPacket(chartData,["Winning Team","Number of Match Wins"],"Most Winning IPL Teams","Number of match wins by every IPL team","Number of Match Wins","Winning Team");
  plotBarChart(data, "mostMatchWins")
}

function plotMostTossWinsChart(chartData){
  let data = createDataPacket(chartData,["Winning Team","Number of Toss Wins"],"Most Toss Winning IPL Teams","Number of toss wins by every IPL team","Number of Toss Wins","Winning Team");
  plotBarChart(data, "mostTossWins");
}

function plotMostSeasonWinsChart(chartData){
  let data = createDataPacket(chartData,["Winning Team","Number of Season Wins"],"Most Season Winning IPL Teams","Number of season wins by every IPL team","Most Season Winning IPL Teams","Number of season wins by every IPL team","Number of Season Wins","Winning Team");
  plotBarChart(data, "mostSeasonWins");
}

function plotAverageScoreChart(chartData){
  let data = createDataPacket(chartData,["Team","Average Score"],"Average Score of IPL Teams","Average Score of every IPL team over all seasons","Team","Average Score");
  plotPieChart(data, "averageScore");
}

function plotFinalScoreBatFirstChart(chartData){
  let data = createDataPacket(chartData,["Team","Final Match Score", { type: "string", role: "annotation" }],"Final Match Score of IPL Teams - Bat First","Total scored by the team which batted first in the final of the season","Team","Final Match Score");
  plotColumnChart(data, "finalScoreBatFirst");
}

function plotMatchesStadiumChart(chartData){
  let data = createDataPacket(chartData,["Stadium","Number of Matches"],"Number of IPL Matches per stadium","A stadium wise distribution of IPL matches","Stadium","Number of Matches");
  plotColumnChart(data, "mostMatchesStadiumWise");
}

function plotMatchesCityChart(chartData){
  let data = createDataPacket(chartData,["City","Number of Matches"],"Number of IPL Matches per city","A city wise distribution of IPL matches","City","Number of Matches");
  plotGeoChart(data, "mostMatchesCityWise");
}

function plotScoreTeams(chartData, scoreType, scoreTypeDiv){
  for (let team in chartData){
    let data = createDataPacket(chartData[team],["Season",`${scoreType} Score`],`${scoreType} Score of ${team} over all seasons`,`Per Season ${scoreType} total`,"Season",`${scoreType} Score`);
    let perTeamDiv = document.createElement("div");
    perTeamDiv.id = `${team}${scoreType}Score`;
    document.getElementById(scoreTypeDiv).appendChild(perTeamDiv);
    plotLineChart(data, perTeamDiv.id);
  }
}

function drawChart(){
  plotMostWinsChart(allChartData["teamWins"]);
  plotMostTossWinsChart(allChartData["tossWinsTeams"]);
  plotMostSeasonWinsChart(allChartData["seasonsWinsTeams"]);
  plotAverageScoreChart(allChartData["averageScoreTeams"]);
  plotFinalScoreBatFirstChart(allChartData["finalScoreBatFirst"]);
  plotScoreTeams(allChartData["lowestScoreTeams"],"Lowest","lowestScoreSeasonWise");
  plotScoreTeams(allChartData["highestScoreTeams"],"Highest","highestScoreSeasonWise");
  plotMatchesStadiumChart(allChartData["gamesPlayedStadium"]);
}

function receiveData(allIPLData){
  allChartData = allIPLData;
}