(function($) {

	var initGallery = function(items) {
		
		var currentSlide = null;
		var displayLegend = true;
		var lastMousePos = {x : 0, y : 0};
		
		// template for displaying items
		var template = '' + '<div class="item" ><div class="item-w">' + '  <div style="position:relative;display: inline-block;"><img src="">'
				+ '  <div class="legend" style="display:none;">'
				+ '    <h3></h3>' + '  </div></div>' + '</div></div>';
    
		var getPrefix = function getPrefix(prop){
        var prefixes = ['Moz','Khtml','Webkit','O','ms'],
            elem     = document.createElement('div'),
            upper    = prop.charAt(0).toUpperCase() + prop.slice(1);

        for (var len = prefixes.length; len--; ){
            if ((prefixes[len] + upper)  in elem.style)
                return ('-'+prefixes[len].toLowerCase()+'-');
        }

        return false;
    };
    
    var onResize = function () {
      createEffectStyle();
    }
    
    var ismouseover = function(overThis, x, y) {  
        var offset = $(overThis).offset();             
        result =    offset.left <= x && offset.left + $(overThis).outerWidth() > x &&
                    offset.top <= y && offset.top + $(overThis).outerHeight() > y;
        return result;
    };  
    
    var mouseMove = function (e) {
    	lastMousePos.x = e.pageX;
    	lastMousePos.y = e.pageY;
      if (currentSlide !== null) {
         syncLegendVisibility()
      }
    }
    
    var syncLegendVisibility = function (force) {
    	if (currentSlide === null && force !== true) {
    		 return;
    	}
    	var _displayLegend = ismouseover(currentSlide.find('img:first'),lastMousePos.x, lastMousePos.y);
      displayLegend = _displayLegend;
      if (displayLegend && currentSlide.find('.legend:visible').length == 0) {
       currentSlide.find('.legend').fadeIn(200);
      } else if (!displayLegend && currentSlide.find('.legend:visible').length == 1){
       currentSlide.find('.legend').fadeOut(200);
      }
    }
    
    // create effect style sheet
    var createEffectStyle = function () {
    	
    	var prefix = getPrefix('transform');
    	var prefixAnimation = getPrefix('animation');
    	
    	var offset = $(window).width();
    	
    	var effect = [
          '@'+prefixAnimation+'keyframes outRight {',     
              '0% { '+prefix+'transform: translateX(0px);}',
              '20% { '+prefix+'transform: translateX(+10px);}',
              '60% { '+prefix+'transform: translateX(-'+(offset + 30)+'px);}',
              '80% { '+prefix+'transform: translateX(-'+(offset - 10)+'px);}',
              '100% { '+prefix+'transform: translateX(-'+offset+'px);}',
          '}',
          
          '@'+prefixAnimation+'keyframes outLeft {',
              '0% { '+prefix+'transform: translateX(0px);}',
              '20% { '+prefix+'transform: translateX(-10px);}',
              '60% { '+prefix+'transform: translateX('+(offset + 30)+'px);}',
              '80% { '+prefix+'transform: translateX('+(offset - 10)+'px);}',
              '100% {'+prefix+'transform: translateX('+offset+'px);}',
          '}'
          
      ].join('');
      
      
      var changeClass = [
          '.transition-next {',
              prefixAnimation+'animation: '+effectDuration+'ms ease;',
              prefixAnimation+'animation-name: outRight;',
              prefixAnimation+'animation-fill-mode: both;',
          '}',
          
          '.transition-prev {',
              prefixAnimation+'animation: '+effectDuration+'ms ease;',
              prefixAnimation+'animation-name: outLeft;',
              prefixAnimation+'animation-fill-mode: both;',
          '}'
          
      ].join('');
      
      if(!document.getElementById('glisse-css')) {
          $('<style type="text/css" id="glisse-css">'+effect+changeClass+'</style>').appendTo('head');
      } else {
          $('#glisse-css').html(effect+changeClass);
      }
      
    }
    
		// display next slide
		var nextSlide = function() {
			if (currentPos == $(items).length - 1) {
				if (supportEffects) {
  				$('#gallery .item').addClass('shake');
            setTimeout(function () {
              $('#gallery .item').removeClass('shake');
            }, 600);
				}
				return;
			}
			displaySlide(++currentPos, true);
		}
    
		// display previous slide
		var previousSlide = function() {
			if (currentPos == 0) {
				if (supportEffects) {
  				$('#gallery .item').addClass('shake');
            setTimeout(function () {
              $('#gallery .item').removeClass('shake');
            }, 600);
            return;
				}
			}
			displaySlide(--currentPos, false);
		}
		
		// close gallery
		var close = function() {
			$(document).unbind('keyup', keyUpHandler);
			$(document).unbind('mousemove', mouseMove);
			$(window).unbind('resize', onResize);
			
			if (supportEffects) {
			gallery.fadeOut(500, function() {
						gallery.remove();
					})
			} else {
			   gallery.remove();
			}
		}
    
		
		
    // display slide at pos 
		var displaySlide = function(pos, next) {
			currentSlide = null;
			$('#gallery .item:first .legend').slideUp(200);
			
			if (slideContainer.children('.item').length == 2) {
            slideContainer.children('.item:first').remove();
          }
			
			var offset = $(window).width();
			
			var item = $(items.get(pos));
			var slide = $(template);
			slide.find('img:first').attr('src', item.attr('data-img-src'));
			slide.find('.legend').html(item.find('.caption').html());
			
			var slideNav = nav.clone();
			slideNav.find('.prev').click(previousSlide);
      slideNav.find('.next').click(nextSlide);
      slideNav.find('.close').click(close);
    
			slide.find('.legend').append(slideNav);
      slide.forceId();
      
      slide.find('img').load(function () {
        slide.css({
               left : (next ? offset : -offset) + 'px'
              })
      	slideContainer.append(slide);
      	
      	
        if(supportEffects) {
          var transitionClass = next ? 'transition-next' : 'transition-prev';
          slideContainer.children('.item').addClass(transitionClass);
          setTimeout(function () {
          	if (slideContainer.children('.item').length == 2) {
              slideContainer.children('.item:first').remove();
            }
          	slide.css('left', '0px');
            slide.removeClass(transitionClass);
            currentSlide = slide;
            syncLegendVisibility(true);           
            
          }, effectDuration + 100);
        } else {
          slideContainer.children('.item').css('left', (next ? '-=' : '+=') + offset + 'px');
          if (slideContainer.children('.item').length == 2) {
            slideContainer.children('.item:first').remove();
          }
          currentSlide = slide;
          syncLegendVisibility(true)
        }
            
      }); // end image on load
		} // end display slide

		var keyUpHandler = function(e) {
			e.preventDefault();
			switch (e.keyCode) {
				case 27 :
					close();
					break;
				case 37 :
					previousSlide();
					break;
				case 39 :
					nextSlide();
					break;
			}
		};
		
		var currentPos = 0;
    var effectDuration = 800;
    var supportEffects = getPrefix('transition') !== false;
    
    var gallery = $('<div id="gallery"></div>');
    $('body').append(gallery);

    var slideContainer = $('<div class="content-w"></div>');
    gallery.append(slideContainer);

    var nav = $('<nav><button class="prev">prev</button><button class="next">next</button><button class="close">close</button></nav>');
    
		
    if (supportEffects) {
      createEffectStyle();
    }
		displaySlide(0, true);
		// displaySlide(1);
		$(document).bind('keyup', keyUpHandler);
		$(document).bind('mousemove', mouseMove);
		$(window).bind('resize', onResize);
		gallery.click(function (e) {
			if (e.srcElement == gallery[0]) {
        close();
      }
		})
	}

	$.fn.extend({

				oxGallery : function() {

					if (typeof($(this).attr('data-url')) !== 'undefined') {

						$.get($(this).attr('data-url'), function(data, success,
										request) {
									initGallery($(data)
											.filter('div[data-img-src]'));
								})

					} else {
						initGallery($(this).filter('div[data-img-src]'));
					}

					return $(this);
				}

			});

})(jQuery);
