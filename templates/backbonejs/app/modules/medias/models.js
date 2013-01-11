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

    localAttributes : ["selected", "running", "year", "month", "day", "full_date", "short_date", "absolute_uri"],

    defaults: {
      "selected": false,
      "running" : false
    },

    // Ensure that each todo created has `title`.
    initialize: function() {

      this.compute_date();
      this.on('change:date', _.bind(this.compute_date, this))
      this.on('sync', _.bind(this.compute_absolute_uri, this))

      this.compute_absolute_uri()
    },

    startRunning : null,
    stopRunning : null,

    compute_absolute_uri : function () {
      this.set('absolute_uri', this.get_uri());
    },

    compute_date: function() {
      if(this.get('date')) {
        var date = Date.parse(this.get('date'));
        this.set('year', date.getFullYear());
        this.set('month', date.getMonth());
        this.set('day', date.getDate());
        this.set('full_date', date.toString('dddd d MMMM yyyy \à H:mm'));
        this.set('short_date', date.toString('d MMM yyyy, H:mm'));
      }
    },

    get_uri: function() {
      if(this.get('is_an_album') == 1) {
        return '/album/' + this.get('id') + '/';
      }
    },

    rotate: function(value, callback) {

      var url = this.url() + '/rotate';
      $.ajax({
        url: url,
        type: 'PUT',
        dataType: 'application/json',
        contentType: 'application/json',
        data: JSON.stringify({
          value: value
        }),
        context: this,
        'complete': function(xhr) {

          if(typeof(callback) !== 'undefined') {
            callback(JSON.parse(xhr.responseText));
          }


        }
      });
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