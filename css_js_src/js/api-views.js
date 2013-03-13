var DO_NOT_SHOW = ["modified", "created", "resource_uri", "id"];

ListView = Backbone.View.extend({
    tagName: "ul",
    el: '.list-view',
    collection: undefined,
    item: undefined,
    events: {
        "click #add": "addItemForm",
        "click #save-new-item": "saveItem",
        'click a#prev': 'previous',
        'click a#next': 'next'
    },
    initialize: function(){
        _.bindAll(this, "renderItem", "loadResults", "addItemForm", "saveItem", "previous", "next", "render");
        this.itemList = new this.collection;
    },

    renderItem: function(model){
        var allItemView = new this.item({model: model});
        allItemView.render();
        $(this.el).append(allItemView.el);
    },

    render: function(){
        this.loadResults();
        $(this.el).data('adding', false)
    },

    loadResults: function () {
        var that = this;
        // fetch is Backbone.js native function for calling and parsing the collection url
        this.itemList.fetch({
            success: function (items) {
                // Once the results are returned lets populate our template
                for(model in items.models)
                {
                    that.renderItem(items.models[model])
                }
                var pagination_template = $('#pagination-template');
                var update_html = (_.template(pagination_template.html(), that.itemList.pageInfo()));
                $(that.el).append(update_html);
            }
        });
    },
    addItemForm : function() {
        fields = {};
        var that = this;
        if($(this.el).data('adding')==false){
            $.getJSON(this.itemList.schema , function(data){
                for (var field in data['fields']){
                    if(DO_NOT_SHOW.indexOf(field)==-1)
                    {
                        fields[field] = "";
                    }
                }
                console.log(data);
                var update_template = $('#generic-item-add-template');
                var update_html = (_.template(update_template.html(), {item: fields, _:_}));
                $(that.el).prepend(update_html);
                $(that.el).data('adding', true);
            });
        } else {
            $(this.el).children("#item-add").remove();
            $(this.el).data('adding', false);
        }
    },
    saveItem: function() {
        var update_elements = $(this.el).children('#item-add').children('.new-item');
        var new_item = new this.item;
        new_item.add(update_elements);
        this.itemList.add(new_item);
        $(this.el).children("#item-add").remove();
        $(this.el).data('adding', false);
    },
    previous: function() {
        this.itemList.previousPage();
        this.render();
    },
    next: function() {
        this.itemList.nextPage();
        this.render();
    },
    remove_data: function(){
        $(this.el).empty();
    }
});

ItemView = Backbone.View.extend({
    tagName: "li",
    templatename : "item",
    modeltype: undefined,
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
            var html = (_.template(item_template.html(), {item: this.model, _:_}));
            var update_template = $('#' + this.templatename + '-item-add-template');
            var update_html = (_.template(update_template.html(), {item: this.model.toJSON(), _:_}));
            $(this.el).append(html);
            $(this.el).append(update_html)
            $(this.el).data('detail', true)
        }
    },

    render: function(){
        var item_template = $('#'+ this.templatename + '-item-template');
        var html = (_.template(item_template.html(), {item: this.model, _:_}));
        $(this.el).append(html);
        $(this.el).data('detail', false)
    },
    update: function() {
        var update_elements = $(this.el).children('#item-add').children('.update');
        var update_dict = this.update_base(update_elements)
        this.model.save(update_dict, {patch: true});
        $(this.el).children().remove();
        this.render();
    },
    update_base: function(update_elements) {
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
        return update_dict;
    },
    add: function(update_elements) {
        var update_dict = this.update_base(update_elements);
        this.model = new this.modeltype;
        this.model.save(update_dict,{
            success: function() {},
            wait: false
        });
    },
    delete: function () {
        $(this.el).remove()
        this.model.destroy();
        this.remove();
    }
});