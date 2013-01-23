define(['jquery', 'lodash', 'backbone'], function($, _, Backbone) {

  var ModalForm = Backbone.View.extend({

    initialize: function(options) {

      this.title = options.title;

      var $modal = $('#modal').clone();
      this.$modal = $modal;
      this.configureModal();

      $modal.find('.btn-primary').click(_.bind(this.save, this));

      var $body = $modal.find('.modal-body');
      this.setElement($body);


    },

    configureModal : function () {
      this.$modal.find('.btn-primary').text(this.options.okLabel || 'ok')
    },

    afterRender: function() {

      this.$modal.find('h3').text(this.title);
      this.$modal.modal('show');
      if (this.options.onShow) {
        this.options.onShow();
      }
    },

    save: function(event) {
        event.preventDefault();
        this.options.onOk(this.$modal.find('form').serializeObject());
        return false;
    }

  });

  Backbone.ModalForm = ModalForm;

  var ModalModelForm = ModalForm.extend({
    initialize : function (options) {
      this.options.okLabel = 'Enregistrer';
      ModalForm.prototype.initialize.apply(this, arguments);
    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    save: function() {
      this.options.model.set(this.$modal.find('form').serializeObject());
      this.options.model.save().then(_.bind(function() {
        this.$modal.modal('hide');
        this.options.onOk(this.options.model)
      }, this))
    }
  });
  Backbone.ModalModelForm = ModalModelForm;
  return ModalForm;

});