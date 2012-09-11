
(function($) {
  var tasks = [];
  
  var generateNextThumbnail = function () {
  	
  	var el = tasks.shift();
    if (typeof(el) === 'undefined') {
      return;
    }
  	
    $.ajax({
        url: $(el).attr('data-generate'),
        context : $(el)
        
      }).done(function(response, status, request) { 
      	generateNextThumbnail();
        $(this).attr('src', response.url);
        $(this).attr('width', response.width);
        $(this).attr('height', response.height);
        $(this).removeClass('thumbnail-pending');
       
      });
  }
  
  $.fn.extend({

        generateThumbnails : function() {

          $(this).each(function (idx, el) {
          	tasks.push(el);
          })
          
          generateNextThumbnail();
          
          return $(this);
        }
      });
})(jQuery);


$(window).load(function() {

	$('img.thumbnail-pending').generateThumbnails()
	
});