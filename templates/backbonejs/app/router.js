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
      return app.page === null || app.page.type !== 'album' || app.page.value !== ( typeof(params.id) === 'undefined' ? null : params.id)
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


      // remove transition classes on current layout
      $('.main-container>div').attr('class', "");

      layoutOptions.afterRender = _.bind(function(layout) {

        if(currentLayout !== null) {


          // setup transition effects
          if(app.supportEffects) {

            var cssClass = null;
            var source = app.page;

            currentLayout.$el.fadeOut(100, function () {
              currentLayout.$el.remove();
              layout.$el.fadeIn(100);
            });


          }
          // browser doesn't support effects
          else {
            currentLayout.remove();
            layout.$el.show();
          }

        }

        /*if(source) {
          $('body').removeClass(source.type);
        }
        $('body').addClass(dest.type);
        */

        // store new page description
        app.page = dest;
      }, this);

      // create layout and render it
      var layout = app.useLayout(layoutOptions)
      if(currentLayout !== null) {
        layout.$el.hide();
      }
      $('.main-container').append(layout.$el);
      return layout.render();

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

      /*var breadcrumbs = new Backbone.Collection({
        model: Medias.Models.Media
      });*/
      var breadcrumbs = new Medias.Models.Medias();
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
            className : 'inline-block',
            model: app.paginator.page.at(0),
            paginator : app.paginator
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

        var id = this.router.params.id;
        app.breadcrumbsUrl[id || 0] = document.location.pathname + document.location.search;

      // if first load or facetting change
      if(this.router._isFirstMediaDisplay() || this.router._hasFacetsChanged()) {




        // if first load
        if(typeof(app.medias) === 'undefined' || app.medias.length == 0 || app.medias.at(0).get('parent_album') != id) {


          var medias = new Medias.Models.Medias();
          app.medias = medias;
          app.medias.setComparator(function(a,b) {
            return Date.parse(a.get('date')) - Date.parse(b.get('date'))
          });
          app.medias.sortCollection();
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

        mediasQuery = mediasQuery.setPill('status', {
          prefixes: ['status:'],
          callback: function(model, value) {
            if (value !== 'all') {
              return model.get('status') == value;
            } else {
              return true;
            }
          }
        });

        // status:published by default
        var facets = this.router._getQueryVariable('facets');
        if (facets == null) {
          facets = 'status:published';
        } else {
          if (facets.indexOf('status:') === -1) {
            facets += ' status:published';
          }
        }
        // apply facetting
        mediasQuery.setSearchString(facets).query();

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


        $el.addClass("offset-fade");
        $el.show();

        $clone.addClass("fade-out");
        $el.addClass("fade-in");

        app.paginator.set('current', page);
        app.paginator._compute();

        this._cleanHtmlTimer = setTimeout(cleanHtml, 800);


      }
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

        //var facetting = this._computeFacetting();

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
              collection: app.paginator.page,
              paginator : app.paginator
            }),

            // side bar
            "#main-aside-right" : new Medias.Views.SideBar({
              //facetting : facetting,
              collection : app.mediasQuery
            })
          }
        };

        this._renderLayout(layoutoptions, {
          type: 'album',
          value: id,
          //facetsQS : facetting.qs
           facetsQS : this._getQueryVariable('facets')
        });
      }

    }

  });

  return Router;

});