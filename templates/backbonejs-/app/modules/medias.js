define(["app"],

function(app) {

			var medias = {};
      app.medias = medias;
      medias.currentAlbum = null;
      
			/*
			 * Media model
			 */
			var Media = Backbone.Model.extend({

						urlRoot : '/rest/medias',

						// Ensure that each todo created has `title`.
						initialize : function() {
						},
						// Remove this Todo from *localStorage* and delete its
						// view.
						clear : function() {
							this.destroy();
						}
					});

			/*
			 * Media collection
			 */
			MediaList = Backbone.Collection.extend({
						url : '/rest/medias',
						// Reference to this collection's model.
						model : Media
					});

		  // initialize the media collection
      medias.collection = new MediaList();

			/*
			 * Media view
			 */
			var MediaView = Backbone.View.extend({

						// ... is a list tag.
						tagName : "li",
            className : "span2",
            
						// Cache the template function for a single item.
						template : 'media.thumb',

						// The TodoView listens for changes to its model,
						// re-rendering. Since there's
						// a one-to-one correspondence between a **Todo** and a
						// **TodoView** in this
						// app, we set a direct reference on the model for
						// convenience.
						initialize : function() {
							this.model.bind('change', this.render, this);
							this.model.bind('destroy', this.remove, this);
						},

						serialize : function() {
							return this.model.toJSON();
						},

						// Re-render the titles of the todo item.
						/*
						 * render : function() {
						 * this.$el.html(this.template(this.model.toJSON()));
						 * 
						 * return this; },
						 */

						// Remove the item, destroy the model.
						clear : function() {
							this.model.clear();
						}
					});

			/*
			 * Media List view
			 */
			var MediaListView = Backbone.View.extend({

						initialize : function() {
							//medias.collection.bind('add', this.addOne, this);
							//medias.collection.bind('reset', this.addAll, this);
							medias.collection.bind('all', this.render, this);
						},
						/*
						 * addOne : function(todo) { var view = new MediaView({
						 * model : todo });
						 * this.$('.thumbnails').append(view.render().el); },
						 * 
						 * addAll : function() {
						 * medias.collection.each(this.addOne); }
						 */

						tagName : "ul",
						className : "thumbnails",
            
						// Insert all subViews prior to rendering the View.
						beforeRender : function() {
							// Iterate over the passed collection and create a
							// view for each item.
							medias.collection.each(function(model) {
										// Pass the sample data to the new
										// SomeItem View.
										this.insertView(new MediaView({
													model : model
												}));
									}, this);
						}
					});

			medias.layout = new Backbone.Layout({
						template : "main",

						views : {
							"#main-content" : new MediaListView()
						}
					});
      
		  
			return medias

		});
