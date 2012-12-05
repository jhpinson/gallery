define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {

  var Views = {};


  Views.GlobalUpload = Backbone.View.extend({
    template: 'uploads/header',

    events: {
      "mouseover": "open",
      "mouseout": "close",
    },

    initialize: function() {
      this.model.bind('all', this.render, this);
    },

    displayProfileMenu: null,

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    open: function() {
      var img_offset = this.$el.children('.upload-button').offset();
      this.$el.children('ul').css({
        'right': ($('body').width() - (img_offset.left + this.$el.children('.upload-button').width())) + 'px',
        'top': (img_offset.top + this.$el.children('.upload-button').height() + 10) + 'px'
      })
      this.$el.children('ul').fadeIn(200);
      if(this.displayProfileMenu !== null) {
        clearTimeout(this.displayProfileMenu);
        this.displayProfileMenu = null;
      }
    },

    close: function() {
      if(this.displayProfileMenu !== null) {
        clearTimeout(this.displayProfileMenu);
        this.displayProfileMenu = null;
      }

      this.displayProfileMenu = setTimeout(_.bind(function() {
        this.$el.children('ul').fadeOut(200);
      },this), 400)
    }

  });


  return Views;

});