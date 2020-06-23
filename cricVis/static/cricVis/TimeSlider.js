class TimeSlider{
  constructor(carouselID, chartDivID, sliderIDNumber, chartData){
    this.carouselID = carouselID;
    this.chartDivID = chartDivID;
    this.sliderIDNumber = sliderIDNumber;
    this.chartData = chartData;
  }
  createTimeSlider(){
    const sliderElement = this.createHTMLElement("input", `timeSlider${this.sliderIDNumber}`, "timeSlider");
    const sliderBubble = this.createHTMLElement("span", `timeSliderValueBubble${this.sliderIDNumber}`, "timeSliderValueBubble");
    let sliderContainer = this.createHTMLElement("div", `timeSliderContainer${this.sliderIDNumber}`, "timeSliderContainer");
    sliderContainer.appendChild(sliderBubble);
    sliderContainer.appendChild(sliderElement);
    document.getElementById(this.carouselID).appendChild(sliderContainer);
  }
  createHTMLElement(elementType, elementID, elementClass){
    let element = document.createElement(elementType);
    element.id = elementID;
    element.classList.add(elementClass);
    return element;
  }
}