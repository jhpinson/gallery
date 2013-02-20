define([
// Application.
"app", "modules/medias/views/header", "modules/medias/views/selection", "modules/medias/views/sidebar", "modules/medias/views/dropbox", "modules/medias/views/items", "modules/medias/views/detail", "modules/medias/views/item"

],

// Map dependencies from above array.

function(app, Header, Selection, SideBar, DropBox, Items, Detail, Item) {

  var Views = {};

  Views.Header = Header;
  Views.Selection = Selection;
  Views.SideBar = SideBar;
  Views.Dropbox = DropBox;
  Views.Items = Items;
  Views.Detail = Detail;
  Views.Item = Item;

  return Views;

});