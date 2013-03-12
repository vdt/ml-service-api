CourseItem = Backbone.Model.extend({
    defaults: {
        'id' : null,
        'users' : null,
        'organizations' : null,
        'problems' : null,
        'course_name' : null
    }
});

CourseList = Backbone.Collection.extend({
    url: function() {return "/essay_site/api/v1/course/?format=json";},
    username: null,
    api_key: null,
    model : CourseItem
});