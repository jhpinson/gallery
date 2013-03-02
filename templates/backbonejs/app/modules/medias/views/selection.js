define([
// Application.
"app", "modules/medias/models","plugins/async"

],

// Map dependencies from above array.

function(app, Models, async) {




  return Backbone.View.extend({
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
              //response['url_' + this.thumb_size] += '?' + Math.random();
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


      }, this);

      async.series(methods, function(err, results) {
        //alert('done')
      });

    },

    move: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      var form = new Backbone.ModalForm({
        template: 'medias/forms/album-select',
        title: 'Déplacer les éléments sélectionnés',
        onShow: _.bind(function() {

          var searchTimeout = null;

          var retrieveResults = function(query, process) {

            if (searchTimeout !== null) {
              clearTimeout(searchTimeout);
            }

            var transformResults = function(results) {
              console.debug(results)
              return $.map(results, function(result) {

                    return {
                      id : result.id,
                      title : result.name,
                      html : _.template('<p><%= name %></p>')(result),
                      toString : function() {
                        return JSON.stringify(this);
                      },
                      toLowerCase : function() {
                        return this.html.toLowerCase();
                      },
                      indexOf : function(string) {
                        return String.prototype.indexOf.apply(
                            this.html, arguments);
                      },
                      replace : function(string) {
                        return String.prototype.replace.apply(
                            this.html, arguments);
                      }
                    };
                  });
            }

            searchTimeout = setTimeout(function(query) {
              if (searchTimeout !== null) {
                clearTimeout(searchTimeout);
              }

              $.ajax({
                url: '/rest/medias/search?q=' + query,
                type: 'GET',
                contentType: 'application/json',
                context: this,

                success : function(data) {
                  return typeof data == 'undefined'
                      ? false
                      : process(transformResults(data))
                },
                error : function() {
                }
              });

            }, 500, query);

          };

          form.$modal.find('#search').typeahead({
                source : retrieveResults,
                updater : function(json) {
                  var item = $.parseJSON(json);
                  form.$modal.find('#album-id').val(item.id);
                  return item.title;

                },
                items : 10,
                minLength : 1
              })





          form.$modal.find('#myTab a').click(function(e) {
            e.preventDefault();
            $(this).tab('show');
            return false;
          });
          orm.$modal.find('#myTab a:first').tab('show');
        }, this),
        onOk: _.bind(function(data) {

          var op, album, follow = typeof(data.goto) !== 'undefined';

          form.$modal.find('.control-group').removeClass('error');
          form.$modal.find('span.error').remove();

          if(form.$modal.find('.active [href=#existent]').length == 1) {

            if(data['album-id'] == '') {
              form.$modal.find('#album-id').parent().append('<span class="help-inline error">Veuillez remplir ce champ</span>');
              form.$modal.find('#album-id').parents('.control-group').addClass('error');
              return false;
            }

            album = new Models.Media({
              id: data['album-id']
            });
            op = album.fetch;
          } else {

            if(data['album-name'] == '') {
              form.$modal.find('#album-name').parent().append('<span class="help-inline error">Veuillez remplir ce champ</span>');
              form.$modal.find('#album-name').parents('.control-group').addClass('error');
              return false;
            }

            album = new Models.Media();
            album.set({
              name: data['album-name']
            });
            op = album.save;
          }

          op.call(album).then(_.bind(function() {

            var items = [];

            this.collection.each(function(obj, id, col) {
              //obj.set('running', true);
              items.push(obj.get('id'))
            });

            $.ajax({
              url: '/rest/medias/move',
              type: 'PUT',
              dataType: 'application/json',
              contentType: 'application/json',
              data: JSON.stringify({
                'items': items,
                'album': album.get('id')
              }),
              context: this,
              'complete': function(xhr) {
                form.$modal.modal('hide');
                if(follow) {
                  app.router.navigate(album.get('absolute_uri'), {
                    trigger: true
                  });
                } else {
                  app.medias.fetch({
                    url: app.medias.url + '?parent_album_id=' + app.currentAlbumId
                  });
                }
              }
            });


          }, this))

        }, this)
      })

      form.render();
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

  });
});