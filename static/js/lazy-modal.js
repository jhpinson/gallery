$(document).ready(function() {
        

      // popup modal
      $('*[data-modal]').click(function(e) {
            e.preventDefault();
            console.debug('lalalalal')
            var href = $(e.target).attr('href');

            if (typeof(href) === 'undefined') {
              href = $(e.currentTarget).attr('href');
            }
            
            if (href.indexOf('#') == 0) {
              var width = $(e.target).attr('data-width');
              if (typeof(width) !== 'undefined') {
                $(href).css({
                      width : width + 'px',
                      'margin-left' : function() {
                        return -($(this).width() / 2);
                      }
                    });
              }
              $(href).modal('show');
            } else {
            	
            	$('body').append('<div class="modal hide fade" id="modal" style="display:none"></div>')
            	
              var width = $(e.target).attr('data-width');
              if (typeof(width) !== 'undefined') {
                $("#modal").css({
                      width : width + 'px',
                      'margin-left' : function() {
                        return -($(this).width() / 2);
                      }
                    });
              }
              $("#modal").modal('show');
              $("#modal").load(href, function() {
                    setupSubmitForm("#modal");
                  })
            }

          });

      // dajax form
      setupSubmitForm()
      
    });