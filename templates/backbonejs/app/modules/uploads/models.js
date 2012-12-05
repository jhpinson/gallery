define([
// Application.
"app",

],

// Map dependencies from above array.

function(app) {

  var Models = {};

  // Default model.
  Models.Upload = Backbone.Model.extend({

    defaults: {
      "status": "pending", // pending, uploading, success, failed
      "progress" : 0,
      "size" : null,
      "name" : null,
      "album" : null
    },

    initialize : function () {
      this.on('change:progress', function(model, progress) {
        console.debug("progress", this.cid, progress)
      });

      this.on('change:status', function(model, status) {
        console.debug("status", this.cid, status)
      });
    }

  });

  Models.GlobalUpload = Backbone.Model.extend({

    defaults: {
      "status": "stopped", // stopped, started
      "progress" : 0,
      "count" : 0
    },

    initialize : function () {
      this.on('change:progress', function(model, progress) {
        console.debug("global progress", this.cid, progress)
      });

      this.on('change:status', function(model, status) {
        console.debug("global status", this.cid, status)
      });
    },

    decrease : function () {
      this.set("count", this.get("count") - 1);
    },

    increase : function () {
      this.set("count", this.get("count") + 1);
    }

  });

  // Default collection.
  Models.Uploads = queryEngine.QueryCollection.extend({
    model: Models.Upload

  });

  // Return the module for AMD compliance.
  return Models;

});