define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {

  var Views = {};


  Views.Header = Backbone.View.extend({
    template: 'medias/header',

    _breadcrumbs: null,

    initialize: function(options) {
      this._breadcrumbs = options.breadcrumbs;
      this._breadcrumbs.bind('reset', this.render, this);
    },

    render: function(template, context) {
      var context = context || {};
      context = _.extend({}, context, {
        breadcrumbs: this._breadcrumbs
      });
      return template(context);
    }

  });

  Views.SideBar = Backbone.View.extend({
    template: 'medias/sidebar',

    _facetting: null,

    initialize: function(options) {
      this._facetting = options.facetting;
    },

    render: function(template, context) {
      var context = context || {};
      context = _.extend({}, context, {
        facetting: this._facetting
      });
      return template(context);
    }

  });

  Views.Detail = Backbone.View.extend({
    template: 'medias/detail',
    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },
  });

  Views.Item = Backbone.View.extend({

    tagName: "li",
    className: "span2",

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    _afterFlip: function() {
      var $li = this.$el.parents('li');
      if($li.hasClass('flipper')) {
        $li.find('.front').remove()
        $li.find('.back').removeClass('back');
        $li.removeClass('flipper');

      }
    },

    afterRender: function() {
      if(this.$el.parents('li.span2').find('>div').length == 2) {
        setTimeout(_.bind(function() {
          this.$el.parents('li.span2').addClass('flipper');

          setTimeout(_.bind(this._afterFlip, this), 100);

        }, this), 100);
      }
    }
  });



  Views.Items = Backbone.View.extend({

    initialize: function() {
      this.collection.bind('all', this.render, this);
    },

    tagName: "ul",
    className: "thumbnails",


    beforeRender: function() {
      this.collection.each(_.bind(function(model, pos) {
        if(model.get('is_an_album') === 1) {
          view = new Views.Item({
            model: model,
            template: 'medias/list/item-album'
          });

        } else {
          view = new Views.Item({
            model: model,
            template: 'medias/list/item-default'

          });

        }
        this.insertView(view);
      }, this));


    }
  });

  return Views;

});