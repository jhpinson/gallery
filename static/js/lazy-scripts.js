$(document).ready(function() {
	 
	$('.fileinputs').each(function (id, el) {
		var $el = $(el);
		var $input = $el.find('input[type=file]');
		var $target = $el.find('.fakefile');
		$input.mouseover(function (e) {
			$target.addClass('hover');
		});
		
		$input.mouseout(function (e) {
      $target.removeClass('hover')
    });
	});
	
});