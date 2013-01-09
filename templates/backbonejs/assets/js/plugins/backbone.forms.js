define(['jquery', 'lodash', 'backbone'], function($, _, Backbone) {

  var ModalForm = Backbone.View.extend({

    initialize : function (options) {

      this.title = options.title;

      var $modal = $('#modal').clone();
      $modal.find('.btn-primary').click(_.bind(this.save, this));


      var $body = $modal.find('.modal-body');
      this.setElement($body);
      this.$modal = $modal;

    },

    serialize: function() {
      return {
        object: this.model.toJSON()
      };
    },

    afterRender : function () {

      this.$modal.find('h3').text(this.title);

      this.$modal.modal('show');
    },

    save : function () {
      console.debug(this.$modal.find('form').serialize());
    }

  });

  Backbone.ModalForm = ModalForm;
  return ModalForm;

});