var DO_NOT_SHOW = ["modified", "created", "resource_uri", "id"];

ListView = Backbone.View.extend({
    tagName: "ul",
    el: '.list-view',
    collection: undefined,
    item: undefined,
    events: {
        "click #add": "addItemForm",
        "click #save-new-item": "saveItem"
    },
    initialize: function(){
        _.bindAll(this, "renderItem", "loadResults", "addItemForm", "saveItem");
        this.courseList = new this.collection;
    },

    renderItem: function(model){
        var courseItemView = new this.item({model: model});
        courseItemView.render();
        $(this.el).append(courseItemView.el);
    },

    render: function(){
        this.loadResults();
        $(this.el).data('adding', false)
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
    addItemForm : function() {
        fields = {};
        var that = this;
        console.log(this.courseList.schema);
        $.getJSON(this.courseList.schema , function(data){
            for (var field in data['fields']){
                if(DO_NOT_SHOW.indexOf(field)==-1)
                {
                    fields[field] = "";
                }
            }
            console.log(data);
            var update_template = $('#generic-item-add-template');
            var update_html = (_.template(update_template.html(), {item: fields, _:_}));
            $(that.el).append(update_html)
            $(that.el).data('adding', true)
        });
    },
    saveItem: function() {
        $(this.el).children("#item-add").remove()
        $(this.el).data('adding', false)
    }
});

ItemView = Backbone.View.extend({
    tagName: "li",
    templatename : "item",
    events: {
        "click a#show": "clicked",
        "click #update": "update",
        "click #delete": "delete"
    },

    initialize: function(){
        _.bindAll(this, "clicked", "render", "update", "delete");
    },

    clicked: function(e){
        e.preventDefault();
        var detail_shown = $(this.el).data('detail')
        if(detail_shown){
            $(this.el).children("#item-detail").remove()
            $(this.el).children("#item-add").remove()
            $(this.el).data('detail', false)
        } else {
            var item_template = $('#' + this.templatename + '-item-detail-template');
            var html = (_.template(item_template.html(), {course: this.model, _:_}));
            var update_template = $('#' + this.templatename + '-item-add-template');
            var update_html = (_.template(update_template.html(), {course: this.model.toJSON(), _:_}));
            $(this.el).append(html);
            $(this.el).append(update_html)
            $(this.el).data('detail', true)
        }
    },

    render: function(){
        var item_template = $('#'+ this.templatename + '-item-template');
        var html = (_.template(item_template.html(), {course: this.model, _:_}));
        $(this.el).append(html);
        $(this.el).data('detail', false)
    },

    update: function() {
        var update_elements = $(this.el).children('#item-add').children('.update');
        var update_dict = {};
        for(var el in update_elements)
        {
            var id = update_elements[el].id
            var value=update_elements[el].value;
            try {
                value = JSON.parse(value);
            }
            catch(err)
            {

            }
            if(id!="" && value!="" && DO_NOT_SHOW.indexOf(id)==-1)
            {
                update_dict[id] = value;
            }
        }
        this.model.save(update_dict, {patch: true});
        $(this.el).children().remove();
        this.render();
    },

    delete: function () {
        $(this.el).remove()
        this.model.destroy();
        this.remove();
    }
});