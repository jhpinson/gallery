define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {
  return Backbone.View.extend({
    template: 'medias/dropbox',

    initialize : function () {

      this.model.bind('change', this.render, this)
      setInterval(_.bind(function () {
        this.model.fetch({url : "/rest/medias/dropbox"});
      },this), 10000);
      this.model.fetch({url : "/rest/medias/dropbox"});
    },

    serialize: function() {

      var object = null;
      if (this.model.get('id') !== 'undefined' && (this.model.get('image_count') > 0 || this.model.get('video_count') > 0 )) {
        object = this.model.toJSON();
      }

      return {
        object: object
      };
    }
  });
});