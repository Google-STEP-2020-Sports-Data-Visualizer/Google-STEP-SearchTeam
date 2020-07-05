google.charts.load('current', {'packages':['corechart','bar']});
function plotCharts(chartsData)
{
	createWormChart(chartsData.wormChartData,'WormChartContainer');
	createRunRateChart(chartsData.runRateChartData,'RunRateChartContainer');
	createManhattanChart(chartsData.manhattanChartData,'ManhattanChartContainer');
}

function createWormChart(chartData,containerID) {
	const team1WormChartName = chartData.team1.teamName;
    const team2WormChartName = chartData.team2.teamName;
    let team1CumulativeRunsList = [];
    let team2CumulativeRunsList = [];
    let team1WormChartTooltipList = [];
    let team2WormChartTooltipList = [];
    let team1WormChartPointList = [];
    let team2WormChartPointList = [];

    chartData.team1.overs.forEach((element, index) => {
      team1CumulativeRunsList.push(element.cumulativeRuns);
      team1WormChartTooltipList.push(createTooltip(index+1, team1WormChartName, element.cumulativeRuns, element.playersDismissed));
      if (element.playersDismissed.length) {
        team1WormChartPointList.push(index+1)
      };
    });
    chartData.team2.overs.forEach((element, index) => {
      team2CumulativeRunsList.push(element.cumulativeRuns);
      team2WormChartTooltipList.push(createTooltip(index+1, team2WormChartName, element.cumulativeRuns, element.playersDismissed));
      if (element.playersDismissed.length) {
        team2WormChartPointList.push(index+1)
      };
    });

    createLineChart([team1WormChartName,team2WormChartName],[team1CumulativeRunsList,team2CumulativeRunsList],[team1WormChartTooltipList,team2WormChartTooltipList],[team1WormChartPointList,team2WormChartPointList],'Overs','Worm Chart',containerID);
}

function createRunRateChart(chartData,containerID) {
	const team1RunRateChartName = chartData.team1.teamName;
    const team2RunRateChartName = chartData.team2.teamName;
    let team1RunRateList = [];
    let team2RunRateList = [];
    let team1RunRateChartTooltipList = [];
    let team2RunRateChartTooltipList = [];
    let team1RunRateChartPointList = [];
    let team2RunRateChartPointList = [];

    chartData.team1.overs.forEach((element, index) => {
      team1RunRateList.push(element.runRate);
      team1RunRateChartTooltipList.push(createTooltip(index+1, team1RunRateChartName, element.runRate.toFixed(2), element.playersDismissed));
      if (element.playersDismissed.length) {
        team1RunRateChartPointList.push(index+1)
      };
    });
    chartData.team2.overs.forEach((element, index) => {
      team2RunRateList.push(element.runRate);
      team2RunRateChartTooltipList.push(createTooltip(index+1, team2RunRateChartName, element.runRate.toFixed(2), element.playersDismissed));
      if (element.playersDismissed.length) {
        team2RunRateChartPointList.push(index+1)
      };
    });

    createLineChart([team1RunRateChartName,team2RunRateChartName],[team1RunRateList,team2RunRateList],[team1RunRateChartTooltipList,team2RunRateChartTooltipList],[team1RunRateChartPointList,team2RunRateChartPointList],'Overs','Run Rate Chart',containerID);
}

function createManhattanChart(chartData,containerID) {
	const team1ManhattanChartName = chartData.team1.teamName;
    const team2ManhattanChartName = chartData.team2.teamName;
    let team1RunsList = [];
    let team2RunsList = [];
    let team1ManhattanChartTooltipList = [];
    let team2ManhattanChartTooltipList = [];
    chartData.team1.overs.forEach((element, index) => {
      team1RunsList.push(element.runs);
      team1ManhattanChartTooltipList.push(createTooltipManhattan(index+1, team1ManhattanChartName, element.runs, element.playersDismissed,element.breakdownRuns));
    });
    chartData.team2.overs.forEach((element, index) => {
      team2RunsList.push(element.runs);
      team2ManhattanChartTooltipList.push(createTooltipManhattan(index+1, team2ManhattanChartName, element.runs, element.playersDismissed,element.breakdownRuns));
    });

    createColumnChart([team1ManhattanChartName,team2ManhattanChartName],[team1RunsList,team2RunsList],[team1ManhattanChartTooltipList,team2ManhattanChartTooltipList],'Overs','Manhattan Chart',containerID);
}

function createTruthValueList(list,finalListLength)
{
  let truthValueList = new Array(finalListLength).fill(false);
  list.forEach((element, index) => {
    if ((element-1)<finalListLength) {
      truthValueList[element-1]=true;
    }
  });
  return truthValueList;
}

