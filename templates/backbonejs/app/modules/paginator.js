define([
// Application.
"app"],

// Map dependencies from above array.

function(app) {

  // Create a new module.
  var Paginator = app.module();

  // Default model.
  Paginator.Paginator = Backbone.Model.extend({

    _collection: null,

    defaults: {
      "limit": 25,
      "pages": 1,
      "current": 1,
      "url": null,
      "prev" : false,
      "next" : false
    },

    hasNext : function () {
      return this.get('current') < this.get('pages')
    },

    hasPrev : function () {
      return this.get('current') > 1
    },

    initialize: function(attributes, collection) {
      this._collection = collection;
      this.page = this._collection.createLiveChildCollection();

      this._collection.bind('all', function() {
        this._compute();
      }, this);
      this.bind('change:current', this._compute, this);
      this.bind('change:limit', this._compute, this);
      this._compute();
    },

    _compute: function() {
      this.set("pages", parseInt((this._collection.length / this.get('limit'))) + ((this._collection.length % this.get('limit') > 0) ? 1 : 0));
      if(this.get('current') > this.get('pages')) {
        var qs = document.location.search;
        qs = qs.replace('page=' + this.get('current'), 'page=1');
        app.router.navigate(document.location.pathname+qs, {trigger:true, replace:true});
        return;
      }
      this.page.query({
        limit: this.get('limit'),
        page: this.get('current')
      });

      if (this.hasNext()) {
        this.set('next', document.location.pathname + '?page=' + (parseInt(this.get('current')) + 1));
      } else {
        this.set('next', false);
      }

      if (this.hasPrev()) {
        this.set('prev', document.location.pathname + '?page=' + (parseInt(this.get('current')) - 1));
      } else {
        this.set('prev', false);
      }
    }

  });
  Paginator.View = Backbone.View.extend({
    tagName : 'span',
    template : 'pagination',

    initialize : function () {
      this.model.bind('all', this.render, this);
    },

    serialize: function() {
      return {paginator : this.model.toJSON()};
    }

  });

  // Return the module for AMD compliance.
  return Paginator;

});