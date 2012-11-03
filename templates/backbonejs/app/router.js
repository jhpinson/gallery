define([
// Application.
"app", "modules/medias", "modules/views", "modules/paginator"],

function(app, Medias, Views, Paginator) {
  document.app = app;
  // Defining the application router, you can attach sub routers here.
  var Router = Backbone.RouteManager.extend({


    before: {

      "": ["preloadMedias", "preloadBreadcrumbs"],
      "album/:id/*qs": ["preloadMedias", "preloadBreadcrumbs"],
      "media/:albumId/*qs": ['_preloadMediaDetail']

    },

    routes: {
      "": "albums",
      "album/:id/*qs": 'album',
      "media-redirect/:id/": 'mediaRedirect',
      "media/:albumId/*qs": 'mediaDetail',
    },



    _isFirstMediaDisplay: function() {
      var params = this.router ? this.router.params : this.params
      return app.page === null || app.page.type !== 'album' || app.page.value !== params.id
    },


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
    _preloadMediaDetail: function(albumId, notregular, mediaId) {
      var params = this.router ? this.router.params : this.params
      var id = albumId || params.albumId;

      console.debug('_preloadMediaDetail', arguments)
      if(app.medias && app.medias.at(0).get('parent_album') == id) {
        console.debug('_preloadMediaDetail', 'app.medias ok')
        var paginator = new Paginator.Paginator({
          current: this.router._getQueryVariable('page', 1),
          limit: 1
        }, app.medias);
        app.paginator = paginator;

        this.router._preloadBreadcrumbs(app.paginator.page.at(0).get('id')).fetch();

      } else {
        console.debug('_preloadMediaDetail', 'chargement de app.medias')
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
    mediaDetail: function(albumId) {
      // l'id est celui de l'abum
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

      //var layoutoptions = this.router._createAlbumLayout();
      this.router._renderLayout(layoutoptions, {
        type: 'media',
        value: albumId,
        page: parseInt(this.router._getQueryVariable('page', 1))
      });

    },

    _cleanHtmlTimer: null,
    preloadMedias: function() {
      if(this.router._isFirstMediaDisplay()) {
        var id = this.router.params.id;

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
            //mediasQuery.query({limit:25, page:1});
            deferred.resolve();
          });
        }

        var mediasQuery = app.medias.createLiveChildCollection();
        mediasQuery.query();
        var paginator = new Paginator.Paginator({
          current: this.router._getQueryVariable('page', 1)
        }, mediasQuery);


        app.mediasQuery = mediasQuery;
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
        //$el.css('position', 'absolute');
        //$el.attr('class', "thumbnails");
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

            if(dest.type == 'album' && dest.value == null) {
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

    _createAlbumLayout: function() {



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
          })
        }
      };

      return layoutoptions;

    },

    albums: function() {
      if(this.router._isFirstMediaDisplay()) {
        var layoutoptions = this.router._createAlbumLayout();
        this.router._renderLayout(layoutoptions, {
          type: 'album',
          value: null
        });
      }
    },

    album: function(id) {
      if(this.router._isFirstMediaDisplay()) {
        var layoutoptions = this.router._createAlbumLayout();
        this.router._renderLayout(layoutoptions, {
          type: 'album',
          value: id
        });
      }
    }
  });

  return Router;

});