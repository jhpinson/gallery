define([
// Application.
"app"

],

// Map dependencies from above array.

function(app) {
  return {

    mask: null,

    rotate: function(event) {

      event.preventDefault();
      event.stopImmediatePropagation();

      this.model.set({
        running: true
      });

      var value = $(event.currentTarget).attr('data-rotate') || $(event.originalEvent.srcElement).attr('data-rotate');

      this.model.rotate(value, _.bind(function(response) {
        var $img = this.$el.find('img[data-media-pk]');
        $img.fadeOut(200, _.bind(function() {

          //response['url_' + this.thumb_size] += '?' + Math.random();
          $img.attr('src', response['url_' + this.thumb_size]);
          $img.attr('width', response['width_' + this.thumb_size]);
          $img.attr('height', response[+'height_' + this.thumb_size]);
          $img.fadeIn(200);

          this.model.set(response, {
            silent: true
          });
          this.model.set('running', false);

        }, this));

      }, this));
    },

    _applyStatus: function(status, callback) {
      this.model.set({
        'status': status
      }, {
        silent: true
      });
      this.model.save().then(callback);
    },

    mRemove: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set({
        running: true
      });
      //this._applyMask();
      this._applyStatus('deleted', _.bind(function() {
        this.model.set('running', false);
      }, this));
    },

    restore: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set({
        running: true
      });
      this._applyStatus('published', _.bind(function() {
        this.model.set('running', false);
      }, this));
    },

    toggleSelect: function(event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      this.model.set('selected', !this.model.get('selected'));
    }

  };
});