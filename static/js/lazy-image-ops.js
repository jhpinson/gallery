var hasOp = {};

selectMedia = function selectMedia($thumb) {
	$thumb.addClass('selected');
	$thumb.find('input[type=checkbox]').attr('checked', true);
}

unSelectMedia = function unSelectMedia($thumb) {
	$thumb.removeClass('selected');
	$thumb.find('input[type=checkbox]').attr('checked', false);
}

disableMassAction = function() {
	$('.mass-media-action').addClass('disabled');
}

setupMassAction = function() {

	var deleted = $('.thumbnail.deleted input[type=checkbox]:checked').length > 0;
	var published = $('.thumbnail.published input[type=checkbox]:checked').length > 0;

	$('.mass-media-action').hide();
	$('.mass-media-action').removeClass('disabled');

	if (deleted && published) {
		$('.mass-media-action.allow-for-all').show();
	} else if (deleted) {
		$('.mass-media-action.allow-for-deleted').show();
		$('.mass-media-action.allow-for-all').show();
	} else if (published) {
		$('.mass-media-action.allow-for-published').show();
		$('.mass-media-action.allow-for-all').show();
	} else {
		$('.mass-media-action.allow-empty').show();
	}

}

callback_media_remove = function callback_media_remove(data) {

	var $img = $('#' + data.html_id);
	var $mask = $("#mask-" + data.html_id)

	$('.thumb-container[data-media-pk=' + data.media_pk + ']').removeClass('published');
	$('.thumb-container[data-media-pk=' + data.media_pk + ']').addClass('deleted');

	$mask.fadeOut(200);
	$img.fadeOut(200, function() {
				$mask.remove();
				hasOp[data.html_id].stop();
				delete hasOp[data.html_id];

				$img.fadeIn(200);
				$('[data-ops-target=' + data.html_id + ']').each(
						function(idx, el) {
							$(el).parents('li:first').removeClass('disabled');
						})

			});

}

callback_media_unremove = function callback_media_unremove(data) {

	var $img = $('#' + data.html_id);
	var $mask = $("#mask-" + data.html_id)

	$('.thumb-container[data-media-pk=' + data.media_pk + ']').removeClass('deleted');
	$('.thumb-container[data-media-pk=' + data.media_pk + ']').addClass('published');

	$mask.fadeOut(200);
	$img.fadeOut(200, function() {
				$mask.remove();
				hasOp[data.html_id].stop();
				delete hasOp[data.html_id];

				$img.fadeIn(200);

				$('[data-ops-target=' + data.html_id + ']').each(
						function(idx, el) {
							$(el).parents('li:first').removeClass('disabled');
						})

			});

}

callback_media_rotate = function callback_medias_rotate(data) {

	var $img = $('#' + data.html_id);
	var $mask = $("#mask-" + data.html_id)

	$mask.fadeOut(200);
	$img.fadeOut(200, function() {
				$mask.remove();
				hasOp[data.html_id].stop();
				delete hasOp[data.html_id];
				$img.attr('width', data.width);
				$img.attr('height', data.height);
				$img.attr('src', data.url + '?' + Math.random());
				$img.fadeIn(200);

				$('[data-ops-target=' + data.html_id + ']').each(
						function(idx, el) {
							$(el).parents('li:first').removeClass('disabled');
						})

			});

}

createSpin = function createSpin(small, targetId) {

	var opts = {
		lines : 17, // The number of lines to draw
		length : 11, // The length of each line
		width : 4, // The line thickness
		radius : 13, // The radius of the inner circle
		corners : 1, // Corner roundness (0..1)
		rotate : 0, // The rotation offset
		color : '#DDD', // #rgb or #rrggbb
		speed : 1, // Rounds per second
		trail : 100, // Afterglow percentage
		shadow : false, // Whether to render a shadow
		hwaccel : false, // Whether to use hardware acceleration
		className : 'spinner', // The CSS class to assign to the spinner
		zIndex : 2e9, // The z-index (defaults to 2000000000),
		top : 'auto',
		left : 'auto'
	};

	var target = document.getElementById(targetId);
	return new Spinner(opts).spin(target);

}

