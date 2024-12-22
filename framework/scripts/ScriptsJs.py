GET_PAGE_READY_STATE_OLD = "return document.readyState"
GET_PAGE_READY_STATE = """(function($, global) {
    if (document.readyState === "complete") {

        function busyBoxIsVisible() {
            return $(".k-loading:visible, .k-loading-image:visible").filter(function(index) {
                return $(this).width() && $(this).height();
            }).length > 0;
        }

        function noActiveAjaxQueries() {
            return global.$ && global.$.active === 0;
        }

        return noActiveAjaxQueries() && !busyBoxIsVisible();
    } else {
        return false;
    }
})(window.jQuery, window)"""
SCROLL_INTO_VIEW = """Element.prototype.documentOffsetTop = function () {
    return this.offsetTop + ( this.offsetParent ? this.offsetParent.documentOffsetTop() : 0 );
};

var top = arguments[0].documentOffsetTop() - ( window.innerHeight / 2 );
window.scrollTo( 0, top );"""
SCROLL_TO_TOP = "window.scrollTo(0, 0);"
SCROLL_TO_DOWN = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
SCROLL_INTO_PAGE = """Element.prototype.documentOffsetTop = function () {
    return this.offsetTop + ( this.offsetParent ? this.offsetParent.documentOffsetTop() : 0 );
};

var top = arguments[1].documentOffsetTop() + arguments[1].clientHeight - (window.innerHeight / 2);
arguments[0].scrollTop = top;"""
CLICK = "arguments[0].click()"
GET_WIDTH = "return arguments[0].clientWidth"
SEND_JQUERY = """javascript: (function(e, s) {
    e.src = s;
    e.onload = function() {
        jQuery.noConflict();
        console.log('jQuery injected');
    };
    document.head.appendChild(e);
})(document.createElement('script'), 'https://code.jquery.com/jquery-3.3.1.min.js')"""
