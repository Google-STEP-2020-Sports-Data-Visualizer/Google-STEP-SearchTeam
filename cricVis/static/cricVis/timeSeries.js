// get the selected values from a checkbox group
var VisualizationResponsesReceived;
function getSelectedCheckboxValues(checkboxGroupName){
  let selectedValues = [];
  $(`input:checkbox[name=${checkboxGroupName}]:checked`).each(function(){
    selectedValues.push($(this).val());
  });
  return selectedValues;
}

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

function createErrorNotification(){
  const notification = document.createElement("div");
  notification.className = "alert alert-warning";
  notification.setAttribute("role","alert");
  notification.innerText = "Data for this request doesn't exist. We apologize for the inconvenience";
  return notification;
}

/* create a visualization request for every individual option selected 
and return a set of requests */

function getVisualizationRequestData(fields, genders, matchTypes, startDate, endDate, playerType){
  let visalizationRequests = [];
  fields.forEach(function(field){
    matchTypes.forEach(function(matchType){
      genders.forEach(function(gender){
        let visalizationRequest = {};
        visalizationRequest["startDate"] = startDate;
        visalizationRequest["endDate"] = endDate;
        visalizationRequest["field"] = field;
        let metaDataRequest = {};
        metaDataRequest["playerType"] = playerType;
        metaDataRequest["gameFormat"] = matchType;
        metaDataRequest["gender"] = gender;
        visalizationRequest["metaDataRequest"] = metaDataRequest;
        visalizationRequests.push(JSON.stringify(visalizationRequest));
      });
    });
  });
  return visalizationRequests;
}

/* keep enabling the following checkboxes on sleection of one, 
so that no invalid data get's submitted */

$('#startDate').on('input', function(){
  $('#endDate').prop('disabled', false);
});

$('#endDate').on('input', function(){
  $('input:checkbox[name=Batsman]').each(function(){
    $(this).prop('disabled', false);
  });
  $('input:checkbox[name=Bowler]').each(function(){
    $(this).prop('disabled', false);
  });
});

$('.batsmanInput').on('input', function(){
  $('input:checkbox[name=matchType]').each(function(){
    $(this).prop('disabled', false);
  });
});

$('.bowlerInput').on('input', function(){
  $('input:checkbox[name=matchType]').each(function(){
    $(this).prop('disabled', false);
  });
});

$('.matchTypeInput').on('input', function(){
  $('input:checkbox[name=gender]').each(function(){
    $(this).prop('disabled', false);
  });
});

$('.genderInput').on('input', function(){
  $('#fetchTimeSeriesDataButton').prop('disabled', false);
});

$('.carousel').carousel({
  interval: false,
});

function getSliderNumber(divID){
  const divIDList = divID.split("_");
  return parseInt(divIDList[1]);
}

function createSlider(chartSliderDiv, sliderNumber, VisualizationResponses){
  if (isEmpty(VisualizationResponses[sliderNumber]["chartDataResponse"])){
    chartSliderDiv.appendChild(createErrorNotification());
  }
  else{
    new TimeSlider(chartSliderDiv.id, `chartDiv_${sliderNumber}`, sliderNumber, VisualizationResponses[sliderNumber]);
  }
}

// send an AJAX GET to get a set of responses corresponding to the set of requests

$('#fetchTimeSeriesDataButton').click(function(){
  const startDate = $('#startDate').val();
  const endDate = $('#endDate').val();
  const batsmanFields = getSelectedCheckboxValues('Batsman');
  const bowlerFields = getSelectedCheckboxValues('Bowler');
  const matchTypes = getSelectedCheckboxValues('matchType');
  const genders = getSelectedCheckboxValues('gender');
  const visualizationResquestsBatsman = getVisualizationRequestData(batsmanFields, genders, matchTypes, startDate, endDate, "Batsman");
  const visualizationResquestsBowler = getVisualizationRequestData(bowlerFields, genders, matchTypes, startDate, endDate, "Bowler");
  const visalizationRequests = visualizationResquestsBatsman.concat(visualizationResquestsBowler);
  $.ajax({
    type: 'GET',
    url: '/cricVis/fetchTimeSeriesData',
    data: {
      visualizationRequest: visalizationRequests
    },
    success: function(visalizationResponses){
      VisualizationResponsesReceived = JSON.parse(visalizationResponses);
      addCarousel(VisualizationResponsesReceived);
    },
    error: function(error){
      console.log(error);
    }
  });
});
function addCarousel(VisualizationResponses) {
  document.getElementById("timeSeriesCarousel").style.visibility = 'visible';
  let carouselInnerDiv = document.getElementById('carouselContainer');
  $('#carouselContainer').empty();
  for (var i = 0; i < VisualizationResponses.length; i++) {
    let carouselItem = document.createElement("div");
    carouselItem.className = "carousel-item";
    carouselItem.id = "carouselDiv_"+i.toString();
    if (i==0) {
      carouselItem.className += " active"
    }
    carouselItem.className += " carouselDiv";
    let chartSliderDiv = document.createElement("div");
    chartSliderDiv.id = "chartSliderDiv_"+i.toString();
    chartSliderDiv.className = "carouselDiv";
    carouselInnerDiv.appendChild(carouselItem);
    let chartDiv = document.createElement("div");
    chartDiv.id = "chartDiv_"+i.toString();
    carouselItem.appendChild(chartSliderDiv);
    chartSliderDiv.appendChild(chartDiv);
    if (i==0){
      createSlider(chartSliderDiv, i, VisualizationResponses);
    }
 }
}
$('.carousel').on('slide.bs.carousel', function onSlide (ev) {
  const carouselDivPrevious = document.getElementsByClassName("active")[0];
  const sliderNumber = (getSliderNumber(carouselDivPrevious.id) + 1) % VisualizationResponsesReceived.length;
  const chartSliderDiv = document.getElementById(`carouselDiv_${sliderNumber}`).children[0];
  const chartSliderDivChildren = chartSliderDiv.children;
  let flag = true;
  for (let childElementIndex = 0; childElementIndex < chartSliderDivChildren.length; childElementIndex++){
    if (chartSliderDivChildren[childElementIndex].id === `timeSliderContainer${sliderNumber}`) {
      flag = false;
    }
  }
  if (flag){
    createSlider(chartSliderDiv, sliderNumber, VisualizationResponsesReceived);
  }

});