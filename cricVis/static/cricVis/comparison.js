var autofillData;
var tableHeadingData;
function receiveAutofillData(autofillDataReceived, tableHeadingReceived){
  console.log(tableHeadingReceived);
  autofillData = autofillDataReceived;
  tableHeadingData = tableHeadingReceived;
}

$('.comparisonTableChoice').on('input', function(){
  const tableName = $("input:radio[name='comparisonTable']:checked").val();
  console.log(tableName);
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
      console.log(JSON.parse(comparisonData));
      createComparisonUI(tableName, JSON.parse(comparisonData));
    },
    error: function(error){
      console.log(error);
    }
  });
});

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
  createStatsTable("T20ComparisonStats", player1Data["chartDataT20"], player2Data["chartDataT20"]);
  createStatsTable("ODIComparisonStats", player1Data["chartDataODI"], player2Data["chartDataODI"]);
  createStatsTable("TestComparisonStats", player1Data["chartDataTest"], player2Data["chartDataTest"]);
}

function createComparisonUITeams(team1Data, team2Data){
  createCardForItem("firstEntityHeader", "firstEntityBody", team1Data["cardData"]);
  createCardForItem("secondEntityHeader", "secondEntityBody", team2Data["cardData"]);
  createComparisonHeadings("TeamHeadingContainer", team1Data["cardData"]["Team Name"], team2Data["cardData"]["Team Name"]);
  createStatsTable("TeamComparisonStats", team1Data["chartData"], team2Data["chartData"]);
}

function createCardForItem(cardHeaderID, cardBodyID, cardData){
  Object.keys(cardData).forEach((key) => {
    if (key === "Player Name"){
      console.log(key);
      document.getElementById(cardHeaderID).innerText = cardData[key];
    }
    else{
      console.log(key,"Else");
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
  document.getElementById(headingContainerID).appendChild(heading1Element);
  document.getElementById(headingContainerID).appendChild(heading2Element);
}

function createStatsTable(statsDivID, statsData1, statsData2){
  const statsDiv = document.getElementById(statsDivID);
  let idCounter = 0;
  Object.keys(statsData1).forEach((key) => {
    const tableRow = createStatDiv(`comparisonChartDiv${idCounter}`, key, statsData1[key], statsData2[key]);
    statsDiv.appendChild(tableRow);
    idCounter ++;
  });
}

function createStatDiv(chartDivID, field, fieldValue1, fieldValue2){
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
  createComparisonChart(field, fieldValue1, fieldValue2);
  return parentDiv;
}


function createComparisonChart(fieldValue1,fieldValue2,containerID) {
  var data = google.visualization.arrayToDataTable([
      ['' , '' , '' ],
      ['', fieldValue1, fieldValue2]
  ]); 
  var options_fullStacked = {
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
  var chart = new google.visualization.BarChart(document.getElementById(containerID));
  chart.draw(data, options_fullStacked);
}