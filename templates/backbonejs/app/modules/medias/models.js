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
    initialize: function() {
      var date = (/([0-9]{4})-([0-9]{2})-([0-9]{2})/).exec(this.get('date'));
      this.set('year', date[1]);
      this.set('month', date[2]);
      this.set('day', date[3]);
    },

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