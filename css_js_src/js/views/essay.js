waitForModel("EssayContainer", function() {
    waitForModel("Essay", function() {
        EssayItemView = ItemView.extend({
            templatename : "essay",
            modeltype: Essay
        });

        EssayListView = ListView.extend({
            el: '.essay-view',
            collection: EssayContainer,
            item: EssayItemView
        });

        var essay_view = new EssayListView();
        essay_view.render();
    });
});