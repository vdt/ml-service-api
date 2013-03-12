waitForModel("CourseContainer", function() {

    CourseItemView = ItemView.extend({
        templatename : "course"
    });

    CourseListView = ListView.extend({
        el: '.course-view',
        collection: CourseContainer,
        item: CourseItemView
    });

    var course_view = new CourseListView();
    course_view.render();
});