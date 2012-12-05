define([
// Application.
"app", "modules/medias", "modules/users", "modules/views", "modules/paginator", "modules/uploads"],

function(app, Medias, Users, Views, Paginator, Uploads) {

  // Defining the application router, you can attach sub routers here.
  var Router = Backbone.RouteManager.extend({


    before: {
      "": ["_clean", "preloadMedias", "preloadBreadcrumbs"],
      "?*qs": ["_clean", "preloadMedias", "preloadBreadcrumbs"],
      "album/:id/*qs": ["_clean", "preloadMedias", "preloadBreadcrumbs"],
      "media/:albumId/*qs": ["_clean", "_preloadMediaDetail"]

    },

    routes: {
      "": "albums",
      "?*qs": "albums",
      "album/:id/*qs": 'album',
      "media-redirect/:id/": 'mediaRedirect',
      "media/:albumId/*qs": 'mediaDetail',
    },



    /*
     * #########################################################################################
     * Utils
     * #########################################################################################
     */


     _clean : function () {
        Uploads.disable();
        app.currentAlbumId = null;
     },

    /*
     * Return true if this is the first time the album or its content is loaded
     */
    _isFirstMediaDisplay: function() {
      var params = this.router ? this.router.params : this.params
      return app.page === null || app.page.type !== 'album' || app.page.value !== params.id
    },

    _hasFacetsChanged : function () {
      return app.page !== null && app.page.facetsQS !== this._getQueryVariable('facets')
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

    /*
     * Render a new layout and animate transition
     */
    _removeOldLayoutTimer: null,
    _renderLayout: function(layoutOptions, dest, options) {
      var options = options || {};
      var currentLayout = app.layout || null;

      // clear timer that remove old layout
      if(this._removeOldLayoutTimer !== null) {
        clearTimeout(this._removeOldLayoutTimer);
        this._removeOldLayoutTimer = null;
      }
      // remove old layout id needed
      $('[data-delete]').remove();

      // remove transition classes on current layout
      $('.main-container>div').attr('class', "");

      layoutOptions.afterRender = _.bind(function(layout) {

        if(currentLayout !== null) {

          // mark current layout to delete it
          currentLayout.$el.attr('data-delete', "");

          // setup transition effects
          if(app.supportEffects) {

            var cssClass = null;
            var source = app.page;

            if (dest.type == source.type && source.type == 'album' && dest.value == source.value ) {
              var destFacetCount = 0, sourceFacetCount = 0;
              if (dest.facetsQS !== null) {
                destFacetCount = dest.facetsQS.split(/\s/).length
              }
              if (source.facetsQS !== null) {
                sourceFacetCount = source.facetsQS.split(/\s/).length
              }
              if ( destFacetCount > sourceFacetCount) {
                  cssClass = 'vertical-down';
              } else {
                cssClass = 'vertical-up';
              }
            } else if (dest.type == 'album' && dest.value == null) {
              cssClass = 'vertical-up';
            } else if(dest.type == 'media' && source.type == 'media' && source.value == dest.value) {
              if(dest.page < source.page) {
                cssClass = 'horizontal-left';
              } else {
                cssClass = 'horizontal-right';
              }
            } else if(source.type == 'media' && dest.type == 'album') {
              cssClass = 'vertical-up';
            } else {
              cssClass = 'vertical-down';
            }

            layout.$el.addClass(" offset-" + cssClass);
            layout.$el.show();

            currentLayout.$el.addClass("out-" + cssClass);
            layout.$el.addClass("in-" + cssClass);

            // remove old layout
            this._removeOldLayoutTimer = setTimeout(_.bind(function() {
              $('[data-delete]').remove();
              this._removeOldLayoutTimer = null;
            }, this), 1000);
          }
          // browser doesn't support effects
          else {
            currentLayout.remove();
            layout.$el.show();
          }

        }

        if(source) {
          $('body').removeClass(source.type);
        }
        $('body').addClass(dest.type);

        // store new page description
        app.page = dest;
      }, this);

      // create layout and render it
      var layout = app.useLayout(layoutOptions)
      if(currentLayout !== null) {
        layout.$el.hide();
      }
      $('.main-container').append(layout.$el);
      layout.render();

    },

    /*
     * #########################################################################################
     * Breadcrumbs
     * #########################################################################################
     */

    /*
     * Load breadcrumb for an album
     */
    preloadBreadcrumbs: function() {
      if(this.router._isFirstMediaDisplay) {

        var b = this.router._preloadBreadcrumbs(this.router.params.id);
        if(b !== null) {
          var deferred = this.defer();
          b.fetch().then(function() {
            deferred.resolve();
          });;

        }
      }
    },

    /*
     * Load breadcrumb for media that is not an album
     */
    preloadMediaBreadcrumbs: function() {
      var params = this.router ? this.router.params : this.params

      var b = this.router._preloadBreadcrumbs(params.id);
      if(b !== null) {
        var deferred = this.defer();
        b.fetch().then(function() {
          deferred.resolve();
        });;

      }

    },

    /*
     * generic breadcrumb load
     */
    _preloadBreadcrumbs: function(id) {

      var breadcrumbs = new Backbone.Collection({
        model: Medias.Models.Media
      });
      app.breadcrumbs = breadcrumbs;


      if(id !== null && typeof(id) !== 'undefined') {
        var url = '/rest/medias/' + id + '/ancestors';
        breadcrumbs.url = url;
        return breadcrumbs;
      }

      return null;
    },

    /*
     * #########################################################################################
     * Single media
     * #########################################################################################
     */

    /*
     * Redirect to album page for this media
     */
    mediaRedirect: function(id) {
      if(app.medias && app.medias.get(id)) {
        var media = app.medias.get(id);
        var pos = app.medias.indexOf(media) + 1;
        app.router.navigate('/media/' + media.get('parent_album') + '/?page=' + pos, {
          trigger: false,
          replace: true
        });
        this.router._preloadBreadcrumbs(id).fetch();
        this.router.mediaDetail(media.get('parent_album'));
      } else {
        var media = new Medias.Models.Media({
          id: id
        });
        media.fetch().then(_.bind(function() {

          app.router.navigate('/media/' + media.get('parent_album') + '/', {
            trigger: false,
            replace: false
          });

          this.router._preloadMediaDetail(media.get('parent_album'), true, id);
          this.mediaDetail(media.get('parent_album'));
        }, this))
      }
    },

    /*
     * Preload album that contain the media displayed
     * redirect to album page if needed
     */
    _preloadMediaDetail: function(albumId, notregular, mediaId) {
      var params = this.router ? this.router.params : this.params
      var id = albumId || params.albumId;

      if(app.medias && app.medias.at(0).get('parent_album') == id) {
        var paginator = new Paginator.Paginator({
          current: this.router._getQueryVariable('page', 1),
          limit: 1
        }, app.medias);
        app.paginator = paginator;

        this.router._preloadBreadcrumbs(app.paginator.page.at(0).get('id')).fetch();

      } else {
        var deferred = null;
        if(notregular !== true) {
          var deferred = this.defer();
        }


        app.medias = new Medias.Models.Medias();

        app.medias.fetch({
          data: {
            parent_album_id: id
          }
        }).then(_.bind(function() {
          var paginator = new Paginator.Paginator({
            current: this.router._getQueryVariable('page', 1),
            limit: 1
          }, app.medias);

          app.paginator = paginator;
          this.router._preloadBreadcrumbs(app.paginator.page.at(0).get('id')).fetch();

          if(deferred !== null) {
            deferred.resolve();
          } else {
            var pos = app.medias.indexOf(app.medias.where({
              id: mediaId
            })) + 1;
            app.router.navigate('/media/' + albumId + '/?page=' + pos, {
              trigger: false,
              replace: true
            });
          }
        }, this));
      }
    },

    /*
     * Regular msingle media display
     */
    mediaDetail: function(albumId) {

      app.currentAlbumId = albumId;
      Uploads.enable();
      var params = this.router ? this.router.params : this.params
      var layoutoptions = {
        template: 'layouts/media',
        views: {

          // breadcrumb
          "#main-header": new Medias.Views.Header({
            breadcrumbs: app.breadcrumbs,
            views: {
              '.paginator': new Paginator.View({
                model: app.paginator
              })
            }
          }),
          // list container
          "#main-content": new Medias.Views.Detail({
            model: app.paginator.page.at(0)
          })
        }
      };

      this.router._renderLayout(layoutoptions, {
        type: 'media',
        value: albumId,
        page: parseInt(this.router._getQueryVariable('page', 1))
      });

    },


    /*
     * #########################################################################################
     * Albums or album content
     * #########################################################################################
     */


    _cleanHtmlTimer: null,
    preloadMedias: function() {

      // if first load or facetting change
      if(this.router._isFirstMediaDisplay() || this.router._hasFacetsChanged()) {


        var id = this.router.params.id;


        // if first load
        if(typeof(app.medias) === 'undefined' || app.medias.length == 0 || app.medias.at(0).get('parent_album') != id) {


          var medias = new Medias.Models.Medias();
          app.medias = medias;

          if(id === null || typeof(id) == 'undefined') {

            fetchData = {
              data: {
                is_an_album: 1
              }
            };
          } else {

            fetchData = {
              data: {
                parent_album_id: id
              }
            };
          }
          var deferred = this.defer();
          medias.fetch(fetchData).then(function() {
            deferred.resolve();
          });
        }

        var mediasQuery = app.medias.createLiveChildCollection();
        app.mediasQuery = mediasQuery;

        mediasQuery = mediasQuery.setPill('year', {
          prefixes: ['year:'],
          callback: function(model, value) {
            return model.get('year') == value;
          }
        });

        mediasQuery = mediasQuery.setPill('month', {
          prefixes: ['month:'],
          callback: function(model, value) {
            return model.get('month') == value;
          }
        });

        mediasQuery = mediasQuery.setPill('day', {
          prefixes: ['day:'],
          callback: function(model, value) {
            return model.get('day') == value;
          }
        });

        // apply facetting
        mediasQuery.setSearchString(this.router._getQueryVariable('facets')).query();

        var paginator = new Paginator.Paginator({
          current: this.router._getQueryVariable('page', 1)
        }, mediasQuery);
        app.paginator = paginator;

      } else {

        var cleanHtml = _.bind(function() {
          this._cleanHtmlTimer = null;
          $('[data-delete]').remove();
          var $el = app.layout.$el.find('.thumbnails');
          $el.css('position', 'relative');
          $el.attr('class', "thumbnails");
        }, this);


        if(this._cleanHtmlTimer !== null) {
          clearTimeout(this._cleanHtmlTimer);
        }
        cleanHtml();

        // remove transition classes on current layout
        var $el = app.layout.$el.find('.thumbnails');

        var $clone = $el.clone();
        var $parent = app.layout.$el.find('.thumbnails').parent();
        $clone.css('position', 'absolute');
        $clone.attr('data-delete', "true");

        $parent.prepend($clone);
        var page = this.router._getQueryVariable('page', 1);

        var cssClass = null;
        if(page < app.paginator.get('current')) {
          cssClass = 'horizontal-left';
        } else {
          cssClass = 'horizontal-right';
        }
        $el.addClass("offset-" + cssClass);
        $clone.addClass("out-" + cssClass);

        app.paginator.set('current', page);
        app.paginator._compute();


        $el.addClass("in-" + cssClass);

        this._cleanHtmlTimer = setTimeout(cleanHtml, 800);


      }
    },

    _getFacetUrl : function (facets, facetAdd, facetRemove) {
      var qs = decodeURIComponent(document.location.search);
      if (qs == '') {
        qs = '?'
      }

      if (facetAdd !== null) {
        if (facets == null) {
          facets = 'facets=' + facetAdd;
          if (qs == '?') {
            qs += facets;
          } else {
            qs += '&' + facets;
          }
        } else {
          qs = qs.replace(facets, facets + ' ' + facetAdd);
        }
      }

      if (typeof(facetRemove) !== 'undefined') {
        var _facets = facets.replace(facetRemove, '');
        var name = facetRemove.split(':')[0];
        if ( name == 'month' || name == "year") {
          _facets = _facets.replace(/day:[0-9]{1,2}/, '');
        }

        if (name == "year") {
         _facets = _facets.replace(/month:[0-9]{1,2}/, '');
        }

        qs = qs.replace(facets, _facets);
        if (_facets.trim().length == 0) {
          qs = qs.replace('facets=', '');
        }
      }


      // clean qs
      qs = qs.replace('&&', '&');
      qs = qs.replace(/&$/, '');
      qs = qs.replace('?&', '?');
      if (qs.trim() == '?') {
        qs ='';
      }

      return document.location.pathname + qs;
    },


    _getDate : function (year, month, day) {
      var d = new Date();
      d.setFullYear(year);

      if (typeof(month) !== 'undefined') {
        d.setMonth(month);
      }

      if (typeof(day) !== 'undefined') {
       d.setDate(day);
      }

      return d;
    },

    _computeFacetting : function () {

      var facetsQs = this._getQueryVariable('facets');

      var facetting = {years : {}, months : {}, days :{}};

      app.mediasQuery.forEach(function(media) {

        // years
        if (typeof(facetting.years[media.get('year')]) !== 'undefined') {
            facetting.years[media.get('year')]++;
        } else {
            facetting.years[media.get('year')] = 1;
        }

        // years
        if (typeof(facetting.months[media.get('month')]) !== 'undefined') {
            facetting.months[media.get('month')]++;
        } else {
            facetting.months[media.get('month')] = 1;
        }

        // years
        if (typeof(facetting.days[media.get('day')]) !== 'undefined') {
            facetting.days[media.get('day')]++;
        } else {
            facetting.days[media.get('day')] = 1;
        }

      }, this);

      var facets = {};

      // dealing with dates
      var d = new Date();

      var years = _.keys(facetting.years);
      if (years.length > 1 ) {
        facets.years = [];
        _.each(years, function (year) {
          facets.years.push({name : year, url : this._getFacetUrl(facetsQs, 'year:' + year), value : facetting.years[year]})
        },this);
      } else {
        d.setFullYear(years[0]);
        // month
        var months = _.keys(facetting.months);
        if (months.length > 1 ) {
          facets.months = [];
          _.each(months, function (month) {
            facets.months.push({name : this._getDate(years[0], month).toString('MMMM yyyy'), url : this._getFacetUrl(facetsQs, 'month:' + month), value : facetting.months[month]})
          },this);
        } else {
          // days
          var days = _.keys(facetting.days);
          if (days.length > 1 ) {
            facets.days = [];
            _.each(days, function (day) {
              facets.days.push({name : this._getDate(years[0], months[0], day).toString('ddd d MMMM yyyy'), url : this._getFacetUrl(facetsQs, 'day:' + day), value : facetting.days[day]})
            },this);
          }
        }
      }

      var currents = [];
      // active facets
      if (facetsQs !== null) {

        _.each(facetsQs.split(/\s+/), function (facet) {
          var split = facet.split(':');
          var name = split[1];
          if (split[0] == 'month') {
            name = this._getDate(years[0], split[1]).toString('MMMM yyyy');
          } else if (split[0] == 'day') {
            name = this._getDate(years[0], months[0], split[1]).toString('ddd d MMMM yyyy')
          }
          currents.push({name : name, url : this._getFacetUrl(facetsQs, null, facet)});
        }, this);
      }


      return {currents : currents, facets : facets, qs : facetsQs};

    },


    albums: function() {
      this.router._album(null);
    },

    album: function(id) {
      this.router._album(id);
    },

    _album : function (id) {

      app.currentAlbumId = id;
      if (id !== null) {
        Uploads.enable();
      }

      if(this._isFirstMediaDisplay() || this._hasFacetsChanged()) {

        var facetting = this._computeFacetting();

        var layoutoptions = {
          template: 'layouts/medias',
          views: {

            // breadcrumb
            "#main-header": new Medias.Views.Header({
              breadcrumbs: app.breadcrumbs,
              views: {
                '.paginator': new Paginator.View({
                  model: app.paginator
                })
              }
            }),

            // list container
            "#main-content": new Medias.Views.Items({
              collection: app.paginator.page
            }),

            // side bar
            "#main-aside-right" : new Medias.Views.SideBar({
              facetting : facetting
            })
          }
        };

        this._renderLayout(layoutoptions, {
          type: 'album',
          value: id,
          facetsQS : facetting.qs
        });
      }

    }

  });

  return Router;

});