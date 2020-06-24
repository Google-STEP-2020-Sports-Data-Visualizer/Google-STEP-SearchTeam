google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(createChart);

function GetSortOrderDescending(prop){
   return function(a,b){
      if( a[prop] < b[prop]){
          return 1;
      }else if( a[prop] > b[prop] ){
          return -1;
      }
      return 0;
   }
}

function createChart(chartDivID, metaDataResponse, yearResponse) {

    let chartValues = [];
    Object.keys(yearResponse).forEach((value) => {
      chartValues.push({"xValue":value, "yValue":yearResponse[value]});
    });
    chartValues.sort(GetSortOrderDescending("yValue"));

    const data = new google.visualization.DataTable();
    data.addColumn('string', metaDataResponse.xAxisLabel);
    data.addColumn('number', metaDataResponse.yAxisLabel);
    chartValues.forEach((value) => {
      data.addRow([value.xValue, value.yValue]);
    });

    const options = {
      width: 800,
      chart: {
        title: metaDataResponse.title,
      },
      bars: 'horizontal',
    };

    const chart = new google.charts.Bar(document.getElementById(chartDivID));
    chart.draw(data, options);
};


function addCarousel(VisualizationResponses) {

    let carouselInnerDiv = document.getElementById('carouselContainer');
    for (var i = 0; i < VisualizationResponses.length; i++) {
      let carouselItem = document.createElement("div");
      carouselItem.className = "carousel-item";
      carouselItem.id = "carouselDiv"+i.toString();
      if (i==0) {
        carouselItem.className += " active"
      }
      carouselInnerDiv.appendChild(carouselItem);
      let chartDiv = document.createElement("div");
      chartDiv.id = "chartDiv"+i.toString();
      carouselItem.appendChild(chartDiv);
   }
}

