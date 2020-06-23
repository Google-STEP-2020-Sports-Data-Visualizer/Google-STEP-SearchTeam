function clearDiv(divID){
  $('#' + divID).empty();
}
function enableSlider(dateList,timeSliderID,timeValueBubbleID){
  const rangeMax = (dateList.length - 1) * 5;
  document.getElementById(timeSliderID).max = rangeMax.toString();
  useSlider(dateList,timeSliderID,timeValueBubbleID);
}
function useSlider(dateList,timeSliderID,timeValueBubbleID){
  $(`#${timeSliderID}`).on('input', function() {
    var currentPositionSlider = $(this).val();
    var portion = (currentPositionSlider) / ($(this).attr('max'));
    $(`#${timeValueBubbleID}`).text(dateList[currentPositionSlider / 5]);
    $(`#${timeValueBubbleID}`).css('left', portion * $(`#${timeSliderID}`).width());
  });
}