function createTooltip(overNumber, teamName, value, playersDismissed)
{
  let tooltip=overNumber+'\n'+teamName+': '+value;
  if (playersDismissed.length>0)
  {
  tooltip = tooltip.concat('\nPlayers Dismissed:');
  playersDismissed.forEach((player) =>  {
    tooltip = tooltip.concat('\n'+ player.playerDismissed+' (Dismissal-type: '+player.type+', Bowler: '+player.bowler+', Fielder: '+player.fielder +')');
      });
  }
  return tooltip;
}

function createTooltipManhattan(overNumber, teamName, value, playersDismissed, breakdown)
{
  let tooltip=overNumber+'\n'+teamName+': '+value+createTooltipBreakdown(value,breakdown);
  if (playersDismissed.length>0)
  {
  tooltip = tooltip.concat('\nPlayers Dismissed:');
  playersDismissed.forEach((player) =>  {
    tooltip = tooltip.concat('\n'+ player.playerDismissed+' (Dismissal-type: '+player.type+', Bowler: '+player.bowler+', Fielder: '+player.fielder +')');
      });
  }
  return tooltip;
}

function createTooltipBreakdown(totalRuns, breakdown)
{
  if (totalRuns>0) {
  	let tooltip = ' (';
  	if (breakdown.batsman_runs>0)
  		tooltip = tooltip.concat(" Batsman Runs: "+breakdown.batsman_runs.toString());
  	if (breakdown.bye_runs>0)
  		tooltip = tooltip.concat(" Bye Runs: "+breakdown.bye_runs.toString());
  	if (breakdown.extra_runs>0)
  		tooltip = tooltip.concat(" Extra Runs: "+breakdown.extra_runs.toString());
  	if (breakdown.legbye_runs>0)
  		tooltip = tooltip.concat(" Legbye Runs: "+breakdown.legbye_runs.toString());
  	if (breakdown.noball_runs>0)
  		tooltip = tooltip.concat(" No Ball Runs: "+breakdown.noball_runs.toString());
  	if (breakdown.penalty_runs>0)
  		tooltip = tooltip.concat(" Penalty Runs: "+breakdown.penalty_runs.toString());
  	if (breakdown.wide_runs>0)
  		tooltip = tooltip.concat(" Wide Runs: "+breakdown.wide_runs.toString());
  	tooltip = tooltip.concat(' )');
  	return tooltip;
  }
  else return '';
}

 /**
 * @desc creats a line chart with multiple lines corresponding to each list of values
 * @param {string[]} lineNameList - The list of names corresponponding to each line of linechart
 * @param {number[][]} yLists - List of lists of numbers to be plotted, each child list corresponding to separate lines on line chart
 * @param {string[][]} tooltipLists - List of list of tooltips corresponding to each number to be plotted
 * @param {number[][]} pointValueLists - List of list of numbers at which points would appear in the line chart per list corresponding to a list of values
 */
function createLineChart(lineNameList,yLists,tooltipLists,pointValueLists,xAxisLabel,chartTitle,containerID)
{
	try {
	    if(!isEqualLength([lineNameList,yLists,tooltipLists,pointValueLists])) throw "Error in correspondance of Lists";
	    if(!isListOfListOfNumbers(yLists)) throw "Non-numeric data passed for plotting";
	    if(!isListOfListOfStrings(tooltipLists)) throw "Non-string data passed for tooltip";
	    if(!isListOfListOfNumbers(pointValueLists)) throw "Non-numeric data passed for points";
	    if(!isEqualLengthPerIndex([yLists,tooltipLists])) throw "Error in correspondance of Lists";
	    if(document.getElementById(containerID)==null) throw "containerID \"" + containerID + "\" not found";
	}
	catch(err) {
		console.log("Error: "+err);
		return;
	}
	const chart = new google.visualization.DataTable();
	chart.addColumn('number', xAxisLabel);
	yLists.forEach((element, index) => {
		chart.addColumn('number', lineNameList[index]);
		chart.addColumn({type: 'string', role: 'tooltip'});
		chart.addColumn({type: 'string', role: 'style'});
	});
	const maxLengthIndex = yLists.map(a => a.length).indexOf(Math.max.apply(Math, yLists.map(a => a.length)));
	const maxLength = yLists[maxLengthIndex].length;
	let pointTruthValueLists = [];
	pointValueLists.forEach((element, index) => {
		pointTruthValueLists.push(createTruthValueList(element,yLists[index].length));
	});
	let rowElement;
	yLists[maxLengthIndex].forEach((element, index) => {
		rowElement = [];
		rowElement.push(index+1);
		yLists.forEach((elementInner, indexInner) => {
			if (index<yLists[indexInner].length) {
				rowElement.push(elementInner[index]);
				rowElement.push(tooltipLists[indexInner][index]);
				rowElement.push((pointTruthValueLists[indexInner][index])? 'point { size: 4; }':null);  
			}
			else rowElement.push(null,null,null);
		});
		chart.addRow(rowElement);
	});
	const options =
	{
		title: chartTitle,
		width: 1200,
		height: 500,
		pointSize: 0.000001,
	};
	const lineChart = new google.visualization.LineChart(document.getElementById(containerID));
	lineChart.draw(chart, options);
}

 /**
 * @desc creats a column chart with multiple series of columns corresponding to each list of values
 * @param {string[]} lineNameList - The list of names corresponponding to each line of column chart
 * @param {number[][]} yLists - List of lists of numbers to be plotted, each child list corresponding to separate lines on column chart
 * @param {string[][]} tooltipLists - List of list of tooltips corresponding to each number to be plotted
 */
