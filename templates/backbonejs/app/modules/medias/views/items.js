define([
// Application.
"app",  "modules/medias/views/item"

],

// Map dependencies from above array.

function(app, Item) {
  return Backbone.View.extend({

    _length: null,

    initialize: function(options) {
      //options.paginator.bind('change:current', this.render, this);
      this.collection.bind('haschange', function() {
        this.render();
      }, this);

    },

    tagName: "ul",
    className: "thumbnails",


    beforeRender: function() {

      app.medias.each(function(o, id, col) {
        o.set({
          'selected': false
        });
      });

      this.collection.each(_.bind(function(model, pos) {
        if(model.get('is_an_album') === 1) {
          view = new Item({
            model: model,
            template: 'medias/list/item-album'
          });

        } else {
          view = new Item({
            model: model,
            template: 'medias/list/item-default'

          });

        }
        this.insertView(view);

      }, this));
    }
  });
});