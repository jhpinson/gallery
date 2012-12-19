define([
// Application.
"app", "plugins/async"

],

// Map dependencies from above array.

function(app, async) {

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

  Views.Selection = Backbone.View.extend({
    template: 'medias/selection',

    events: {
      "click .select-all": "selectAll",
      "click .unselect-all": "unSelectAll",
      "click .revert-selection": "revertSelection",
      "click .remove": "mRemove",
      "click .restore": "restore",
      "click .rotate": "rotate",
      "click .move": "move"
    },

    selectAll: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      app.paginator.page.each(function(o, id, col) {
        var silent = id < col.length - 1;
        o.set({
          'selected': true
        });
      })
    },

    unSelectAll: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      app.paginator.page.each(function(o, id, col) {
        var silent = id < col.length - 1;
        o.set({
          'selected': false
        });
      })
    },

    revertSelection: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      app.paginator.page.each(function(o, id, col) {
        var silent = id < col.length - 1;
        o.set({
          'selected': !o.get('selected')
        });
      })
    },

    mRemove: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      var methods = [];

      this.collection.each(function(obj, id, col) {
        obj.set('running', true);
        methods.push(_.bind(function(callback) {

          obj.set({
            status: 'deleted'
          }, {
            silent: true
          });

          obj.save().then(function() {
            /*obj.set({
              running: false
            });*/
            obj.set('running', false);
            callback(null, obj);
          });
        }, this))


      });
      async.series(methods, function(err, results) {
        //app.medias.remove(results);
      });
    },


    restore: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      var methods = [];

      this.collection.each(function(obj, id, col) {
        obj.set('running', true);
        methods.push(_.bind(function(callback) {

          obj.set({
            status: 'published'
          }, {
            silent: true
          });


          obj.save().then(function() {
            obj.set('running', false);
            callback(null)
          });
        }, this))


      });

      async.series(methods, function(err, results) {
        //alert('done')
      });

    },

    rotate: function(event) {

      event.preventDefault();
      event.stopImmediatePropagation();
      var value = $(event.currentTarget).attr('data-rotate') || $(event.originalEvent.srcElement).attr('data-rotate');
      var thumb_size = $(event.currentTarget).attr('data-thumb-size') || $(event.originalEvent.srcElement).attr('data-thumb-size');
      var methods = [];
      this.collection.each(function(obj, id, col) {
        obj.set('running', true);
        methods.push(_.bind(function(callback) {
          obj.rotate(value, _.bind(function(response) {
            var $img = $('img[data-media-pk="' + obj.get('id') + '"]');
            $img.fadeOut(200, _.bind(function() {
              response['url_' + this.thumb_size] += '?' + Math.random();
              $img.attr('src', response['url_' + this.thumb_size]);
              $img.attr('width', response['width_' + this.thumb_size]);
              $img.attr('height', response[+'height_' + this.thumb_size]);
              $img.fadeIn(200, _.bind(function() {
                obj.set(response, {
                  silent: true
                });
                obj.set('running', false);
                callback(null);
              }, this));


            }, this));

          }, this));
        }, this))


      },this);

      async.series(methods, function(err, results) {
        //alert('done')
      });

    },

    move: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      var methods = [];

      this.collection.each(function(obj, id, col) {
        obj.set('running', true);
        methods.push(_.bind(function(callback) {
          setTimeout(_.bind(function() {
            obj.set('running', false);
            callback(null, obj);
          }, this), 200)


        }, this));

      });
      async.series(methods, _.bind(function(err, results) {
        app.medias.remove(results);
      }, this));
    },

    initialize: function() {
      this.collection.bind('all', this.render, this);

    },

    render: function(template, context) {

      context = {
        hasSelected: this.collection.length > 0
      }
      context.hasDeleted = this.collection.where({
        status: 'deleted'
      }).length > 0;
      context.hasPublished = this.collection.where({
        status: 'published'
      }).length > 0

      return template(context);
    }

  })

  Views.SideBar = Backbone.View.extend({
    template: 'medias/sidebar',

    _facetting: null,
    _selectionView: null,
    initialize: function(options) {
      //this._facetting = options.facetting;
      this._collection = options.collection;
      this._collection.bind('all', this.onCollectionChange, this);
      this._facetting = this._computeFacetting();

      // reset
      this.paginator = app.paginator;
      this.paginator.bind('change:current', this.resetSelectionView, this);
    },

    onCollectionChange: function() {
      var facetting = this._computeFacetting();
      if(JSON.stringify(this._facetting) != JSON.stringify(facetting)) {
        this._facetting = facetting;
        this.render();
      }
    },

    _getQueryVariable: function(variable, defaut) {
      var query = window.location.search.substring(1);
      var vars = query.split("&");
      for(var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable) {
          return unescape(pair[1]);
        }
      }
      return defaut || null;
    },

    _getFacetUrl: function(facets, facetAdd, facetRemove) {
      var qs = decodeURIComponent(document.location.search);
      if(qs == '') {
        qs = '?'
      }

      if(facetAdd !== null) {
        if(facets == null) {
          facets = 'facets=' + facetAdd;
          if(qs == '?') {
            qs += facets;
          } else {
            qs += '&' + facets;
          }
        } else {
          qs = qs.replace(facets, facets + ' ' + facetAdd);
        }
      }

      if(typeof(facetRemove) !== 'undefined') {
        var _facets = facets.replace(facetRemove, '');
        var name = facetRemove.split(':')[0];
        if(name == 'month' || name == "year") {
          _facets = _facets.replace(/day:[0-9]{1,2}/, '');
        }

        if(name == "year") {
          _facets = _facets.replace(/month:[0-9]{1,2}/, '');
        }

        qs = qs.replace(facets, _facets);
        if(_facets.trim().length == 0) {
          qs = qs.replace('facets=', '');
        }
      }


      // clean qs
      qs = qs.replace('&&', '&');
      qs = qs.replace(/&$/, '');
      qs = qs.replace('?&', '?');
      if(qs.trim() == '?') {
        qs = '';
      }

      return document.location.pathname + qs;
    },


    _getDate: function(year, month, day) {
      var d = new Date();
      d.setFullYear(year);

      if(typeof(month) !== 'undefined') {
        d.setMonth(month);
      }

      if(typeof(day) !== 'undefined') {
        d.setDate(day);
      }

      return d;
    },

    _computeFacetting: function() {

      var facetsQs = this._getQueryVariable('facets');

      var facetting = {
        years: {},
        months: {},
        days: {},
        deleted: 0
      };

      this._collection.getParentCollection().forEach(function(media) {
        if(media.get('status') == 'deleted') {
          facetting.deleted++;
        }
      }, this);

      this._collection.forEach(function(media) {

        // years
        if(typeof(facetting.years[media.get('year')]) !== 'undefined') {
          facetting.years[media.get('year')]++;
        } else {
          facetting.years[media.get('year')] = 1;
        }

        // month
        if(typeof(facetting.months[media.get('month')]) !== 'undefined') {
          facetting.months[media.get('month')]++;
        } else {
          facetting.months[media.get('month')] = 1;
        }

        // day
        if(typeof(facetting.days[media.get('day')]) !== 'undefined') {
          facetting.days[media.get('day')]++;
        } else {
          facetting.days[media.get('day')] = 1;
        }
      }, this);

      var facets = {};

      // dealing with dates
      var d = new Date();

      facets.deleted = {
        name: 'supprimé',
        url: this._getFacetUrl(facetsQs, 'status:all'),
        value: facetting.deleted
      }

      var years = _.keys(facetting.years);
      if(years.length > 1) {
        facets.years = [];
        _.each(years, function(year) {
          facets.years.push({
            name: year,
            url: this._getFacetUrl(facetsQs, 'year:' + year),
            value: facetting.years[year]
          })
        }, this);
      } else {
        d.setFullYear(years[0]);
        // month
        var months = _.keys(facetting.months);
        if(months.length > 1) {
          facets.months = [];
          _.each(months, function(month) {
            facets.months.push({
              name: this._getDate(years[0], month).toString('MMMM yyyy'),
              url: this._getFacetUrl(facetsQs, 'month:' + month),
              value: facetting.months[month]
            })
          }, this);
        } else {
          // days
          var days = _.keys(facetting.days);
          if(days.length > 1) {
            facets.days = [];
            _.each(days, function(day) {
              facets.days.push({
                name: this._getDate(years[0], months[0], day).toString('ddd d MMMM yyyy'),
                url: this._getFacetUrl(facetsQs, 'day:' + day),
                value: facetting.days[day]
              })
            }, this);
          }
        }
      }

      var currents = [];
      // active facets
      if(facetsQs !== null) {

        _.each(facetsQs.split(/\s+/), function(facet) {
          var split = facet.split(':');
          var name = split[1];
          if(split[0] == 'status' && name == 'all') {
            name = 'éléments supprimés';
            delete facets.deleted;
          }
          if(split[0] == 'month') {
            name = this._getDate(years[0], split[1]).toString('MMMM yyyy');
          } else if(split[0] == 'day') {
            name = this._getDate(years[0], months[0], split[1]).toString('ddd d MMMM yyyy')
          }
          currents.push({
            name: name,
            url: this._getFacetUrl(facetsQs, null, facet)
          });
        }, this);
      }

      return {
        currents: currents,
        facets: facets,
        qs: facetsQs
      };

    },

    render: function(template, context) {
      var context = context || {};
      context = _.extend({}, context, {
        facetting: this._facetting
      });
      return template(context);
    },

    afterRender: function() {
      this.resetSelectionView();
    },

    resetSelectionView: function() {
      // if there is no album display currently
      if(app.page.value === null) {
        return;
      }

      if(this._selectionView !== null) {
        this._selectionView.remove();
        this._selectionView = null;

        app.paginator.page.each(function(o, id, col) {
          o.set({
            'selected': false
          });
        });
      }

      var selectionView = new Views.Selection({
        collection: this.paginator.page.createLiveChildCollection().setPill('selected', {
          prefixes: ['selected:'],
          callback: function(model, value) {
            return model.get('selected') == true;
          }
        }).setSearchString('selected:true').query()
      });
      this._selectionView = selectionView;
      this.$el.append(selectionView.$el);
      selectionView.render();
    }
  });

  var ImageOps = {

    mask: null,

    rotate: function(event) {

      event.preventDefault();
      event.stopImmediatePropagation();

      this.model.set({
        running: true
      });

      var value = $(event.currentTarget).attr('data-rotate') || $(event.originalEvent.srcElement).attr('data-rotate');

      this.model.rotate(value, _.bind(function(response) {
        var $img = this.$el.find('img[data-media-pk]');
        $img.fadeOut(200, _.bind(function() {

          response['url_' + this.thumb_size] += '?' + Math.random();
          $img.attr('src', response['url_' + this.thumb_size]);
          $img.attr('width', response['width_' + this.thumb_size]);
          $img.attr('height', response[+'height_' + this.thumb_size]);
          $img.fadeIn(200);

          this.model.set(response, {
            silent: true
          });
          this.model.set('running', false);

        }, this));

      }, this));
    },

    _applyStatus: function(status, callback) {
      this.model.set({
        'status': status
      }, {
        silent: true
      });
      this.model.save().then(callback);
    },

    mRemove: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set({
        running: true
      });
      //this._applyMask();
      this._applyStatus('deleted', _.bind(function() {
        this.model.set('running', false);
      }, this));
    },

    restore: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set({
        running: true
      });
      this._applyStatus('published', _.bind(function() {
        this.model.set('running', false);
      }, this));
    },

    toggleSelect: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set('selected', !this.model.get('selected'));
    }

  };

  Views.Detail = Backbone.View.extend(_.extend({
    template: 'medias/detail',

    thumb_size: 'medium',

    events: {
      "click .remove": "mRemove",
      "click .restore": "restore",
      "click .rotate": "rotate",
      "mouseover" : "show",
      "mouseout" : "hide",
    },

    initialize: function() {
      this.model.bind('all', this.render, this);
    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    render : function (template, context) {
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

  }, ImageOps));

  Views.Item = Backbone.View.extend(_.extend({

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
    },

    initialize: function() {

      this.model.bind('change', this.render, this);
    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
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
  }, ImageOps));



  Views.Items = Backbone.View.extend({

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