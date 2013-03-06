CourseView = Backbone.View.extend({
    el: '.course-view',
    initialize: function () {
        // isLoading is a useful flag to make sure we don't send off more than
        // one request at a time
        this.isLoading = false;
        this.courseList = new CourseList();
        _.bindAll(this, 'render'); // fixes loss of context for 'this' within methods
        this.render(); // not all views are self-rendering. This one is.
    },
    render: function () {
        this.loadResults();
    },
    loadResults: function () {
        var that = this;
        // we are starting a new load of results so set isLoading to true
        this.isLoading = true;
        // fetch is Backbone.js native function for calling and parsing the collection url
        this.courseList.fetch({
            success: function (courses) {
                // Once the results are returned lets populate our template
                $(that.el).append(_.template($('#course-list-template').html(), {courses: courses.models, _:_}));
                // Now we have finished loading set isLoading back to false
                that.isLoading = false;
            }
        });
    },
    // This will simply listen for scroll events on the current el
    events: {
        'scroll': 'checkScroll'
    },
    checkScroll: function () {
        var triggerPoint = 100; // 100px from the bottom
        if( !this.isLoading && this.el.scrollTop + this.el.clientHeight + triggerPoint > this.el.scrollHeight ) {
            this.courseCollection.page += 1; // Load next page
            this.loadResults();
        }
    }
});

$(document).ready(function() {
    course_view = new CourseView()
});