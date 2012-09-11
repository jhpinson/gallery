dajaxiceFormClearErrors = function(formId) {
  
	$('#'+formId+' *[data-loading-text]').button('reset');
	
	// remove class error on div.control-group
	$('#' + formId + ' .control-group').removeClass('error');

	// add hidden class on error containers
	$('#' + formId + ' .error').not('.control-group').remove()
	$('#' + formId + ' .alert-error').hide();

	// empty error containers
	$('#' + formId + ' .alert-error').empty();

}

dajaxiceFormSetErrors = function(data) {

	var formId = data.formId;
	var fieldsErrors = typeof(data.fieldsErrors) !== 'undefined'
			? data.fieldsErrors
			: null;
	var globalErrors = typeof(data.globalErrors) !== 'undefined'
			? data.globalErrors
			: null;

	// fields errors
	if (fieldsErrors != null) {
		for (field in fieldsErrors) {
			$('#' + formId + ' #error_' + field).parents('.control-group')
					.addClass('error');
			var tpl = $('#' + formId + ' #error_' + field + ' .error-tpl');
			fieldsErrors[field].forEach(function (error) {
				$('#' + formId + ' #error_' + field)
						.append((tpl.clone().html(error)
								.removeClass('error-tpl').addClass('error')));
			});
			$('#' + formId + ' #error_' + field).show();
		}
	}

	// global errors
	if (globalErrors !== null) {
		globalErrors.forEach(function(error) {
					$('#' + formId + ' .alert-error').append('<p>' + error
							+ '</p>')
				});

		$('#' + formId + ' .alert-error').show();
	}

}

setupSubmitForm = function(root) {

	var selector = 'form[data-dajax-method]';

	if (typeof(root) !== 'undefined') {
		selector = root + ' ' + selector;
	}
  
	$(selector).submit(function(e) {

				var form = $(this).forceId();
				
				
				if (typeof(form.attr('data-dajax-method')) !== 'undefined') {
					
					$('#'+form.attr('id')+' *[data-loading-text]').button('loading');
					
					e.preventDefault();
					var data = form.serializeObject();
					data.form_id = form.attr('id');
					
					if (typeof(form.attr('data-pk')) !== 'undefined') {
						data.pk = form.attr('data-pk');
					}
					
					var dajaxice = Dajaxice;
					form.attr('data-dajax-method').split('.').forEach(
							function(m) {
								dajaxice = dajaxice[m]
							});
					dajaxice(Dajax.process, data);
          
				}

			});
}
