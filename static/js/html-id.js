(function($) {
  var generatedIds =0;
	$.fn.extend({

				forceId : function() {

					if (typeof($(this).attr('id')) === 'undefined') {
						$(this).attr('id', 'auto-id-' + generatedIds);
						generatedIds++;
					}
					
					return $(this);
				}
			});
})(jQuery);
