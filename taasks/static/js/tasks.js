// Protect the global namespace
(function ($) {

// Create a new task object assigning the given text to it
var Task = function (src) {
    if (typeof src === 'string') {
        // We have a new text for task - create it now
        this.create(src);
    } else {
        // Just init the existing node (most probably page load)
        this.node = $(src);
        this.id = this.node.attr('id').substring('task-'.length);
    }
    // Let the task node remember the object
    this.node.data('T.task', this);

    this.textNode = this.node.find('div.text');
    // Is it safe to assume this?
    this.inputNode = this.textNode.next();
    this.indicatorNode = this.node.find('div.indicator');
    this.addCallbacks();
};

// Init an existing task object given the node
Task.init = function (node) {
    new Task(node);
};

// Show/hide the empty-task-list message depending on 'show' parameter. If not
// provided then it is computed automatically
Task.toggleTaskListEmpty = function (show) {
    if (show === undefined) {
        show = $('#tasks').children().length === 0;
    }
    var emptyTaskList = $('#empty-task-list'),
        visible = emptyTaskList.is(':visible');
    if (!visible && show) {
        emptyTaskList.fadeIn();
    } else if (visible && !show) {
        emptyTaskList.hide();
    }
};

Task.prototype = {
    create: function (text) {
        var that = this,
            template, args;
        this.node = $('#task-template').children().clone().hide();

        args = {
            'title': text
        };
        $.post(url('{% url tasks:create %}'), args, function (json) {
            that.node.attr('id', json.id);
            that.node.find('.text').html(json.html);
            that.id = json.id;
        }, 'json');

        Task.toggleTaskListEmpty(false);

        this.node.find('div.text').text(text);
        this.node.appendTo($('#tasks')).fadeIn();
    },

    save: function (text) {
        that = this;
        $.post(url('{% url tasks:update 0 %}', {0: this.id}), {
            title: text
        }, function (json) {
            that.textNode.html(json.html)
        }, 'json');
    },

    start: function (notify) {
        // If removing the class is not enough to stop a task then uncomment
        // this
        //$('#tasks > div.task-active').data('T.task').stop();
        $('#tasks > div.task-active').removeClass('task-active');

        this.node.addClass('task-active');
        $('#timer').addClass('timer-running');

        this.indicatorNode.click();
        if (notify) {
            $.post(url('{% url tasks:start 0 %}', {0: this.id}));
        }
    },

    stop: function (notify) {
        this.node.removeClass('task-active');
        $('#timer').removeClass('timer-running');

        this.indicatorNode.click();
        if (notify) {
            $.post(url('{% url tasks:stop 0 %}', {0: this.id}));
        }
    },

    done: function (notify) {
        this.node.addClass('task-completed');
        if (notify) {
            $.ajax({
                url: '/tasks/' + this.id,
                data: { 'task[completed]': 1 },
                type: 'PUT',
                success: function () {
                }
            });
        }
    },

    undone: function (notify) {
        this.node.removeClass('task-completed');
        if (notify) {
            $.ajax({
                url: '/tasks/' + this.id,
                data: { 'task[completed]': 0 },
                type: 'PUT',
                success: function () {
                }
            });
        }
    },

    remove: function (notify) {
        var node = this.node;
        node.fadeOut('', function () {
            node.remove();
            Task.toggleTaskListEmpty();
        });
        if (notify) {
            $.post(url('{% url tasks:remove 0 %}', {0: this.id}), {});
        }
    },

    addCallbacks: function () {
        var that = this,
            $body = $('body');

        // Blur the inputNode and show the textNode
        function blurInput () {
            // First unbind the blur bound to body
            $body.unbind('click', bodyBlurInput);
            // hide the input
            that.inputNode.blur().hide();
            // show the div
            that.textNode.show();
        }

        // Save the inputNode value and switch to textNode
        // This is assumed to be bound to body.click
        function bodyBlurInput (event) {
            // If we're clicking outside of the input
            if (!$(event.target).closest('input.task-input').length) {
                that.save(that.inputNode.val());
                blurInput();
            }
        }

        this.textNode.click(function (event) {
            var text = that.textNode;
            // Hide the div
            text.hide();
            // Set the input value to text and show the input
            that.inputNode.val(text.text()).show().focus();
            // If we click outside then save and switch to textNode (same as if
            // enter was pressed)
            $body.click(bodyBlurInput);
            // Don't let body catch this click at once
            return false;
        });

        this.inputNode.keydown(function (e) {
            if (e.keyCode === 13) {
                // If enter then save the value
                that.save(that.inputNode.val());
            }
            if (e.keyCode === 13 || e.keyCode === 27) {
                // If enter or escape then just switch to textNode
                blurInput();
            }
        });

        this.indicatorNode.click(function (event) {
            var wasSelected = that.node.hasClass('selected');
            $('#tasks > div.task').removeClass('selected').find(
                    'div.edit-view').hide();
            if (wasSelected) {
                $('#tasks').sortable('enable');
            } else {
                that.node.addClass('selected').find('div.edit-view').slideDown(
                        80);
                $('#tasks').sortable('disable');
            }
        });

        this.node.find('span.done-button').click(function (event) {
            that.stop();
            that.done(true);
        });
        this.node.find('span.undone-button').click(function (event) {
            that.undone(true);
        });

        this.node.find('span.start-button').click(function (event) {
            that.start(true);
        });
        this.node.find('span.stop-button').click(function (event) {
            that.stop(true);
        });

        this.node.find('span.remove-button').click(function (event) {
            that.remove(true);
        });
    }
};

var StatusMessage = {
    show: function (text) {
        var el = $('#status-message');
        if (text) {
            el.text(text);
        }
        el.slideDown();
        setTimeout(function () {
            el.slideUp();
        }, 5000);
    }
};

$(document).ready(function () {
    var addTaskButton = $('#add-task-button'),
        mainTaskInput = $('#main-task-input'),
        tasks;

    $('#main-task-input').focus().keyup(function (event) {
        if (event.keyCode == 13) {
            if ($(this).val()) {
                addTaskButton.click();
            }
        }
    });
    
    $('#add-task-button').click(function () {
        new Task(mainTaskInput.val());
        mainTaskInput.val('');
    });
    
    $('#view-examples').click(function () {
        alert('TODO');
        return false;
    });
    
    tasks = $('#tasks > div.task');
    tasks.each(function () {
        Task.init(this);
    });
    
    $('#tasks:not(.archive)').sortable({
        placeholder: 'drop-highlight',
        axis: 'y',
        update: function (event, ui) {
            var ids = $('#tasks').sortable('toArray');
            var data = { ids: $.json.encode(ids) };
            $.post('/tasks/sort', data);
        },
        // After a drag the click event is initiated. In order to prevent it we
        // substitute the jQuery click handlers with our own click handler.
        stop: function (event, ui) {
            var events = $(event.originalTarget).data('events'),
                clickEvents, e, origHandler;
            if (events && events.hasOwnProperty('click')) {
                clickEvents = events.click;
                for (e in clickEvents) {
                    if (clickEvents.hasOwnProperty(e)) {
                        origHandler = clickEvents[e];
                        // All our function does is puts the original event
                        // handler back so that it would fire normally next time
                        clickEvents[e] = function () {
                            clickEvents[e] = origHandler;
                        };
                    }
                }
            }
            
            // Fix the broken position
            ui.item.css({
                position: '',
                left: '',
                top: '',
                display: ''
            });
        }
    });
    
    $('#archive-button').click(function () {
    });
});

})(jQuery);
