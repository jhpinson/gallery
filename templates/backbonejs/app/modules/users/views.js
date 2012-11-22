define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {

  var Views = {};


  Views.Logged = Backbone.View.extend({
    template: 'users/logged',

    events: {
      "mouseover": "open",
      "mouseout": "close",
    },

    displayProfileMenu: null,

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    open: function() {
      var img_offset = this.$el.children('img').offset();
      this.$el.children('ul').css({
        'right': ($('body').width() - (img_offset.left + this.$el.children('img').width())) + 'px',
        'top': (img_offset.top + this.$el.children('img').height() + 10) + 'px'
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