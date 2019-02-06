/**
 * Polling for exercise status.
 *
 */
;(function($, window, document, undefined) {
	"use strict";

	var pluginName = "aplusExercisePoll";
	var defaults = {
    poll_url_attr: "data-poll-url",
		poll_delays: [2,3,5,5,5,10,10,10,10],
		message_selector: ".progress-bar",
		message_attr: {
			error: "data-msg-error",
			timeout: "data-msg-timeout"
		}
  };

	function AplusExercisePoll(element, callback, options) {
		this.element = $(element);
		this.callback = callback;
		this.settings = $.extend({}, defaults, options);
		this.url = null;
		this.count = 0;
		this.init();
	}

	$.extend(AplusExercisePoll.prototype, {

		/**
		 * Constructs contained exercise elements.
		 */
		init: function() {
			this.element.removeClass("hide");
			this.url = this.element.attr(this.settings.poll_url_attr);
			this.schedule();
		},

		poll: function(firstTime) {
			var poller = this;
			$.ajax(this.url, {dataType: "html"})
				.fail(function() {
					poller.message("error");
				})
				.done(function(data) {
					poller.count++;
					if (data.trim() === "ready" || data.trim() === "error" || data.trim() === "unofficial") {
						poller.ready();
					} else if (poller.element.is(":visible")) {
						if (poller.count < poller.settings.poll_delays.length) {
							poller.schedule();
						} else {
							poller.message("timeout");
						}
					}
				});
		},

		schedule: function() {
			var poller = this;
			setTimeout(function() { poller.poll(); },
				this.settings.poll_delays[this.count] * 1000);
		},

		ready: function() {
			this.element.hide();
			var suburl = this.url.substr(0, this.url.length - "poll/".length);
			if (this.callback) {
				this.callback(suburl);
			} else {
				window.location = suburl;
			}
	    },

		message: function(messageType) {
			this.element.removeClass("active").find(this.settings.message_selector)
				.text(this.element.attr(this.settings.message_attr[messageType]));
			if (messageType == "error") {
				this.element.addClass("progress-bar-danger");
			}
		},

	});

	$.fn[pluginName] = function(callback, options) {
		return this.each(function() {
			if (!$.data(this, "plugin_" + pluginName)) {
				$.data(this, "plugin_" + pluginName, new AplusExercisePoll(this, callback, options));
			}
		});
	};

  $.aplusExerciseDetectWaits = function(callback) {
    $(".exercise-wait").aplusExercisePoll(callback);
  };

})(jQuery, window, document);

jQuery(function() {
	jQuery.aplusExerciseDetectWaits();
});
