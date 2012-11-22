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

      var date = Date.parse(this.get('date'));

      //var date = (/([0-9]{4})-([0-9]{2})-([0-9]{2})/).exec(this.get('date'));
      this.set('year', date.getFullYear());
      this.set('month', date.getMonth());
      this.set('day', date.getDate());


      this.set('full_date', date.toString('dddd d MMMM yyyy \à H:mm'));
      this.set('short_date', date.toString('d MMM yyyy, H:mm'));

      this.set('absolute_uri', this.get_uri());

    },

    get_uri : function () {
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