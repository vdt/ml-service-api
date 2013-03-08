CourseListView = Backbone.View.extend({
    tagName: "ul",
    el: '.course-view',
    initialize: function(){
        _.bindAll(this, "renderItem", "loadResults");
        this.courseList = new CourseList();
    },

    renderItem: function(model){
        var courseItemView = new CourseItemView({model: model});
        courseItemView.render();
        $(this.el).append(courseItemView.el);
    },

    render: function(){
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
                console.log(courses.models);
                for(model in courses.models)
                {
                    that.renderItem(courses.models[model])
                }
            }
        });
    },
});

CourseItemView = Backbone.View.extend({
    tagName: "li",
    events: {
        "click a": "clicked"
    },

    clicked: function(e){
        e.preventDefault();
        detail_shown = $(this.el).data('detail')
        if(detail_shown){
            $(this.el).children("#item-detail").remove()
            $(this.el).data('detail', false)
        } else {
            var item_template = $('#course-item-detail-template');
            var html = (_.template(item_template.html(), {course: this.model, _:_}));
            $(this.el).append(html);
            $(this.el).data('detail', true)
        }
    },

    render: function(){
        var item_template = $('#course-item-template');
        var html = (_.template(item_template.html(), {course: this.model, _:_}));
        $(this.el).append(html);
        $(this.el).data('detail', false)
    }
});

$(document).ready(function() {
    var view = new CourseListView();
    view.render();
});