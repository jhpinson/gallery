define([
// Application.
"app", "modules/medias/views/mixins/image-ops"

],

// Map dependencies from above array.

function(app, ImageOpsMixin) {
  return Backbone.View.extend(_.extend({

    tagName: "li",
    className: "span2",

    thumb_size: 'small',

    events: {
      "mouseover": "show",
      "mouseout": "hide",
      "click .remove": "mRemove",
      "click .restore": "restore",
      "click .rotate": "rotate",
      "click .select": "toggleSelect",
      "click .edit": 'edit'
    },

    initialize: function() {

      this.model.bind('change', this.render, this);
    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    edit: function(event) {

      var form = new Backbone.ModalModelForm({
        template: 'medias/forms/album',
        title: 'Modifier cet album',
        model: this.model,

        onOk: function(album) {

        },

        validate : function (data) {

          form.$modal.find('.control-group').removeClass('error');
          form.$modal.find('.error').remove();

          if (data.name.trim().length == 0) {
            form.$modal.find('#name').parent().append("<span class='help-inline error'>Ce champ est requis</span>");
            form.$modal.find('#name').parents('.control-group').addClass('error');
            return false
          }
          return true;
        }
      })

      form.render();

    },

    displayImageActions: null,
    show: function() {
      if(this.model.get('is_an_album') == 1 || this.mask !== null) {
        return;
      }
      this.$el.find('.action:not(.persist), .legend').fadeIn(200);

      if(this.displayImageActions !== null) {
        clearTimeout(this.displayImageActions);
        this.displayImageActions = null;
      }
    },

    hide: function() {

      if(this.model.get('is_an_album') == 1) {
        return;
      }

      if(this.displayImageActions !== null) {
        clearTimeout(this.displayImageActions);
        this.displayImageActions = null;
      }

      this.displayImageActions = setTimeout(_.bind(function() {
        this.$el.find('.action:not(.persist), .legend').fadeOut(200);
      }, this), 200)
    }
  }, ImageOpsMixin));
});