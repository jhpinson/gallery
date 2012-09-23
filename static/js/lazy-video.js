$(document).ready(function() {
  
	
	
	// popup modal
	$('*[data-modal-video]').click(function(e) {
		
		var $target = $(e.currentTarget), 
		$modal = $('<div class="modal hide fade" style="display:none"></div>').forceId();
		$('body').append($modal)

		var width = $target.attr('data-width') || 800;
		if (typeof(width) !== 'undefined') {
			$modal.css({
						width : width + 'px',
						'margin-left' : function() {
							return -($(this).width() / 2);
						}
					});
		}
		$modal.modal('show');
		$modal.load($target.attr('data-modal-video'), function() {
			   var id = $modal.find('video').forceId().attr('id')
                    _V_(id);
                  })
	});

});