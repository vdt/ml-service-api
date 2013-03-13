waitForModel("CourseContainer", function() {
    waitForModel("Course", function() {
        CourseItemView = ItemView.extend({
            templatename : "course",
            modeltype: Course
        });

        CourseListView = ListView.extend({
            el: '.course-view',
            collection: CourseContainer,
            item: CourseItemView
        });

        var course_view = new CourseListView();
        course_view.render();
    });
});