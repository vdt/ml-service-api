CourseView = Backbone.View.extend({
    el: '.course-view',
    initialize: function () {
        // isLoading is a useful flag to make sure we don't send off more than
        // one request at a time
        this.isLoading = false;
        this.courseList = new CourseList();
        _.bindAll(this, 'render', 'loadResults'); // fixes loss of context for 'this' within methods
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
});

var CourseItemViewOld = Backbone.View.extend({
    tagName: 'li', // name of tag to be created
    initialize: function () {
        // isLoading is a useful flag to make sure we don't send off more than
        // one request at a time
        _.bindAll(this, 'render', 'unrender', 'swap', 'remove', 'loadResults'); // every function that uses 'this' as the current object should be in here
        this.model.bind('remove', this.unrender);
    },
    events: {
        'click span.swap':  'swap',
        'click span.delete': 'remove'
    },
    initialize: function(){
        _.bindAll(this, 'render', 'unrender', 'swap', 'remove', 'loadResults'); // every function that uses 'this' as the current object should be in here
        this.model.bind('remove', this.unrender);
    },
    render: function () {
        return(_.template($('#course-list-template').html(), {courses: this.model, _:_}));
    },
    unrender: function(){
        $(this.el).remove();
    },
    remove: function(){
        this.model.destroy();
    }
});

var CourseListViewOld = Backbone.View.extend({
    el: '.course-view', // el attaches to existing element
    events: {
        'click button#add': 'addItem'
    },
    loadResults: function () {
        var that = this;
        // we are starting a new load of results so set isLoading to true
        this.isLoading = true;
        // fetch is Backbone.js native function for calling and parsing the collection url
        this.courseList.fetch({
            success: function (courses) {
                // Once the results are returned lets populate our template
                that.appendItem(courses.models);
                // Now we have finished loading set isLoading back to false
                that.isLoading = false;
            }
        });
    },
    initialize: function(){
        _.bindAll(this, 'render', 'addItem', 'appendItem'); // every function that uses 'this' as the current object should be in here

        this.isLoading = false;
        this.courseList = new CourseList();
        this.courseList.bind('add', this.appendItem); // collection event binder

        this.counter = 0;
        this.render();
    },
    render: function(){
        var self = this;
        $(this.el).append("<button id='Add'>Add list item</button>");
        $(this.el).append("<ul></ul>");
        this.courseList.fetch()
        _(this.courseList.models).each(function(item){ // in case collection is not empty
            this.appendItem(item);
        }, this);
    },
    addItem: function(){
        this.counter++;
        var courseItem = new CourseItem();
        this.courseList.add(courseItem);
    },
    appendItem: function(item){
        var courseItemView = new CourseItemView({
            model: item
        });
        $(this.el).append(courseItemView.render());
    }
});

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
        var name = this.model.get("name");
        alert(name);
    },

    render: function(){
        var template1 = $('#course-item-template');
        var html = (_.template(template1.html(), {course: this.model, _:_}));
        $(this.el).append(html);
    }
});

$(document).ready(function() {
    //course_view = new CourseView()
    var view = new CourseListView();
    view.render();
});