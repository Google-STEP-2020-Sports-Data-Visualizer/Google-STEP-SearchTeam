$(function() {
    $('#timeSlider').on('input', function() {
      var currentPositionSlider = $(this).val();
      var portion = (currentPositionSlider) / (100);
      $('#timeValueBubble').text(currentPositionSlider);
      $('#timeValueBubble').css('left', portion * $('#timeSlider').width());
    });
  });