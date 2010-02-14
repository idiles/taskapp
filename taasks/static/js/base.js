var StatusMessage = {
    show: function (html) {
        var el = $('#notification-inner');
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
        $('.rounded').corner();
        $('.rounded5').corner('5px');
        $('.button').corner('10px');
        $('.control-button').corner('10px');
        $('#header-inner').corner('bl br');
        $('#menubar a').corner();
        $('#notification-inner').corner('bl br');
        
        var messages = $('#notification-container').html();
        if (messages) {
            StatusMessage.show(messages);
        }
        
        $('button.connect').click(function () {
           var username = $(this).attr('rel');
           $.post(url('{% url account:connect 0 %}', {0: username}), {},
                function () {
                    $('#profile-' + username).addClass('waiting-user-profile');
                    StatusMessage.show('Connection request sent to ' + username);
                });
        });
        
        $('button.cancel-connection').click(function () {
           var username = $(this).attr('rel');
           $.post(url('{% url account:cancel-connection 0 %}', {0: username}), {},
                function () {
                    $('#profile-' + username).removeClass(
                        'connected-user-profile').removeClass(
                        'waiting-user-profile').removeClass('connection-confirm-profile');
                    StatusMessage.show('Connection with ' + username + ' canceled');
                });
        });
        
        $('button.confirm-connection').click(function () {
           var username = $(this).attr('rel');
           $.post(url('{% url account:confirm-connection 0 %}', {0: username}), {},
                function () {
                    $('#profile-' + username).removeClass(
                        'connection-confirm-profile').removeClass(
                        'waiting-user-profile').addClass('connected-user-profile');
                    StatusMessage.show('You are now connected with ' + username);
                });
        });
    });
})();
