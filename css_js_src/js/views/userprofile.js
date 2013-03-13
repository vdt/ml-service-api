waitForModel("UserprofileContainer", function() {
    waitForModel("Userprofile", function() {
        UserprofileItemView = ItemView.extend({
            templatename : "userprofile",
            modeltype: Userprofile
        });

        UserprofileListView = ListView.extend({
            el: '.userprofile-view',
            collection: UserprofileContainer,
            item: UserprofileItemView
        });

        var userprofile_view = new UserprofileListView();
        userprofile_view.render();
    });
});