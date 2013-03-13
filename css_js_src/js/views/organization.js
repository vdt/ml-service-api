waitForSchema(function() {

    OrganizationItemView = ItemView.extend({
        templatename : "organization",
        modeltype: Organization
    });

    OrganizationListView = ListView.extend({
        el: '.course-view',
        collection: OrganizationContainer,
        item: OrganizationItemView
    });

    var view = new OrganizationListView();
    view.render();
});