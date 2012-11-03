define([
// Application.
"app",

"modules/medias/models", "modules/medias/views", ],

// Map dependencies from above array.


function(app, Models, Views) {

  // Create a new module.
  var Medias = app.module();

  Medias.Views = Views;
  Medias.Models = Models;

  //app.medias = new Models.Medias();

  //app.qMedias = queryEngine.createCollection(app.medias)
  /*app.childMedias = app.medias.createLiveChildCollection().setFilter('search', function(model, searchString) {
          var pass, searchRegex;
          searchRegex = queryEngine.createSafeRegex(searchString);
          pass = searchRegex.test(model.get('name'));
          return pass;
        });*/
  // Return the module for AMD compliance.
  return Medias;

});