_prepare_for_running_operation = function($target) {
	if (typeof(hasOp[$target.attr('id')]) !== 'undefined') {
		return false;
	}

	hasOp[$target.attr('id')] = null;

	var $thumb = $('#' + $target.attr('id')).parents('.thumb-container');

	var offset = $thumb.offset();

	var width = $thumb.width() + parseInt($thumb.css('padding')) * 2
			+ parseInt($thumb.css('border-width')) * 2;
	var height = $thumb.height() + parseInt($thumb.css('padding')) * 2
			+ parseInt($thumb.css('border-width')) * 2;
	var $mask = $('<div id="mask-' + $target.attr('id')
			+ '" class="image-mask" style="display:none"></div>')
	$('body').append($mask);
	$mask.css({
				top : offset.top + 'px',
				left : offset.left + 'px',
				height : height + 'px',
				width : width + 'px'
			})

	$mask.fadeIn(50, function() {
				hasOp[$target.attr('id')] = createSpin(true, $mask.attr('id'));
			});
	$thumb.find('.actions').fadeOut(50);

	$('[data-ops-target=' + $target.attr('id') + ']').each(function(idx, el) {
				$(el).parents('li:first').addClass('disabled');
			});

	return true;
}

media_rotate = function media_rotate($el) {

	var data = {
		html_id : $el.attr('data-ops-target'),
		size : $el.attr('data-image-size') || null,
		value : $el.attr('data-image-rotate') || null,
		pk : $el.attr('data-media-pk')
	}

	if (_prepare_for_running_operation($('#' + $el.attr('data-ops-target'))) !== false) {
		Dajaxice.medias.rotate(Dajax.process, data);
	}
}

mass_media_rotate = function media_rotate($el, $list) {

	var data = [];

	$list.each(function(idx, target) {
		var $target = $(target).parents('.thumbnail')
				.find('img[data-media-pk]');

		if (_prepare_for_running_operation($('#' + $target.attr('id'))) !== false) {
			data.push({
						html_id : $target.attr('id'),
						size : $el.attr('data-image-size') || null,
						value : $el.attr('data-image-rotate') || null,
						pk : $target.attr('data-media-pk')
					});
		}
	});

	Dajaxice.medias.mass_rotate(Dajax.process, {
				datas : data
			});

}

media_remove = function media_remove($el) {

	var data = {
		html_id : $el.attr('data-ops-target'),
		size : $el.attr('data-image-size') || null,
		value : $el.attr('data-image-rotate') || null,
		pk : $el.attr('data-media-pk')
	}

	if (_prepare_for_running_operation($('#' + $el.attr('data-ops-target'))) !== false) {
		Dajaxice.medias.remove(Dajax.process, data);
	}
}

mass_media_remove = function media_rotate($el, $list) {
	var data = [];
	$list.each(function(idx, target) {
		var $target = $(target).parents('.thumbnail')
				.find('img[data-media-pk]');

		if (_prepare_for_running_operation($('#' + $target.attr('id'))) !== false) {
			data.push({
						html_id : $target.attr('id'),
						size : $el.attr('data-image-size') || null,
						value : $el.attr('data-image-rotate') || null,
						pk : $target.attr('data-media-pk')
					})
			// Dajaxice.medias.remove(Dajax.process, data);
		}
	});
	Dajaxice.medias.mass_remove(Dajax.process, {
				datas : data
			});
}

media_unremove = function media_unremove($el) {

	var data = {
		html_id : $el.attr('data-ops-target'),
		size : $el.attr('data-image-size') || null,
		value : $el.attr('data-image-rotate') || null,
		pk : $el.attr('data-media-pk')
	}

	if (_prepare_for_running_operation($('#' + $el.attr('data-ops-target'))) !== false) {
		Dajaxice.medias.unremove(Dajax.process, data);
	}
}

