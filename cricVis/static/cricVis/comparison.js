google.charts.load('current', {'packages':['corechart','bar']});
var autofillData;
var tableHeadingData;
function receiveAutofillData(autofillDataReceived, tableHeadingReceived){
  autofillData = autofillDataReceived;
  tableHeadingData = tableHeadingReceived;
}

$('.comparisonTableChoice').on('input', function(){
  const tableName = $("input:radio[name='comparisonTable']:checked").val();
  createAutofill(autofillData[tableName], "autofillFirst", tableHeadingData[tableName]);
  createAutofill(autofillData[tableName], "autofillSecond", tableHeadingData[tableName]);
});

$('#fetchComparisonData').click(function(){
  const entityID1 = $("#autofillFirst").val();
  const entityID2 = $("#autofillSecond").val();
  const tableName = $("input:radio[name='comparisonTable']:checked").val();
  $.ajax({
    type: 'GET',
    url: '/cricVis/fetchComparisonData',
    data: {
      entityID1: entityID1,
      entityID2: entityID2,
      tableName: tableName,
    },
    success: function(comparisonData){
      createComparisonUI(tableName, JSON.parse(comparisonData));
    },
    error: function(error){
      console.log(error);
    }
  });
});

function emptyDiv(divID){
  $(`#${divID}`).empty();
}

function createAutofill(sourceData, inputID, type){
  $(`#${inputID}`).attr('disabled', false);
  $(`#${inputID}`).attr('placeholder', `Enter ${type} name...`);
  $(`#${inputID}`).autocomplete({
    minLength:2,    
    source: sourceData
 });
}

function createHTMLElement(type, elementClass=null, elementID=null){
  const element = document.createElement(type);
  if (elementID) element.id = elementID;
  if (elementClass) element.className = elementClass;
  return element;
}

function createComparisonUI(tableName, comparisonData){
  if (tableName == "TeamWise"){
    createComparisonUITeams(comparisonData[0], comparisonData[1]);
  }
  else{
    createComparisonUIPlayers(comparisonData[0], comparisonData[1]);
  }
}

function createComparisonUIPlayers(player1Data, player2Data){
  createCardForItem("firstEntityHeader", "firstEntityBody", player1Data["cardData"]);
  createCardForItem("secondEntityHeader", "secondEntityBody", player2Data["cardData"]);
  createComparisonHeadings("T20HeadingContainer", player1Data["cardData"]["Player Name"], player2Data["cardData"]["Player Name"]);
  createComparisonHeadings("ODIHeadingContainer", player1Data["cardData"]["Player Name"], player2Data["cardData"]["Player Name"]);
  createComparisonHeadings("TestHeadingContainer", player1Data["cardData"]["Player Name"], player2Data["cardData"]["Player Name"]);
  document.getElementById("comparisonPlayerContainer").style.visibility = "visible";
  document.getElementById("cardDataContainer").style.visibility = "visible";
  createStatsTable("T20ComparisonStats", player1Data["chartDataT20"], player2Data["chartDataT20"], "T20");
  createStatsTable("ODIComparisonStats", player1Data["chartDataODI"], player2Data["chartDataODI"], "ODI");
  createStatsTable("TestComparisonStats", player1Data["chartDataTest"], player2Data["chartDataTest"], "Test");
}

function createComparisonUITeams(team1Data, team2Data){
  createCardForItem("firstEntityHeader", "firstEntityBody", team1Data["cardData"]);
  createCardForItem("secondEntityHeader", "secondEntityBody", team2Data["cardData"]);
  createComparisonHeadings("TeamHeadingContainer", team1Data["cardData"]["Team Name"], team2Data["cardData"]["Team Name"]);
  document.getElementById("comparisonPlayerContainer").style.visibility = "visible";
  document.getElementById("cardDataContainer").style.visibility = "visible";
  createStatsTable("TeamComparisonStats", team1Data["chartData"], team2Data["chartData"], "Team");
}

function createCardForItem(cardHeaderID, cardBodyID, cardData){
  emptyDiv(cardBodyID);
  Object.keys(cardData).forEach((key) => {
    if (key === "Player Name" | key === "Team Name"){
      document.getElementById(cardHeaderID).innerText = cardData[key];
    }
    else{
      const dataTag = createHTMLElement("p", "card-text");
      dataTag.innerText = `${key} : ${cardData[key]}`;
      document.getElementById(cardBodyID).appendChild(dataTag);
    }
  });
}

function createComparisonHeadings(headingContainerID, heading1, heading2){
  const heading1Element = createHTMLElement("h3");
  const heading2Element = createHTMLElement("h3");
  heading1Element.innerText = heading1;
  heading2Element.innerText = heading2;
  emptyDiv(headingContainerID);
  document.getElementById(headingContainerID).appendChild(heading1Element);
  document.getElementById(headingContainerID).appendChild(heading2Element);
}

function createStatsTable(statsDivID, statsData1, statsData2, category){
  emptyDiv(statsDivID);
  let statsDiv = document.getElementById(statsDivID);
  let idCounter = 0;
  Object.keys(statsData1).forEach((key) => {
    createStatDiv(`comparisonChartDiv${category}${idCounter}`, key, statsData1[key], statsData2[key], statsDiv);
    idCounter ++;
  });
}

function createStatDiv(chartDivID, field, fieldValue1, fieldValue2, statsDiv){
  const parentDiv = createHTMLElement("div", "list-group-item list-group-item-action flex-column align-items-center chartStatsContainer");
  const chartStatsDiv = createHTMLElement("div", "d-flex w-100 justify-content-between");
  const chartDiv = createHTMLElement("div", "comparisonChartDiv", chartDivID);
  const stat1 = createHTMLElement("p", "statTag");
  const stat2 = createHTMLElement("p", "statTag");
  stat1.innerText = fieldValue1;
  stat2.innerText = fieldValue2;
  const chartStatsDivHeading = createHTMLElement("h4", "chartStatsDivHeading");
  chartStatsDivHeading.innerText = field;
  chartStatsDiv.appendChild(stat1);
  chartStatsDiv.appendChild(chartDiv);
  chartStatsDiv.appendChild(stat2);
  parentDiv.appendChild(chartStatsDivHeading);
  parentDiv.appendChild(chartStatsDiv);
  statsDiv.appendChild(parentDiv);
  createComparisonChart(fieldValue1, fieldValue2, chartDivID);
}

function createComparisonChart(fieldValue1,fieldValue2,containerID) {
  const data = google.visualization.arrayToDataTable([
      ['' , '' , '' ],
      ['', fieldValue1, fieldValue2]
  ]);
  const options_fullStacked = {
    'width':400,
    'height':54,
    isStacked: 'percent',
    legend: 'none',
    hAxis: {
      textPosition: 'none',
      baselineColor: 'transparent',
      ticks: []
    },
    vAxis: {
      textPosition: 'none',
      baselineColor: 'transparent',
      ticks: []
    },
    'tooltip' : {
      trigger: 'none',
    }
  };
  const chart = new google.visualization.BarChart(document.getElementById(containerID));
  chart.draw(data, options_fullStacked);
}