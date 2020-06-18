function enableSlider(dateList){
  const rangeMax = (dateList.length - 1) * 5;
  document.getElementById("timeSlider").max = rangeMax.toString();
  useSlider(dateList);
}