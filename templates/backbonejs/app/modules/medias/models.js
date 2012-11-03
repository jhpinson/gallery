define([
// Application.
"app",

],

// Map dependencies from above array.

function(app) {

  var Models = {};

  // Default model.
  Models.Media = Backbone.Model.extend({
    urlRoot: '/rest/medias',

    // Ensure that each todo created has `title`.
    initialize: function() {},

    get_url : function () {
      if (this.get('is_an_album') == 1) {
        return '/album/' + this.get('id') + '/';
      }
    },

    clear: function() {
      this.destroy();
    }
  });

  // Default collection.
  Models.Medias = queryEngine.QueryCollection.extend({
    url: '/rest/medias',
    // Reference to this collection's model.
    model: Models.Media
  });

  // Return the module for AMD compliance.
  return Models;

});