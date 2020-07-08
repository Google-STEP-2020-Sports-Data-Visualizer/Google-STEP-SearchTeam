class TimeSlider{
  constructor(carouselID, chartDivID, sliderIDNumber, chartData, carouselDiv){
    this.carouselID = carouselID;
    this.chartDivID = chartDivID;
    this.sliderIDNumber = sliderIDNumber;
    this.chartData = chartData;
    this.dateList = this.createDateList(this.chartData["chartDataResponse"]);
    this.sliderID = `timeSlider${this.sliderIDNumber}`;
    this.sliderBubbleID = `timeSliderValueBubble${this.sliderIDNumber}`;
    this.carouselDiv = carouselDiv;
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
  // drawChart(chart, options){
  //   chart.draw(data, options);
  // }
  createChart(chartDivID, metaDataResponse, yearResponse) {
    $(`#${chartDivID}`).empty();
    let chartValues = [];
    Object.keys(yearResponse).forEach((value) => {
      chartValues.push({"xValue":value, "yValue":yearResponse[value]});
    });
    chartValues.sort(this.getSortOrderDescending("yValue"));
    const data = new google.visualization.DataTable();
    data.addColumn('string', metaDataResponse.xAxisLabel);
    data.addColumn('number', metaDataResponse.yAxisLabel);
    chartValues.forEach((value) => {
      data.addRow([value.xValue, value.yValue]);
    });

    const options = {
      height: 600,
      chart: {
        title: metaDataResponse.title,
      }
    };
    const chart = new google.visualization.BarChart(document.getElementById(chartDivID));
    chart.draw(data, options);
    console.log("here");
    
    console.log("hello");
    // if (this.carouselDiv.id !== "carouselDiv0"){
    //   console.log("entered");
    //   console.log(this.carouselDiv.classList);
    //   this.carouselDiv.classList.remove("active");
    // }
  }
}