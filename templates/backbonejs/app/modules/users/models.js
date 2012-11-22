define([
// Application.
"app",

],

// Map dependencies from above array.

function(app) {

  var Models = {};

  // Default model.
  Models.User = Backbone.Model.extend({
    urlRoot: '/rest/users',

    // Ensure that each todo created has `title`.
    initialize: function() {

      this.set('absolute_uri', this.get_uri());

    },

    get_uri : function () {
      return '/users/' + this.get('id') + '/';
    },

    clear: function() {
      this.destroy();
    }
  });


  // Return the module for AMD compliance.
  return Models;

});