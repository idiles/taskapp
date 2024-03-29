// Protect the global namespace
(function ($) {
    
var Project = function () {
};

Project.get_slug = function () {
    return $('#project-slug').val(); 
}

var task_children = {};

// Create a new task object assigning the given text to it
var Task = function (src) {
    if (typeof src === 'string') {
        // We have a new text for task - create it now
        this.create(src);
    } else {
        // Just init the existing node (most probably page load)
        this.node = $(src);
        this.id = this.node.attr('id').substring('task-'.length);
        this.children = task_children[this.id];
    }
    // Let the task node remember the object
    this.node.data('T.task', this);

    this.textNode = this.node.find('div.text');
    // Is it safe to assume this?
    this.inputNode = this.textNode.next();
    this.indicatorNode = this.node.find('div.indicator');
    this.indent_value = parseInt(this.node.find('input.indent').val());
    this.addCallbacks();
    
    this.updateControls();
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
    create: function (text, create) {
        var that = this,
            template, args;
        this.node = $('#task-template').children().clone().hide();

        args = {
            'title': text
        };
        
        if (create === undefined || create === true) {
            $.post(url('{% url tasks:create 0 %}', {0: Project.get_slug()}), 
                    args, function (json) {
                that.node.attr('id', 'task-' + json.id);
                that.node.find('.text').html(json.html);
                that.node.find('span.time').text(json.time);
                that.id = json.id;
                this.children = task_children[that.id];
                that.indent_value = 0;
            }, 'json');
        }

        Task.toggleTaskListEmpty(false);

        this.node.find('div.text').text(text);
        this.node.appendTo($('#tasks')).fadeIn();
    },

    save: function (text) {
        if (text == '') {
            text = 'Untitled';
        }
        
        that = this;
        $.post(url('{% url tasks:update 0 1 %}', 
            {0: Project.get_slug(), 1: this.id}), 
                {title: text}, function (json) {
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
            $.post(url('{% url tasks:start 0 1 %}', 
                {0: Project.get_slug(), 1: this.id}));
            TimeTracker.start();
            StatusMessage.show('Time tracker is now running');
        }
    },

    stop: function (notify) {
        this.node.removeClass('task-active');
        $('#timer').removeClass('timer-running');

        this.indicatorNode.click();
        if (notify) {
            $.post(url('{% url tasks:stop 0 1 %}', 
                {0: Project.get_slug(), 1: this.id}));
            TimeTracker.stop();
            StatusMessage.show('Time tracker has been stopped');
        }
    },

    done: function (notify, no_commit) {
        this.node.addClass('task-done');
        // this.indicatorNode.click();
        if (notify) {
            if (no_commit === undefined) {
                $.post(url('{% url tasks:done 0 1 %}', 
                    {0: Project.get_slug(), 1: this.id}));
                $('#archive-completed-action').fadeIn();
            }
        }
        
        for (var i = 0; i < this.children.length; i++) {
            this.getTaskById(this.children[i]).done(true, true);
        }
    },

    undone: function (notify, no_commit) {
        this.node.removeClass('task-done');
        var task = this.node;
        // this.indicatorNode.click();
        if (notify) {
            if (no_commit === undefined) {
                $.post(url('{% url tasks:undone 0 1 %}', 
                        {0: Project.get_slug(), 1: this.id}), {},
                    function () {
                        if (task.hasClass('task-archived')) {
                            window.location.reload(true);
                        }
                    }
                );
            }
        }
        
        for (var i = 0; i < this.children.length; i++) {
            this.getTaskById(this.children[i]).undone(true, true);
        }
    },

    remove: function (notify, no_commit) {
        var node = this.node;
        
        node.fadeOut('', function () {
            node.remove();
            Task.toggleTaskListEmpty();
        });
        
        if (notify) {
            if (no_commit === undefined) {
                $.post(url('{% url tasks:remove 0 1 %}', 
                    {0: Project.get_slug(), 1: this.id}), {});
                StatusMessage.show('Task moved to Trash');
            }
        }
        
        for (var i = 0; i < this.children.length; i++) {
            this.getTaskById(this.children[i]).remove(true, true);
        }
    },
    
    restore: function (no_commit) {
        var node = this.node;
        node.fadeOut('', function () {
            node.remove();
            Task.toggleTaskListEmpty();
        });
        
        if (no_commit === undefined) {
            $.post(url('{% url tasks:restore 0 1 %}', 
                    {0: Project.get_slug(), 1: this.id}), {},
                function () {
                    StatusMessage.show('Task has been restored');
                });
        }
        
        for (var i = 0; i < this.children.length; i++) {
            this.getTaskById(this.children[i]).restore(true);
        }
    },
    
    indent: function (direction, no_commit) {
        var old_indent = this.indent_value;
        
        if (direction == 'left') {
            if (this.indent_value > 0) {
                this.indent_value -= 1;
            }
        } else if (direction == 'right') {
            this.indent_value += 1;
        }
        
        this.node.removeClass('task-indent-' + old_indent);
        this.node.addClass('task-indent-' + this.indent_value);
        
        if (no_commit === undefined) {
            $.post(url('{% url tasks:indent 2 1 0 %}', 
                {'2': Project.get_slug(), '1': this.id, '0': direction}));
        }
        
        this.updateControls();
        
        for (var i = 0; i < this.children.length; i++) {
            this.getTaskById(this.children[i]).indent(direction, true);
        }
    },
    
    updateControls: function () {
        if (this.indent_value == 0) {
            this.node.find('span.indent-left').hide();
        } else {
            this.node.find('span.indent-left').show();
        }
        
        if (this.indent_value == 3) {
            this.node.find('span.indent-right').hide();
        } else {
            this.node.find('span.indent-right').show();
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
            if (that.node.hasClass('task-removed')) {
                return;
            }
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
        
        // TODO: Clicking will not work for new tasks until page is 
        // reloaded. This code should be fixed.
        this.node.find('span.tag').click(function (event) {
           var tag = $(this).text();
           tag = tag.substr(1, tag.length);
           
           window.location = url('{% url tasks:tasks 0 %}?tag=' + tag,
               {'0': Project.get_slug()});
           event.stopPropagation();
        });
        
        this.node.find('span.due-date').click(function (event) {
           var due = $(this).text();
           due = due.substr(1, due.length);
           window.location = url('{% url tasks:tasks 0 %}?due=' + due,
               {'0': Project.get_slug()});
           event.stopPropagation();
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
        
        this.node.find('span.indent-left').click(function (event) {
            that.indent('left');
        });
        
        this.node.find('span.indent-right').click(function (event) {
            that.indent('right');
        });
        
        this.node.find('button.restore-button').click(function (event) {
            that.restore();
        });
        
        if (this.node.hasClass('task-active')) {
            if (! $('#timer').hasClass('timer-running')) {
                $('#timer').addClass('timer-running');
            }
            if (! TimeTracker.active) {
                TimeTracker.start();
            }
        }
    },
    
    getTaskById: function (id) {
        return new Task($('#task-' + id));
        
    }
};


var TimeTracker = {
    active: false,
    
    start: function () {
        TimeTracker.active = true;
        TimeTracker.update();
    },
    
    stop: function () {
        TimeTracker.active = false;
    },
    
    update: function () {
        $.ajax({
            url: '{% url tasks:time %}', 
            cache: false,
            dataType: 'json', 
            success: function (json) {
                $('#timer span.time').text(json.today);
                for (var i = 0; i < json.tasks.length; i++) {
                    var task = json.tasks[i];
                    $('#task-' + task.id + ' span.time').text(task.time);
                }
            }
        });
        
        if (TimeTracker.active) {
            setTimeout(TimeTracker.update, 20000);
        }
    }
};


$(document).ready(function () {
    $('#add-task-button').click(function () {
        var task = new Task('');
        var text = task.textNode;
        text.hide();
        task.inputNode.val(text.text()).show().focus();
    });
    
    $('#create-project-button').click(function () {
        $(this).hide(); 
        $('#project-form').slideDown();
    });
    
    $('#view-examples').click(function () {
        alert('TODO');
        return false;
    });
    
    task_children = $.evalJSON($('#task-children').val());
    
    var tasks = $('#tasks > div.task');
    tasks.each(function () {
        Task.init(this);
        if ($(this).hasClass('task-done')) {
            $('#archive-completed-action').show();
        }
    });
    
    $('#archive-completed-action').click(function () {
        $.post(url('{% url tasks:archive_completed 0 %}', 
            {'0': Project.get_slug()}), null, 
            function (response_data) {
                var response = $.evalJSON(response_data);
                
                var tasks = $('#tasks > div.task');
                tasks.each(function () {
                    if ($(this).hasClass('task-done')) {
                        $(this).fadeOut();
                    }
                });
                
                StatusMessage.show(response.archived + ' tasks moved to archive');
            }
        );
        
        return false;
    });
    
    $('#tasks:not(.archive)').sortable({
        placeholder: 'drop-highlight',
        axis: 'y',
        update: function (event, ui) {
            var ids = $('#tasks').sortable('toArray');
            var data = { ids: $.toJSON(ids) };
            $.post(url('{% url tasks:sort 0 %}', {0: Project.get_slug()}), 
                data);
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
});

})(jQuery);