function createColumnChart(lineNameList,yLists,tooltipLists,xAxisLabel,chartTitle,containerID)
{
	try {
	    if(!isEqualLength([lineNameList,yLists,tooltipLists])) throw "Error in correspondance of Lists";
	    if(!isListOfListOfNumbers(yLists)) throw "Non-numeric data passed for plotting";
	    if(!isListOfListOfStrings(tooltipLists)) throw "Non-string data passed for tooltip";
	    if(!isEqualLengthPerIndex([yLists,tooltipLists])) throw "Error in correspondance of Lists";
	    if(document.getElementById(containerID)==null) throw "containerID \"" + containerID + "\" not found";
	}
	catch(err) {
		console.log("Error: "+err);
		return;
	}
	const chart = new google.visualization.DataTable();
	chart.addColumn('number', xAxisLabel);
	yLists.forEach((element, index) => {
		chart.addColumn('number', lineNameList[index]);
		chart.addColumn({type: 'string', role: 'tooltip'});
	});
	const maxLengthIndex = yLists.map(function(a){return a.length;}).indexOf(Math.max.apply(Math, yLists.map(function(a){return a.length;})));
	const maxLength = yLists[maxLengthIndex].length;
	let rowElement;
	yLists[maxLengthIndex].forEach((element, index) => {
		rowElement = [];
		rowElement.push(index+1);
		yLists.forEach((elementInner, indexInner) => {
			if (index<yLists[indexInner].length) {
				rowElement.push(elementInner[index]);
				rowElement.push(tooltipLists[indexInner][index]);
			}
			else rowElement.push(null,null);
		});
		chart.addRow(rowElement);
	});
	const options =
	{
	title: chartTitle,
	width: 1200,
	height: 500,
	};
	const lineChart = new google.visualization.ColumnChart(document.getElementById(containerID));
	lineChart.draw(chart, options);
}

 /**
 * @desc checks per index length correspondance of children lists
 * @return bool - success or failure, returns success in case of empty list
 */
function isEqualLengthPerIndex(lists) {
	let flag = true;
	if (!isEqualLength(lists))
		return false;
	if (lists.length == 0)
		return true;
	lists.forEach((list, index) => {
		list.forEach((innerList, innerIndex) => {
			if(innerList.length!=lists[0][innerIndex].length)
				flag = false;
		});
	});
	return flag;
}

 /**
 * @desc checks if every child list is of equal length
 * @return bool - success or failure, returns success in case of empty list
 */
function isEqualLength(lists) {
	let flag = true;
	flag = isListOfLists(lists);
	if (flag==false)
		return false;
	lists.forEach((list, index) => {
		if(list.length!=lists[0].length)
			flag = false;
	});
	return flag;
}

function isListOfLists(lists) {
	let flag = true;	
	if (!Array.isArray(lists))
		return false;
	lists.forEach((element, index) => {
		if (!Array.isArray(element))
			flag = false;
	});
	return flag;
}

function isListOfListOfNumbers(list) {
	let flag = true;
	if (!Array.isArray(list))
		return false;
	list.forEach((element, index) => {
		if(!isListOfNumbers(element))
			flag = false;
	});
	return flag;
}

function isListOfNumbers(list) {
	let flag = true;
	if (!Array.isArray(list))
		return false;
	list.forEach((element, index) => {
		if(isNaN(element))
			flag = false;
	});
	return flag;
}

