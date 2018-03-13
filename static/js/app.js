/**
 * Created by Thinkpad on 2018/3/12.
 */
var app = (function ($) {
    var config = $('#config'),
        app =JSON.parse(config.text());

    return app;
})(jQuery);