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
})();
