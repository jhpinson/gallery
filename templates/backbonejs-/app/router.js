define([
  // Application.
  "app",
  "modules/medias"
],

function(app, medias) {

  // Defining the application router, you can attach sub routers here.
  var Router = Backbone.Router.extend({
    routes: {
      "": "albums",
      "album/:id/" : 'album'
    },

    albums: function() {
    	$("body").empty().append(medias.layout.el);
      medias.layout.render();
      
      medias.collection.fetch({
            data : {
              is_an_album : 1
            }
          });
          
    },
    
    album : function (id) {
    	medias.collection.fetch({
            data : {
              parent_album_id : id
            }
          });
    }
  });

  return Router;

});
