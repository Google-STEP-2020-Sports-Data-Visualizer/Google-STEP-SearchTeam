function clearDiv(divID){
  $('#' + divID).empty();
}
function enableSlider(dateList){
  const rangeMax = (dateList.length - 1) * 5;
  document.getElementById("timeSlider").max = rangeMax.toString();
  useSlider(dateList);
}
function useSlider(dateList){
  $('#timeSlider').on('input', function() {
    var currentPositionSlider = $(this).val();
    var portion = (currentPositionSlider) / ($(this).attr('max'));
    $('#timeValueBubble').text(dateList[currentPositionSlider / 5]);
    $('#timeValueBubble').css('left', portion * $('#timeSlider').width());
  });
}