$(document).ready(function() {
      
	
	   
	
	   var displayImageActions = {};
      $('div.image').mouseover(function (e) {
      	
      	 var $el = $(this).forceId();
         $el.find('.actions').slideDown(200);
        
        if (typeof(displayImageActions[$el.attr('id')]) !== 'undefined') {
              clearTimeout(displayImageActions[$el.attr('id')]);
              delete displayImageActions[$el.attr('id')]
            }
      });	
	     
      
      $('div.image').mouseout(function (e) {
      	var $el = $(this).forceId();
      	if (typeof(displayImageActions[$el.attr('id')]) !== 'undefined') {
              clearTimeout(displayImageActions[$el.attr('id')]);
              delete displayImageActions[$el.attr('id')]
            }

            displayImageActions[$el.attr('id')] = setTimeout(function() {
                  $el.find('.actions').fadeOut(200);
                }, 400)
      	
      });
	     // FILE INPUT STYLE
			$('.fileinputs').each(function(id, el) {
						var $el = $(el);
						var $input = $el.find('input[type=file]');
						var $target = $el.find('.fakefile');
						$input.mouseover(function(e) {
									$target.addClass('hover');
								});

						$input.mouseout(function(e) {
									$target.removeClass('hover')
								});
					});

		  // DROPDOWN MENU PROFILE
			var displayProfileMenu = null;
			// show avatar menu
			$('div.avatar').mouseover(function() {
				    var img_offset = $('div.avatar img').offset();
				    $('div.avatar ul').css({'right' : ($('body').width() - (img_offset.left + $('div.avatar img').width())) + 'px',
				                            'top' : (img_offset.top + $('div.avatar img').height() + 10) + 'px'})
						$('div.avatar ul').fadeIn(200);
						if (displayProfileMenu !== null) {
							clearTimeout(displayProfileMenu);
							displayProfileMenu = null;
						}
					});
			$('div.avatar').mouseout(function() {

						if (displayProfileMenu !== null) {
							clearTimeout(displayProfileMenu);
							displayProfileMenu = null;
						}

						displayProfileMenu = setTimeout(function() {
									$('div.avatar ul').fadeOut(200);
								}, 400)
					});

		});