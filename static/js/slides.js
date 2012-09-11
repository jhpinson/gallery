$(window).load(function() {

			$('.start-slides').click(function(e) {
				  e.preventDefault();
				  
						$('body').append($('<div id="gallery"></div>'));
						$('#gallery').load($(this).attr('data-url'), function() {
									/*$('#gallery-wrap').camera({
												navigation : true,
												height : '600px',
												imagePath : '../images/',
												loader : 'bar',
												navigationHover : true
											});*/
											
											$('#gallery-wrap').camera({
        height: 'auto',
        loader: 'bar',
        pagination: true,
        thumbnails: true,
        hover: false,
        opacityOnGrid: false,
        imagePath: '../images/'
      });
								});
					})

		});
