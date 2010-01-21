var StatusMessage = {
    show: function (html) {
        var el = $('#notification');
        if (html) {
            el.html(html);
        }
        el.slideDown();
        setTimeout(function () {
            el.slideUp();
        }, 5000);
    }
};

(function () {
    // Define a global namespace
    if (window.T === undefined) {
        window.T = {};
    }

    // Explicitly define function url in global namespace
    window.url = function (real_url, params) {
        if (params === undefined) {
            return real_url;
        }
        for (var val in params) {
            if (params.hasOwnProperty(val)) {
                real_url = real_url.replace(val, params[val]);
            }
        }
        return real_url;
    }
    
    $(document).ready(function () {
        // alert('esu');
        var messages = $('#notification-container').html();
        // alert('"' + messages + '"');
        if (messages) {
            StatusMessage.show(messages);
        }
    });
})();
