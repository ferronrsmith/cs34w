/**
 * The following function converts youtube/vimeo url to links
 */
String.prototype.linkify = function () {
    "use strict";
    var urlPattern = /http:\/\/(?:www\.)?(vimeo|youtube)\.com\/(?:watch\?v=)?([\s\S]*?)(?:\z|$|&feature=related|&)/mgi;
    return this
        .replace(urlPattern, '<a href="$&" class="omebed"></a>');
};