mass_media_unremove = function media_rotate($el, $list) {
	var data = [];
	$list.each(function(idx, target) {
		var $target = $(target).parents('.thumbnail')
				.find('img[data-media-pk]');

		if (_prepare_for_running_operation($('#' + $target.attr('id'))) !== false) {
			data.push({
						html_id : $target.attr('id'),
						size : $el.attr('data-image-size') || null,
						value : $el.attr('data-image-rotate') || null,
						pk : $target.attr('data-media-pk')
					})
			// Dajaxice.medias.remove(Dajax.process, data);
		}
	});
	Dajaxice.medias.mass_unremove(Dajax.process, {
				datas : data
			});
}

$(document).ready(function() {

	setupMassAction();

	$('#modal-move #id_name').autocomplete({
				source : function(request, response) {
					$.getJSON('/autocomplete-album/?q=' + request.term,
							response)
				},
				focus : function(event, ui) {
					$('#modal-move #id_name').val(ui.item.label);
					return false;
				},
				select : function(event, ui) {
					$('#modal-move #id_name').val(ui.item.label);
					$('#modal-move #id_album_id').val(ui.item.value);
					return false;
				}
			});

	$('#modal-move').on('show', function() {
		    dajaxiceFormClearErrors('form-move')
		    $('#modal-move #btn-move').parents('li:first').addClass('disabled');
		    $('#modal-move #btn-move').button('reset');
				$('#modal-move #id_name').val('');
				$('#modal-move #id_album_id').val('');
			});

	$('#modal-move #btn-move').click(function(e) {
		e.preventDefault();
     
		$(this).button('loading');
		
		if ($('#modal-move #id_new_album').is(':checked')) {
			var data = {
				'album_name' : $('#modal-move #id_name').val(),
				create : true
			};
		} else {
			var data = {
				'album_pk' : $('#modal-move #id_album_id').val()
			};
		}

		data.medias = [];

		$('.thumbnail.published input[type=checkbox]:checked').each(
				function(idx, el) {
					data.medias.push($(el).parents('.thumbnail')
							.attr('data-media-pk'));
				});
		Dajaxice.medias.move(Dajax.process, data);
	})

	$('.thumbnail input[type=checkbox]').change(function() {

				setupMassAction();

				if ($(this).is(':checked')) {
					selectMedia($(this).parents('.thumbnail'));
				} else {
					unSelectMedia($(this).parents('.thumbnail'));
				}
			});

	$('[data-select-all]').click(function(e) {
				e.preventDefault();
				$('.thumbnail').each(function(idx, el) {
							selectMedia($(el));
						});
				setupMassAction();
			});

	$('[data-unselect-all]').click(function(e) {
				e.preventDefault();
				$('.thumbnail').each(function(idx, el) {
							unSelectMedia($(el));
						});
				setupMassAction();
			});

	$('[data-revert-selection]').click(function(e) {
				e.preventDefault();
				$('.thumbnail').each(function(idx, el) {
							if ($(el).find('input[type=checkbox]')
									.is(':checked')) {
								unSelectMedia($(el));
							} else {
								selectMedia($(el));
							}
						});
				setupMassAction();
			});

	$('[data-image-rotate]').click(function(e) {
		e.preventDefault();

		var $el = $(e.currentTarget);
		if ($el.parents('li').hasClass('mass-media-action')) {
			disableMassAction();
			mass_media_rotate($el,
					$('.media-select input[type=checkbox]:checked'));
		} else {
			media_rotate($el);
		}

	});

	$('[data-media-remove]').click(function(e) {

		e.preventDefault()

		var $el = $(e.currentTarget);
		if ($el.parents('li').hasClass('mass-media-action')) {
			disableMassAction();
			mass_media_remove($el,
					$('.media-select input[type=checkbox]:checked'));
		} else {
			media_remove($el);
		}

	});

	$('[data-media-unremove]').click(function(e) {

		e.preventDefault()

		var $el = $(e.currentTarget);
		if ($el.parents('li').hasClass('mass-media-action')) {
			disableMassAction();
			mass_media_unremove($el,
					$('.media-select input[type=checkbox]:checked'));
		} else {
			media_unremove($el);
		}

	});

});