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
      this.page = this._collection.createLiveChildCollection().setComparator(function(a,b) {
        return Date.parse(a.get('date')) - Date.parse(b.get('date'))
      });

      //var comparator = queryEngine.generateComparator({date : 1})
      //this.page.setComparator(comparator)
      //this.page.sort()

      //this._collectionHash = this._getCollectionHash();

      this._collection.bind('add remove reset', this._compute, this);
      /*
      this._collection.bind('all', function (e) {
        console.debug(e)
        if (['change', 'sync', 'request'].indexOf(e) !== -1) {
          console.debug(arguments)
          this._compute();
        }
      }, this);
      */
      this.bind('change:current', this._compute, this);
      this.bind('change:limit', this._compute, this);
      this._compute();

    },

    _getCollectionHash : function () {
      var hash = [];
      this.page.each(function (obj) {
        hash.push(obj.cid);
      });

      return hash.join('-');
    },

    _getPageUrl : function (page) {
        var qs = document.location.search;
        if (qs.indexOf('page=') !== -1) {
          qs = qs.replace(/page=[0-9]+/, 'page=' + page);
        } else if (qs.length > 1) {
          qs += '&page=' + page;
        } else {
          qs = '?page=' + page;
        }

        return document.location.pathname + qs;
    },

    _compute: function() {

      var pages = parseInt((this._collection.length / this.get('limit'))) + ((this._collection.length % this.get('limit') > 0) ? 1 : 0);
      if (pages == 0) {
        pages = 1;
      }
      this.set("pages", pages);

      if(this.get('current') > this.get('pages') && this._collection._runningXHR == false) {
        var qs = document.location.search;
        qs = qs.replace('page=' + this.get('current'), 'page=1');
        app.router.navigate(document.location.pathname+qs, {trigger:true, replace:true});
        return;
      }

      this.page.sortCollection();
      this.page.query({
        limit: this.get('limit'),
        page: this.get('current')
      });
      if (this.hasNext()) {
        //this.set('next', document.location.pathname + '?page=' + (parseInt(this.get('current')) + 1));
        this.set('next', this._getPageUrl(parseInt(this.get('current')) + 1));
      } else {
        this.set('next', false);
      }

      if (this.hasPrev()) {
        this.set('prev', this._getPageUrl(parseInt(this.get('current')) - 1));
      } else {
        this.set('prev', false);
      }

      var newHash = this._getCollectionHash();
      if (this._collectionHash != newHash) {
        this._collectionHash = newHash;
        this.page.trigger('haschange');
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