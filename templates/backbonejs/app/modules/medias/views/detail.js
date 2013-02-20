define([
// Application.
"app", "modules/medias/views/mixins/image-ops"

],

// Map dependencies from above array.

function(app, ImageOpsMixin) {
  return Backbone.View.extend(_.extend({
    template: 'medias/detail',

    thumb_size: 'medium',

    events: {
      "click .remove": "mRemove",
      "click .restore": "restore",
      "click .rotate": "rotate",
      "mouseover": "show",
      "mouseout": "hide",
    },

    initialize: function() {
      this.model.bind('all', this.render, this);
    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    render: function(template, context) {
      var context = context || {};
      context = _.extend({}, context, {
        paginator: this.paginator
      });
      return template(context);
    },

    displayOnMouseOver: null,
    show: function() {

      this.$el.find('.appear-on-mouseover:not(.persist)').fadeIn(200);

      if(this.displayOnMouseOver !== null) {
        clearTimeout(this.displayOnMouseOver);
        this.displayOnMouseOver = null;
      }
    },

    hide: function() {


      if(this.displayOnMouseOver !== null) {
        clearTimeout(this.displayOnMouseOver);
        this.displayOnMouseOver = null;
      }

      this.displayOnMouseOver = setTimeout(_.bind(function() {
        this.$el.find('.appear-on-mouseover:not(.persist)').fadeOut(200);
      }, this), 200)
    }

    /*afterRender: function() {
      $('.image-wrapper').css({
        height: ($(window).height() - 124) + 'px'
      });
    }*/

  }, ImageOpsMixin));
});