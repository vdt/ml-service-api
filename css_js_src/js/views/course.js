waitForSchema(function() {

    CourseItemView = ItemView.extend({
        templatename : "course"
    });

    CourseListView = ListView.extend({
        el: '.course-view',
        collection: CourseContainer,
        item: CourseItemView
    });

    var view = new CourseListView();
    view.render();
});