waitForModel("UserContainer", function() {
    waitForModel("User", function() {
        UserItemView = ItemView.extend({
            templatename : "user",
            modeltype: User
        });

        UserListView = ListView.extend({
            el: '.user-view',
            collection: UserContainer,
            item: UserItemView
        });

        var user_view = new UserListView();
        user_view.render();
    });
});