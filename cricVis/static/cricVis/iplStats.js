google.charts.load("current", {packages: ['corechart', 'bar', 'geochart']});
google.charts.setOnLoadCallback(drawIPLCharts);
var allChartData;

$('.carousel').carousel({
  interval: false,
});

// get the colour of bar corresponding to the team

function getColour(key){
  if (key in allChartData["teamColour"]) return "color: " + allChartData["teamColour"][key];
  return "color: #FFBE7D";
}

// convert the chart data to matrix for Google Charts API format

function convertDataToMatrix(data,headers, color=null){
  let matrixData = []
  headers.push({ role: "style" });
  matrixData.push(headers);
  Object.keys(data).forEach((xAxis) => {
    if (typeof(data[xAxis]) === "object"){
      const key = Object.keys(data[xAxis]);
      if (!color) colour = getColour(key[0]);
      matrixData.push([xAxis, data[xAxis][key[0]], key[0], colour]);
    }
    else {
      if (!color) colour = getColour(xAxis);
      matrixData.push([xAxis, data[xAxis], colour]);
    }
  });
  return matrixData;
}

// generate chart data to be used in plotting chart using Google Charts format

function generateChartData(data,headers, color=null){
  const matrixData = convertDataToMatrix(data,headers, color);
  const chartdata = google.visualization.arrayToDataTable(matrixData);
  return chartdata;
}

// generate some fixed and some parameterized charting options for a graph

function generateOptions(chartTitle,chartSubtitle,chartXAxisTitle,chartYAxisTitle){
  let options = {
    title: chartTitle,
    subtitle: chartSubtitle,
    hAxis: {
      title: chartXAxisTitle,
    },
    vAxis: {
      title: chartYAxisTitle,
    },
    width: 900,
    height: 600,
    legend: {
      position: 'none'
    },
  }
  return options;
}

function plotBarChart(chartData, chartOptions, chartDivID){
  chartOptions["bars"] = 'horizontal';
  const chart = new google.visualization.BarChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotColumnChart(chartData, chartOptions, chartDivID){
  const chart = new google.visualization.ColumnChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotPieChart(chartData, chartOptions ,chartDivID){
  chartOptions["pieSliceText"] = 'label';
  const chart = new google.visualization.PieChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotBubbleChart(chartData, chartOptions ,chartDivID){
  const chart = new google.visualization.BubbleChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

function plotLineChart(chartData, chartOptions ,chartDivID){
  const chart = new google.visualization.LineChart(document.getElementById(chartDivID));
  chart.draw(chartData, chartOptions);
}

// plot the graph for most wins by a team

function plotMostWinsChart(chartData){
  const data = generateChartData(chartData,["Winning Team","Number of Match Wins"]); 
    let chartOptions = generateOptions("Most Winning IPL Teams","Number of match wins by every IPL team","Number of Match Wins","Winning Team");
  plotBarChart(data, chartOptions, "mostMatchWins")
}

// plot the graph for the number of tosses won by a team

function plotMostTossWinsChart(chartData){
  const data = generateChartData(chartData,["Winning Team","Number of Toss Wins"]); 
  let chartOptions = generateOptions("Most Toss Winning IPL Teams","Number of toss wins by every IPL team","Number of Toss Wins","Winning Team");
  plotBarChart(data, chartOptions, "mostTossWins");
}

// plot the graph for number of seasons won by a team

function plotMostSeasonWinsChart(chartData){
  const data = generateChartData(chartData,["Winning Team","Number of Season Wins"]);
  let chartOptions = generateOptions("Most Season Winning IPL Teams","Number of season wins by every IPL team","Most Season Winning IPL Teams","Number of season wins by every IPL team","Number of Season Wins","Winning Team");
  plotBarChart(data, chartOptions, "mostSeasonWins");
}

// plot the graph for average score of a team throughout the tournament

function plotAverageScoreChart(chartData){
  const data = generateChartData(chartData,["Team","Average Score"]);
  let chartOptions = generateOptions("Average Score of IPL Teams","Average Score of every IPL team over all seasons","Team","Average Score");
  plotColumnChart(data, chartOptions, "averageScore");
}

// plot the graph for the score of the team which batted first in a season final

function plotFinalScoreBatFirstChart(chartData){
  const data = generateChartData(chartData,["Team","Final Match Score", { type: "string", role: "annotation" }]);
  let chartOptions = generateOptions("Final Match Score of IPL Teams - Bat First","Total scored by the team which batted first in the final of the season","Team","Final Match Score");
  plotColumnChart(data, chartOptions, "finalScoreBatFirst");
}

// plot the number of matches held in each stadium

function plotMatchesStadiumChart(chartData){
  const data = generateChartData(chartData,["Stadium","Number of Matches"]);
  let chartOptions = generateOptions("Number of IPL Matches per stadium","A stadium wise distribution of IPL matches","Stadium","Number of Matches");
  plotColumnChart(data, chartOptions, "mostMatchesStadiumWise");
}

// plot the lowest/highest score of every team throughout all the seasons

function plotScoreTeams(chartData, scoreType, scoreTypeDiv){
  let flag = true;
  for (const team in chartData){
    const data = generateChartData(chartData[team],["Season",`${scoreType} Score`], allChartData["teamColour"][team]);
    let chartOptions = generateOptions(`${scoreType} Score of ${team} over all seasons`,`Per Season ${scoreType} total`,"Season",`${scoreType} Score`);
    chartOptions.height = 200;
    const perTeamDiv = document.createElement("div");
    perTeamDiv.id = `${team}${scoreType}Score`;
    if (flag) {
      perTeamDiv.classList.add("carousel-item");
      perTeamDiv.classList.add("active");
      flag = false;
    }
    else perTeamDiv.classList.add("carousel-item");
    document.getElementById(scoreTypeDiv).appendChild(perTeamDiv);
    plotLineChart(data, chartOptions, perTeamDiv.id);
  }
}

// draw all the above statistics 

function drawIPLCharts(){
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