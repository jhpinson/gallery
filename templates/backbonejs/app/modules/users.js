define([
// Application.
"app",

"modules/users/models", "modules/users/views" ],

function(app, Models, Views) {

  // Create a new module.
  var Users = app.module();

  Users.Models = Models;
  Users.Views = Views;

  return Users;

});