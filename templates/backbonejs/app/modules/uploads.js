define([
// Application.
"app", ],

function(app) {

  // Create a new module.
  var Uploads = app.module();

  var filesAdded = function(e, data) {
    $.each(data.files, function(index, file) {
      var li = $('<li id="' + fileToId(file) + '" ><h6>' + file.name + '</h6></li>')
      $('#upload-details').append(li);

    });
  };

  Uploads.init = function() {


    $('body').fileupload({
      dataType: 'json',
      fileInput: $('#fileUploadInput'),
      sequentialUploads: true,
      limitConcurrentUploads: 1,
      url: '/p/upload/',

      //change : filesAdded,
      //drop : filesAdded,
      /*
        done : function(e, data) {
          setTimeout(function () {
            var name = fileToId(data.files[0]);
            $('#upload-manager #'+ name +' .progress').removeClass('active');
            $('#upload-manager #'+ name +' .progress').addClass('progress-success');
           $('#' + name).fadeOut(200, function() {
           $(this).remove();
          })}, 1000);
        },*/
      /*
      fail: function(e, data) {
        msgError(data.jqXHR.responseText);
      },

      start: function(e, data) {
        $('#upload-manager').show();

      },

      send: function(e, data) {
        $('#progressall').removeClass('progress-success');
        var name = fileToId(data.files[0]);
        //$('#' + name).append('<div  class="progress"  ><div  class="bar" style="width: 0;"></div></div>');
        $('#upload-manager h5 span').text(data.files[0].name);
      },

      stop: function() {
        var url = document.location.href.split('#')[0];
        if(url.indexOf('?') !== -1) {
          url += '&thumbnails'
        } else {
          url += '?thumbnails'
        }

        $('#upload-manager').fadeOut(200, function() {
          $('#upload-manager').hide();
          $('#upload-details').empty()
        });

        $('#thumbnails').fadeOut(200, function() {
          $('#thumbnails').load(url, function() {
            //$('img.thumbnail-pending').generateThumbnails()
            $('#thumbnails').fadeIn(200);
          });
        });



      },

      progress: function(e, data) {
        var name = fileToId(data.files[0]);
        var progress = parseInt(data.loaded / data.total * 100, 10);
        if(progress == 100) {
          $('#progressall').addClass('progress-success');
        }

      },

      progressall: function(e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#upload-manager #progressall .bar').css('width', progress + '%');
      }*/
    });

    $('body').bind('fileuploadsubmit', function(e, data) {

      if(typeof(data.formData) === 'undefined') {
        data.formData = {};
      }
      data.formData.album = app.currentAlbumId;

      for(var i = 0, l = data.files.length; i < l; i++) {
        data.formData[data.files[i].name] = data.files[i].lastModifiedDate.toJSON();
      }

    });
  }

  return Uploads;

});