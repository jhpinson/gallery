define([
// Application.
"app", "modules/uploads/models","modules/uploads/views", "modules/medias"],

function(app, Models, Views, Medias) {

  // Create a new module.
  var Uploads = app.module();
  app.Uploads = Uploads;

  Uploads.Models = Models;
  Uploads.Views = Views;

  var filesAdded = function(e, data) {
      $.each(data.files, function(index, file) {
        var li = $('<li id="' + fileToId(file) + '" ><h6>' + file.name + '</h6></li>')
        $('#upload-details').append(li);

      });
    };


  Uploads.isEnabled = false;

  Uploads.enable = function() {
    $('body').fileupload('enable');
    Uploads.isEnabled = true;
  };

  Uploads.disable = function() {
    //$('body').fileupload('disable');
    Uploads.isEnabled = false;
  };




  Uploads.init = function() {

    app.uploads = new Uploads.Models.Uploads();
    app.globalUpload = new Uploads.Models.GlobalUpload();

    var view = new Views.GlobalUpload({model : app.globalUpload });
    view.setElement($('#uploads'));
    view.render();

    $('body').fileupload({
      dataType: 'json',
      //fileInput: $('#fileUploadInput'),
      sequentialUploads: true,
      limitConcurrentUploads: 1,
      url: '/p/upload/',

      // global start
      start: function(e, data) {
        app.globalUpload.set('status', 'started');
        app.globalUpload.set('progress', 0);
      },

      // global stop
      stop: function() {
        app.globalUpload.set('status', 'stopped');
        app.globalUpload.set('progress', 0);
      },

      // global progress
      progressall: function(e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        app.globalUpload.set('progress', progress);
      },

      // file done
      done: function(e, data) {
        var upload = app.uploads.getByCid(data.formData.cid);
        upload.set("status", "success");

        app.globalUpload.decrease();

        if (upload.get('album') == app.currentAlbumId) {
          var media = new Medias.Models.Media({id:data.result.id});
          media.fetch().then(function () {
            if (media.get('parent_album') == app.currentAlbumId) {
              app.medias.add(media);
            }
          })
        } else {
          // @ todo remove from uploads
        }

      },

      // file failed
      fail: function(e, data) {
        var upload = app.uploads.getByCid(data.formData.cid);
        upload.set("status", "failed");
        // @ todo remove from uploads
        app.globalUpload.decrease();
      },

      // start file upload
      send: function(e, data) {
        var upload = app.uploads.getByCid(data.formData.cid);
        upload.set("status", "uploading");
      },

      // file progress
      progress: function(e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var upload = app.uploads.getByCid(data.formData.cid);
        upload.set("progress", progress);

      }
    });

    $('body').bind('fileuploadsubmit', function(e, data) {

      if (Uploads.isEnabled === false) {
        return false
      }

      if(typeof(data.formData) === 'undefined') {
        data.formData = {};
      }
      data.formData.album = app.currentAlbumId;
      for(var i = 0, l = data.files.length; i < l; i++) {
        var upload = new Models.Upload({
          name: data.files[i].name,
          size: data.files[i].size,
          album: app.currentAlbumId
        });
        app.uploads.add(upload);
        app.globalUpload.increase();
        data.formData[data.files[i].name] = data.files[i].lastModifiedDate.toJSON();
        data.formData.cid = upload.cid;
      }



    });
  }

  return Uploads;

});