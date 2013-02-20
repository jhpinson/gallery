define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {

  return Backbone.View.extend({
    template: 'medias/header',

    _breadcrumbs: null,

    initialize: function(options) {

      this._breadcrumbs = options.breadcrumbs;
      this._breadcrumbs.bind('reset', this.render, this);
    },

    render: function(template, context) {
      var context = context || {};

      var breadcrumbs = [];
      if (typeof(app.breadcrumbsUrl[0]) == 'undefined') {
        breadcrumbs.push({name : 'Accueil', url : '/'})
      } else {
        breadcrumbs.push({name : 'Accueil', url : app.breadcrumbsUrl[0]})
      }

      this._breadcrumbs.forEach(function (obj) {
        if (typeof(app.breadcrumbsUrl[obj.get('id')]) == 'undefined') {
            breadcrumbs.push({name : obj.get('name'), url : obj.get_uri()})
          } else {
            breadcrumbs.push({name : obj.get('name'), url : app.breadcrumbsUrl[obj.get('id')]})
          }
      })

      context = _.extend({}, context, {
        breadcrumbs: breadcrumbs
      });
      return template(context);
    }

  });
});