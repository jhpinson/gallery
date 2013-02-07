// Set the require.js configuration for your application.
require.config({

  // Initialize the application with the main application file.
  deps: ["main"],

  paths: {
    // JavaScript folders.
    libs: "../assets/js/libs",
    plugins: "../assets/js/plugins",
    vendor: "../assets/vendor",

    // Libraries.
    jquery: "../assets/js/libs/jquery",
    lodash: "../assets/js/libs/lodash",
    backbone: "../assets/js/libs/backbone"
  },

  shim: {
    // Backbone library depends on lodash and jQuery.
    backbone: {
      deps: ["lodash", "jquery"],
      exports: "Backbone"
    },

    // Backbone.LayoutManager depends on Backbone.
    "plugins/backbone.layoutmanager": ["backbone"],
    "plugins/backbone.queryengine": ["backbone"],
    "plugins/backbone.routemanager": ["backbone"],
    "plugins/backbone.forms": ["backbone"],
    "vendor/bootstrap/js/bootstrap": ["jquery"],
    "plugins/date": ["jquery"],
    "plugins/spin": ["jquery"],
    "plugins/jquery.serializeObject" : ["jquery"],
    "plugins/jquery.typeahead" : ["jquery"],
    "plugins/fileupload/jquery.fileupload": ["jquery"],
    "plugins/fileupload/jquery.iframe-transport": ["jquery"],
    "vendor/video-js/video": ["jquery"],
  }

});
