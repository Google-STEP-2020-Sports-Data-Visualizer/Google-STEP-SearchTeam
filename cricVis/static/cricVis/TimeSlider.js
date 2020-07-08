class TimeSlider{
  constructor(carouselID, chartDivID, sliderIDNumber, chartData){
    this.carouselID = carouselID;
    this.chartDivID = chartDivID;
    this.sliderIDNumber = sliderIDNumber;
    this.chartData = chartData;
    this.dateList = this.createDateList(this.chartData["chartDataResponse"]);
    this.sliderID = `timeSlider${this.sliderIDNumber}`;
    this.sliderBubbleID = `timeSliderValueBubble${this.sliderIDNumber}`;
    this.createTimeSlider();
  }
  createDateList(chartDataResponse){
    let dateList = [];
    Object.keys(chartDataResponse).forEach(function(date){
      dateList.push(date);
    });
    dateList.sort();
    return dateList;
  }
  createTimeSlider(){
    const sliderElement = this.createHTMLElement("input", `timeSlider${this.sliderIDNumber}`, "timeSlider");
    sliderElement.min = 0;
    sliderElement.value = 0;
    sliderElement.type = "range";
    sliderElement.step = 5;
    const sliderBubble = this.createHTMLElement("span", `timeSliderValueBubble${this.sliderIDNumber}`, "timeSliderValueBubble");
    let sliderContainer = this.createHTMLElement("div", `timeSliderContainer${this.sliderIDNumber}`, "timeSliderContainer");
    sliderContainer.appendChild(sliderBubble);
    sliderContainer.appendChild(sliderElement);
    document.getElementById(this.carouselID).appendChild(sliderContainer);
    this.enableSlider()
  }
  createHTMLElement(elementType, elementID, elementClass){
    let element = document.createElement(elementType);
    element.id = elementID;
    element.classList.add(elementClass);
    return element;
  }
  enableSlider(){
    const rangeMax = (this.dateList.length - 1) * 5;
    document.getElementById(this.sliderID).max = rangeMax.toString();
    document.getElementById(this.sliderBubbleID).innerHTML = this.dateList[0];
    this.useSlider();
  }
  useSlider(){
    const classObject = this;
    classObject.createChart(classObject.chartDivID, classObject.chartData["metaDataResponse"], classObject.chartData["chartDataResponse"][classObject.dateList[0]]);
    $(`#${classObject.sliderID}`).on('input', function() {
      const currentPositionSlider = $(this).val();
      const portion = (currentPositionSlider) / ($(this).attr('max'));
      const year = classObject.dateList[currentPositionSlider / 5];
      $(`#${classObject.sliderBubbleID}`).text(year);
      $(`#${classObject.sliderBubbleID}`).css('left', portion * $(`#${classObject.sliderID}`).width());
      classObject.createChart(classObject.chartDivID, classObject.chartData["metaDataResponse"], classObject.chartData["chartDataResponse"][year]);
    });
  }
getSortOrderDescending(prop){
    return function(a,b){
      if( a[prop] < b[prop]){
        return 1;
      }
      else if( a[prop] > b[prop] ){
        return -1;
      }
      return 0;
    }
 }
  createChart(chartDivID, metaDataResponse, chartPlotData) {
    $(`#${chartDivID}`).empty();
    let chartValues = [];
    Object.keys(chartPlotData).forEach((value) => {
      chartValues.push({"xValue":value, "yValue":chartPlotData[value]});
    });
    chartValues.sort(this.getSortOrderDescending("yValue"));
    this.drawBarChart(chartValues,metaDataResponse.xAxisLabel,metaDataResponse.yAxisLabel,
      metaDataResponse.title,chartDivID)
  }
  drawBarChart(chartData,xAxisLabel,yAxisLabel,chartTitle,containerID) {
    const data = new google.visualization.DataTable();
    data.addColumn('string', yAxisLabel);
    data.addColumn('number', xAxisLabel);
    chartData.forEach((value) => {
        data.addRow([value.xValue, value.yValue]);
    });
    const options = {
      height: 600,
      chart: {
        title: chartTitle,
      },
      bars: 'horizontal',
    };
    const chart = new google.charts.Bar(document.getElementById(containerID));
    chart.draw(data, options);
  }
}