function isListOfListOfStrings(list) {
	let flag = true;
	if (!Array.isArray(list))
		return false;
	list.forEach((element, index) => {
		if(!(isListOfStrings(element)))
			flag = false;
	});
	return flag;
}

function isListOfStrings(list) {
	let flag = true;
	if (!Array.isArray(list))
		return false;
	list.forEach((element, index) => {
		if(!(typeof element === 'string'))
			flag = false;
	});
	return flag;
}

function createHTMLElement(elementType,className=null){
  let element = document.createElement(elementType);
  if (className) element.classList.add(className);
  return element;
}
function createTextHTMLElement(elementType,text,className=null){
  let element = document.createElement(elementType);
  let textNode = document.createTextNode(text);
  element.appendChild(textNode);
  if (className) element.classList.add(className);
  return element;
}
function createTeamList(teamList,containerName){
  let listLength = teamList.length;
  let listContainer = document.getElementById(containerName);
  for (let i = 0; i < listLength; i++){
    let listElement = createHTMLElement("li","list-group-item");
    listElement.appendChild(document.createTextNode(teamList[i]));
    listContainer.appendChild(listElement);
  }
}
function displayTeamLists(allData){
  let team1 = allData["matchDetails"]["team1"];
  let team2 = allData["matchDetails"]["team2"];
  $('#team1Heading').append(document.createTextNode(team1));
  $('#team2Heading').append(document.createTextNode(team2));
  createTeamList(allData["playersPlaying"][team1],"team1Details");
  createTeamList(allData["playersPlaying"][team2],"team2Details");
}
function addOneBoxResult(matchDetails){
  let matchResultDiv = $("#matchResult");
  let resultString = matchDetails["result"] + " won by ";
  if (matchDetails["winByRuns"]) resultString += matchDetails["winByRuns"] + " runs";
  else resultString += matchDetails["winByWickets"] + " wickets";
  matchResultDiv.append(createTextHTMLElement("p",resultString));
}
function addOneBoxDetails(matchDetails){
  let matchDetailsDiv = $("#matchDetails");
  matchDetailsDiv.append(createTextHTMLElement("p","Venue: " + matchDetails["venue"],"card-text"));
  matchDetailsDiv.append(createTextHTMLElement("p","Player of Match: " + matchDetails["playerOfMatch"],"card-text"));
  matchDetailsDiv.append(createTextHTMLElement("p",matchDetails["team1"] + " batted first","card-text"));
}
function addOneBoxTeams(matchDetails){
  let matchTeamsDiv = $("#matchTeams");
  matchTeamsDiv.append(createTextHTMLElement("p",matchDetails["team1"] + " v/s " + matchDetails["team2"]));
  matchTeamsDiv.append(createTextHTMLElement("small",matchDetails["matchDate"]));
}
function createOneBox(matchDetails){
  $("#matchTeams").css("visibility","visible");
  $("#matchDetails").css("visibility","visible");
  $("#matchResult").css("visibility","visible");
  addOneBoxTeams(matchDetails);
  addOneBoxDetails(matchDetails);
  addOneBoxResult(matchDetails);
}
function emptyMatchElements(){
  $('#WormChartContainer').empty();
  $('#RunRateChartContainer').empty();
  $('#ManhattanChartContainer').empty();
  $('#team1Details').empty();
  $('#team2Details').empty();
  $('#matchTeams').empty();
  $('#matchDetails').empty();
  $('#matchResult').empty();
  $('#team1Heading').empty();
  $('#team2Heading').empty();
}
function enableChartsDiv(){
  $("#toggleChartsBar").css("visibility","visible");
  $("#chartsContainer").css("visibility","visible");
}
function displayMatch(allData){
  emptyMatchElements();
  enableChartsDiv();
  displayTeamLists(allData);
  createOneBox(allData["matchDetails"]);
  plotCharts(allData["chartData"]);
}
// on clicking the "View Results" button, send a GET request to fetchGraphData function in views.py and log the chartsData response.
$('.match-group .match').click(function(){
  $(this).parent().parent().find('.match').removeClass('badge');
  $(this).parent().parent().find('.match').removeClass('badge-pill');
  $(this).parent().parent().find('.match').removeClass('badge-primary');
  $(this).addClass('badge');
  $(this).addClass('badge-pill');
  $(this).addClass('badge-primary');
  let matchID = $(this).attr('data-value');
  console.log(matchID);
  $.ajax({
    type: 'GET',
    url: '/cricVis/fetchGraphData',
    data: {
      matchID: matchID
    },
    success: function(allData){
      allData = JSON.parse(allData);
      console.log(allData);
      displayMatch(allData);
    },
    error: function(error){
      console.log(error);
    }
  })
});
