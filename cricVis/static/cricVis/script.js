function plotCharts(chartsData)
{
  console.log(chartsData);

  
  
  var wormdata = new google.visualization.DataTable();
  
  wormdata.addColumn('number', 'Overs');
  wormdata.addColumn('number', chartsData.wormChartData.team1.teamName);
  wormdata.addColumn({type: 'string', role: 'tooltip'});
  wormdata.addColumn('number', chartsData.wormChartData.team2.teamName);
  wormdata.addColumn({type: 'string', role: 'tooltip'});
  var s1='',s2='';
  var i;
  if(chartsData.wormChartData.team1.overs.length>=chartsData.wormChartData.team2.overs.length)
  {
    
      for (i = 0; i < chartsData.wormChartData.team2.overs.length; i++)
      {
        s1='';
        s2='';
        if (chartsData.wormChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.wormChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
        if (chartsData.wormChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.wormChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          wormdata.addRow([i+1,chartsData.wormChartData.team1.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team1.teamName+': '+chartsData.wormChartData.team1.overs[i].cumulativeRuns+s1,chartsData.wormChartData.team2.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team2.teamName+': '+chartsData.wormChartData.team2.overs[i].cumulativeRuns+s2]);
      }
      for (i = chartsData.wormChartData.team2.overs.length; i < chartsData.wormChartData.team1.overs.length; i++)
      {
        s1='';
        if (chartsData.wormChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.wormChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          wormdata.addRow([i+1,chartsData.wormChartData.team1.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team1.teamName+': '+chartsData.wormChartData.team1.overs[i].cumulativeRuns+s1,null,null]);
      }
  }
  else
  {
      for (i = 0; i < chartsData.wormChartData.team1.overs.length; i++)
      {
        s1='';
        s2='';
        if (chartsData.wormChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.wormChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
        if (chartsData.wormChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.wormChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          wormdata.addRow([i+1,chartsData.wormChartData.team1.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team1.teamName+': '+chartsData.wormChartData.team1.overs[i].cumulativeRuns+s1,chartsData.wormChartData.team2.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team2.teamName+': '+chartsData.wormChartData.team2.overs[i].cumulativeRuns+s2]);
      }
      for (i = chartsData.wormChartData.team1.overs.length; i < chartsData.wormChartData.team2.overs.length; i++)
      {
        s2='';
        if (chartsData.wormChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.wormChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.wormChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          wormdata.addRow([i+1,null,null,chartsData.wormChartData.team2.overs[i].cumulativeRuns,i+1+'\n'+chartsData.wormChartData.team2.teamName+': '+chartsData.wormChartData.team2.overs[i].cumulativeRuns+s2]);
      }
  }

  
  var wormoptions =
  {
      title: 'Worm Chart',
      width: 1200,
      height: 500
  };    
  var wormchart = new google.visualization.LineChart(document.getElementById('WormChartContainer'));
  wormchart.draw(wormdata, wormoptions);
  

  
  
  var runratedata = new google.visualization.DataTable();

  runratedata.addColumn('number', 'Overs');
  runratedata.addColumn('number', chartsData.runRateChartData.team1.teamName);
  runratedata.addColumn({type: 'string', role: 'tooltip'});

  runratedata.addColumn('number', chartsData.runRateChartData.team2.teamName);
  runratedata.addColumn({type: 'string', role: 'tooltip'});

  
  if(chartsData.runRateChartData.team1.overs.length>=chartsData.runRateChartData.team2.overs.length)
  {

      for (i = 0; i < chartsData.runRateChartData.team2.overs.length; i++)
      {
        s1='';
        s2='';
        if (chartsData.runRateChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.runRateChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
        if (chartsData.runRateChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.runRateChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          runratedata.addRow([i+1,chartsData.runRateChartData.team1.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team1.teamName+': '+chartsData.runRateChartData.team1.overs[i].runRate+s1,chartsData.runRateChartData.team2.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team2.teamName+': '+chartsData.runRateChartData.team2.overs[i].runRate+s2]);
      }
      for (i = chartsData.runRateChartData.team2.overs.length; i < chartsData.runRateChartData.team1.overs.length; i++)
      {
        s1='';
        if (chartsData.runRateChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.runRateChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          runratedata.addRow([i+1,chartsData.runRateChartData.team1.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team1.teamName+': '+chartsData.runRateChartData.team1.overs[i].runRate+s1,null,null]);
      }
  }
  else
  {
      for (i = 0; i < chartsData.runRateChartData.team1.overs.length; i++)
      {
          s1='';
        s2='';
        if (chartsData.runRateChartData.team1.overs[i].playersDismissed.length>0)
        {
          s1='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team1.overs[i].playersDismissed.length; j++)
          {
            s1 = s1.concat('\n'+ chartsData.runRateChartData.team1.overs[i].playersDismissed[j].playerDismissed);
          }

        }
        if (chartsData.runRateChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.runRateChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          runratedata.addRow([i+1,chartsData.runRateChartData.team1.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team1.teamName+': '+chartsData.runRateChartData.team1.overs[i].runRate+s1,chartsData.runRateChartData.team2.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team2.teamName+': '+chartsData.runRateChartData.team2.overs[i].runRate+s2]);
      }
      for (i = chartsData.runRateChartData.team1.overs.length; i < chartsData.runRateChartData.team2.overs.length; i++)
      {
          s2='';
        if (chartsData.runRateChartData.team2.overs[i].playersDismissed.length>0)
        {
          s2='\nPlayers Dismissed:';
          for (var j = 0; j < chartsData.runRateChartData.team2.overs[i].playersDismissed.length; j++)
          {
            s2 = s2.concat('\n'+ chartsData.runRateChartData.team2.overs[i].playersDismissed[j].playerDismissed);
          }

        }
          runratedata.addRow([i+1,null,null,chartsData.runRateChartData.team2.overs[i].runRate,i+1+'\n'+chartsData.runRateChartData.team2.teamName+': '+chartsData.runRateChartData.team2.overs[i].runRate+s2]);
      }
  }

  
  var runrateoptions =
  {
      title: 'Run Rate Graph',
      width: 1200,
      height: 500
  };    
  var runratechart = new google.visualization.LineChart(document.getElementById('RunRateChartContainer'));
  runratechart.draw(runratedata, runrateoptions);
  
  
  
  
  var manhattandata = new google.visualization.DataTable();

  
  manhattandata.addColumn('number', 'Overs');
  manhattandata.addColumn('number', chartsData.manhattanChartData.team1.teamName);
  manhattandata.addColumn('number', chartsData.manhattanChartData.team2.teamName);
  
  if(chartsData.manhattanChartData.team1.overs.length>=chartsData.manhattanChartData.team2.overs.length)
  {
      for (i = 0; i < chartsData.manhattanChartData.team2.overs.length; i++)
      {
          manhattandata.addRow([i+1,chartsData.manhattanChartData.team1.overs[i].runs,chartsData.manhattanChartData.team2.overs[i].runs]);
      }
      for (i = chartsData.manhattanChartData.team2.overs.length; i < chartsData.manhattanChartData.team1.overs.length; i++)
      {
          manhattandata.addRow([i+1,chartsData.manhattanChartData.team1.overs[i].runs,null]);
      }
  }
  else
  {
      for (i = 0; i < chartsData.manhattanChartData.team1.overs.length; i++)
      {
          manhattandata.addRow([i+1,chartsData.manhattanChartData.team1.overs[i].runs,chartsData.manhattanChartData.team2.overs[i].runs]);
      }
      for (i = chartsData.manhattanChartData.team1.overs.length; i < chartsData.manhattanChartData.team2.overs.length; i++)
      {
          manhattandata.addRow([i+1,null,chartsData.manhattanChartData.team2.overs[i].runs]);
      }
  }

  
  var manhattanoptions =
  {
      title: 'Manhattan Graph',
      width: 1200,
      height: 500
  };    
  var manhattanchart = new google.charts.Bar(document.getElementById('ManhattanChartContainer'));
  manhattanchart.draw(manhattandata, google.charts.Bar.convertOptions(manhattanoptions));
    
}
function createHTMLElement(elementType,className=null){
  let element = document.createElement(elementType);
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
function emptyMatchElements(){
  $('#WormChartContainer').empty();
  $('#RunRateChartContainer').empty();
  $('#ManhattanChartContainer').empty();
  $('#team1Details').empty();
  $('#team2Details').empty();
}
function enableChartsDiv(){
  $("#toggleChartsBar").css("visibility","visible");
  $("#chartsContainer").css("visibility","visible");
}
function displayMatch(allData){
  emptyMatchElements();
  enableChartsDiv();
  displayTeamLists(allData);
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
      displayMatch(allData);
    },
    error: function(error){
      console.log(error);
    }
  })
});