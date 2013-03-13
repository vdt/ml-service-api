/*
 * Backbone-tastypie model generator
 * Created by Marco Montanari
 * released under 3 clause BSD
 */

var PaginatedCollection = Backbone.Collection.extend({
    initialize: function() {
        _.bindAll(this, 'parse', 'url', 'pageInfo', 'nextPage', 'previousPage', 'filtrate', 'sort_by');
        typeof(options) != 'undefined' || (options = {});
        typeof(this.limit) != 'undefined' || (this.limit = 20);
        typeof(this.offset) != 'undefined' || (this.offset = 0);
        typeof(this.filter_options) != 'undefined' || (this.filter_options = {});
        typeof(this.sort_field) != 'undefined' || (this.sort_field = '');
    },
    fetch: function(options) {
        typeof(options) != 'undefined' || (options = {});
        //this.trigger("fetching");
        var self = this;
        var success = options.success;
        options.success = function(resp) {
            //self.trigger("fetched");
            if(success) { success(self, resp); }
        };
        return Backbone.Collection.prototype.fetch.call(this, options);
    },
    parse: function(resp) {
        Backbone.Collection.prototype.initialize.apply(this, arguments);
        this.offset = resp.meta.offset;
        this.limit = resp.meta.limit;
        this.total = resp.meta.total_count;
        return resp.objects;
    },
    url: function() {
        var url = Backbone.Collection.prototype.initialize.apply(this, arguments);
        console.log(url)
        urlparams = {offset: this.offset, limit: this.limit};
        urlparams = $.extend(urlparams, this.filter_options);
        if (this.sort_field) {
            urlparams = $.extend(urlparams, {sort_by: this.sort_field});
        }
        return this.urlRoot + '?' + $.param(urlparams);
    },
    pageInfo: function() {
        var info = {
            total: this.total,
            offset: this.offset,
            limit: this.limit,
            pages: Math.ceil(this.total / this.limit),
            prev: false,
            next: false
        };

        var max = Math.min(this.total, this.offset + this.limit);

        if (this.total == this.pages * this.limit) {
            max = this.total;
        }

        info.range = [(this.offset + 1), max];

        if (this.offset > 0) {
            info.prev = (this.offset - this.limit) || 1;
        }

        if (this.offset + this.limit < info.total) {
            info.next = this.offset + this.limit;
        }

        return info;
    },
    nextPage: function() {
        if (!this.pageInfo().next) {
            return false;
        }
        this.offset = this.offset + this.limit;
        return this.fetch();
    },
    previousPage: function() {
        if (!this.pageInfo().prev) {
            return false;
        }
        this.offset = (this.offset - this.limit) || 0;
        return this.fetch();
    },
    filtrate: function (options) {
        this.filter_options = options || {};
        this.offset = 0;
        return this.fetch();
    },
    sort_by: function (field) {
        this.sort_field = field;
        this.offset = 0;
        return this.fetch();
    }

});

var PaginatedView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'previous', 'next', 'render');
        this.collection.bind('reset', this.render);
    },
    events: {
        'click a.prev': 'previous',
        'click a.next': 'next'
    },
    render: function() {
        this.el.html(app.templates.pagination(this.collection.pageInfo()));
    },

    previous: function() {
        this.collection.previousPage();
        return false;
    },

    next: function() {
        this.collection.nextPage();
        return false;
    }
});

(function( undefined ) {

    Backbone.SchemaUrl = "";
    Backbone.LoadModelsFromUrl = function(url, models){
        Backbone.SchemaUrl =url;
        $.getJSON(Backbone.SchemaUrl , function(data){
            Backbone.LoadModels(data, models)
            _schema_loaded = true
        });
    }

    Backbone.LoadModels = function(object, models){
        for (var model in object){
            var _mdl = {};
            _mdl['name'] = Backbone.ModelNameGenerator (model);
            _mdl['url'] = object[model]['list_endpoint'].slice(0,-1);
            _mdl['container_name'] = Backbone.ModelNameGenerator (model)+"Container";
            _mdl['schema'] = object[model]['schema'] + "?format=json";

            _mdl['validator'] = {};

            window[_mdl['name']] = Backbone.Model.extend({
                urlRoot: _mdl['url'],
                validate: _mdl['validator'],
                schema : _mdl['schema'],
                options: {}
            });

            window[_mdl['container_name']] = Backbone.Collection.extend({
                urlRoot: _mdl['url'],
                model: window[_mdl['name']],
                schema : _mdl['schema'],
                options : {},
                limit : 20,
                offset : 0,
                pageInfo: function() {
                    var info = {
                        total: this.total,
                        offset: this.offset,
                        limit: this.limit,
                        pages: Math.ceil(this.total / this.limit),
                        prev: false,
                        next: false
                    };

                    var max = Math.min(this.total, this.offset + this.limit);

                    if (this.total == this.pages * this.limit) {
                        max = this.total;
                    }

                    info.range = [(this.offset + 1), max];

                    if (this.offset > 0) {
                        info.prev = (this.offset - this.limit) || 1;
                    }

                    if (this.offset + this.limit < info.total) {
                        info.next = this.offset + this.limit;
                    }

                    return info;
                },
                nextPage: function() {
                    if (!this.pageInfo().next) {
                        return false;
                    }
                    this.offset = this.offset + this.limit;
                    return this.fetch();
                },
                previousPage: function() {
                    if (!this.pageInfo().prev) {
                        return false;
                    }
                    this.offset = (this.offset - this.limit) || 0;
                    return this.fetch();
                }
            });
        }
    }

    Backbone.ModelNameGenerator = function (string)
    {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }


    Backbone.TPValidator = function(model, attrib_set){
        var url = model.url();

    }

    Backbone.Validators = {};

    Backbone.Validators['string'] = function(attribute, value){
        if (typeof value != "string")
            return "Not valid string for attribute "+attribute;
    }

    Backbone.Validators['object']= function(attribute, value){
        if (typeof value != "object")
            return "Not valid object for attribute "+attribute;
    }

    Backbone.Validators['number']= function(attribute, value){
        if (typeof value != "number")
            return "Not valid number for attribute "+attribute;
    }
    Backbone.Validators['boolean']= function(attribute, value){
        if (typeof value != "boolean")
            return "Not valid boolean for attribute "+attribute;
    }

})();