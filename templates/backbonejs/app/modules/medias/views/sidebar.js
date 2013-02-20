define([
// Application.
"app", "modules/medias/models", "modules/medias/views/selection",

],

// Map dependencies from above array.

function(app, Models, Selection) {
  return  Backbone.View.extend({
    template: 'medias/sidebar',

    events: {
      "click .album-add": "addAlbum",
      "click .move": "move"
    },

    _facetting: null,
    _selectionView: null,
    initialize: function(options) {
      //this._facetting = options.facetting;
      this._collection = options.collection;
      this._collection.bind('all', this.onCollectionChange, this);
      this._facetting = this._computeFacetting();

      // reset
      this.paginator = app.paginator;
      this.paginator.bind('change:current', this.resetSelectionView, this);
    },

    move: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();

      var form = new Backbone.ModalForm({
        template: 'medias/forms/album-select',
        title: 'Déplacer les éléments sélectionnés',
        onShow: _.bind(function() {

          form.$modal.find('#search').typeahead({
            matcher: function(item) {
              return true
            },
            sorter: function(items) {
              return items;
            },
            updater: function(item) {
              form.$modal.find('#album-id').val(item.id);
              return item.name;
            },
            source: function(query, process) {
              $.ajax({
                url: '/rest/medias/search?q=' + query,
                type: 'GET',
                dataType: 'application/json',
                contentType: 'application/json',
                context: this,
                'complete': function(xhr) {

                  process(JSON.parse(xhr.responseText));


                }
              });
            }
          })

          form.$modal.find('#myTab a').click(function(e) {
            e.preventDefault();
            $(this).tab('show');
            return false;
          })
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

            app.mediasQuery.each(function(obj, id, col) {
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

    addAlbum: function(event) {
      event.preventDefault();

      var album = new Models.Media();

      var form = new Backbone.ModalModelForm({
        template: 'medias/forms/album',
        title: 'Nouvel album',
        model: album,
        onOk: function(album) {
          app.router.navigate(album.get('absolute_uri'), {
            trigger: true
          });
        },
        validate: function(data) {
          form.$modal.find('.control-group').removeClass('error');
          form.$modal.find('.error').remove();
          if(data.name.trim().length == 0) {
            form.$modal.find('#name').parent().append("<span class='help-inline error'>Ce champ est requis</span>");
            form.$modal.find('#name').parents('.control-group').addClass('error');
            return false
          }
          return true;
        }
      })

      form.render();

    },

    onCollectionChange: function() {
      var facetting = this._computeFacetting();
      if(JSON.stringify(this._facetting) != JSON.stringify(facetting)) {
        this._facetting = facetting;
        this.render();
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

    _getFacetUrl: function(facets, facetAdd, facetRemove) {
      var qs = decodeURIComponent(document.location.search);
      if(qs == '') {
        qs = '?'
      }

      if(facetAdd !== null) {
        if(facets == null) {
          facets = 'facets=' + facetAdd;
          if(qs == '?') {
            qs += facets;
          } else {
            qs += '&' + facets;
          }
        } else {
          qs = qs.replace(facets, facets + ' ' + facetAdd);
        }
      }

      if(typeof(facetRemove) !== 'undefined') {
        var _facets = facets.replace(facetRemove, '');
        var name = facetRemove.split(':')[0];
        if(name == 'month' || name == "year") {
          _facets = _facets.replace(/day:[0-9]{1,2}/, '');
        }

        if(name == "year") {
          _facets = _facets.replace(/month:[0-9]{1,2}/, '');
        }

        qs = qs.replace(facets, _facets);
        if(_facets.trim().length == 0) {
          qs = qs.replace('facets=', '');
        }
      }


      // clean qs
      qs = qs.replace('&&', '&');
      qs = qs.replace(/&$/, '');
      qs = qs.replace('?&', '?');
      if(qs.trim() == '?') {
        qs = '';
      }
      qs = qs.replace(/page=[0-9]+/, 'page=1');

      return document.location.pathname + qs;
    },


    _getDate: function(year, month, day) {
      var d = new Date();


      if(typeof(year) !== 'undefined') {
        d.setFullYear(year);
      } else {
        return null;
      }

      if(typeof(month) !== 'undefined') {
        d.setMonth(month);
      }

      if(typeof(day) !== 'undefined') {
        d.setDate(day);
      }
      return d;
    },

    _computeFacetting: function() {

      var facetsQs = this._getQueryVariable('facets');
      if(facetsQs != null) {
        facetsQs = facetsQs.trim();
      }
      var facetting = {
        years: {},
        months: {},
        days: {},
        deleted: 0
      };

      this._collection.getParentCollection().forEach(function(media) {
        if(media.get('status') == 'deleted') {
          facetting.deleted++;
        }
      }, this);

      this._collection.forEach(function(media) {

        // years
        if(typeof(facetting.years[media.get('year')]) !== 'undefined') {
          facetting.years[media.get('year')]++;
        } else {
          facetting.years[media.get('year')] = 1;
        }

        // month
        if(typeof(facetting.months[media.get('month')]) !== 'undefined') {
          facetting.months[media.get('month')]++;
        } else {
          facetting.months[media.get('month')] = 1;
        }

        // day
        if(typeof(facetting.days[media.get('day')]) !== 'undefined') {
          facetting.days[media.get('day')]++;
        } else {
          facetting.days[media.get('day')] = 1;
        }
      }, this);

      var facets = {};

      // dealing with dates
      var d = new Date();

      facets.deleted = {
        name: 'supprimé',
        url: this._getFacetUrl(facetsQs, 'status:all'),
        value: facetting.deleted
      }

      var years = _.keys(facetting.years);
      if(years.length > 1) {
        facets.years = [];
        _.each(years, function(year) {
          facets.years.push({
            name: year,
            url: this._getFacetUrl(facetsQs, 'year:' + year),
            value: facetting.years[year]
          })
        }, this);
      } else {
        d.setFullYear(years[0]);
        // month
        var months = _.keys(facetting.months);
        if(months.length > 1) {
          facets.months = [];
          _.each(months, function(month) {
            facets.months.push({
              name: this._getDate(years[0], month).toString('MMMM yyyy'),
              url: this._getFacetUrl(facetsQs, 'month:' + month),
              value: facetting.months[month]
            })
          }, this);
        } else {
          // days
          var days = _.keys(facetting.days);
          if(days.length > 1) {
            facets.days = [];
            _.each(days, function(day) {
              facets.days.push({
                name: this._getDate(years[0], months[0], day).toString('ddd d MMMM'),
                url: this._getFacetUrl(facetsQs, 'day:' + day),
                value: facetting.days[day]
              })
            }, this);
          }
        }
      }

      var currents = [];
      // active facets
      if(facetsQs !== null) {

        _.each(facetsQs.split(/\s+/), function(facet) {
          var split = facet.split(':');
          var name = split[1];
          if(split[0] == 'status' && name == 'all') {
            name = 'éléments supprimés';
            delete facets.deleted;
          }
          if(split[0] == 'month') {
            var d = this._getDate(years[0], split[1]);
            if(d == null) {
              return;
            }
            name = d.toString('MMMM yyyy');
          } else if(split[0] == 'day') {
            var d = this._getDate(years[0], months[0], split[1]);
            if(d == null) {
              return;
            }
            name = d.toString('ddd d MMMM')
          }
          currents.push({
            name: name,
            url: this._getFacetUrl(facetsQs, null, facet)
          });
        }, this);
      }
      return {
        currents: currents,
        facets: facets,
        qs: facetsQs
      };

    },

    render: function(template, context) {
      var context = context || {};
      context = _.extend({}, context, {
        facetting: this._facetting,
        is_an_album: app.currentAlbumId !== null
      });
      return template(context);
    },

    afterRender: function() {
      this.resetSelectionView();

      this.$el.find('.fileinputs').each(function(id, el) {
        var $el = $(el);
        var $input = $el.find('input[type=file]');
        var $target = $el.find('.fakefile');
        $input.mouseover(function(e) {
          $target.addClass('hover');
        });

        $input.mouseout(function(e) {
          $target.removeClass('hover')
        });
      });

      if(app.Uploads.isEnabled) {
        $('body').fileupload('option', 'fileInput', this.$el.find('.fileinputs'));
      }

    },

    resetSelectionView: function() {
      // if there is no album display currently
      if(app.page.value === null) {
        return;
      }

      if(this._selectionView !== null) {
        this._selectionView.remove();
        this._selectionView = null;

        app.paginator.page.each(function(o, id, col) {
          o.set({
            'selected': false
          });
        });
      }

      var selectionView = new Selection({
        collection: this.paginator.page.createLiveChildCollection().setPill('selected', {
          prefixes: ['selected:'],
          callback: function(model, value) {
            return model.get('selected') == true;
          }
        }).setSearchString('selected:true').query()
      });
      this._selectionView = selectionView;
      this.$el.append(selectionView.$el);
      selectionView.render();
    }
  });
});