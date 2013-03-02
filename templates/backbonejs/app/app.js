define([
  // Libraries.
  "jquery",
  "lodash",
  "backbone",



  // Plugins.
  "plugins/backbone.queryengine",
  "plugins/backbone.layoutmanager",
  "plugins/backbone.routemanager",
  "plugins/backbone.forms",

  "plugins/date",
  "plugins/fileupload/jquery.fileupload",
  "plugins/fileupload/jquery.iframe-transport",
  "plugins/jquery.serializeObject",
  "vendor/bootstrap/js/bootstrap",
  //"vendor/typeahead/typeahead",
  "vendor/video-js/video"

],

function($, _, Backbone) {

  // Provide a global location to place configuration settings and module
  // creation.
  var app = {
    // The root path to run the application.
    root: "/",
    page : null,
    layout : null,
    breadcrumbs : new Backbone.Collection(),
    collections : {medias : null, mediasQuery : null},
    supportEffects : true,
    loggedUser : null,
    currentAlbumId : null,
    breadcrumbsUrl : {}
  };

  var onresize = function () {
    $('#main-container').css('min-height', $(window).height() - $('#nav-header').height() - 20 - 20 - $('#footer').height() + 'px');
  }
  $(window).bind('resize', onresize);
  onresize();

  // Localize or create a new JavaScript Template object.
  var JST = window.JST = window.JST || {};

  // Configure LayoutManager with Backbone Boilerplate defaults.
  Backbone.LayoutManager.configure({
    // Allow LayoutManager to augment Backbone.View.prototype.
    manage: true,

    prefix: "app/templates/",

    fetch: function(path) {

      // Concatenate the file extension.
      path = path + ".html";

      // If cached, use the compiled template.
      if (JST[path]) {
        return JST[path];
      }

      // Put fetch into `async-mode`.
      var done = this.async();

      // Seek out the template asynchronously.
      $.get(app.root + path, function(contents) {
        done(JST[path] = _.template(contents));
      });
    }
  });

  // Mix Backbone.Events, modules, and layout management into the app object.
  return _.extend(app, {
    // Create a custom object with a nested Views object.
    module: function(additionalProps) {
      return _.extend({ Views: {} }, additionalProps);
    },

    // Helper for using layouts.
    useLayout: function(options) {
      // Create a new Layout with options.
      var layout = new Backbone.Layout(options);

      // Cache the refererence.
      return this.layout = layout;
    }
  }, Backbone.Events);

});
