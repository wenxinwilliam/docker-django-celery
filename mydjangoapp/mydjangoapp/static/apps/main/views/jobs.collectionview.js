
var Jobs = require('../models/jobs.collection.js')
var tpl = require('../templates/jobs.tpl.html')

var JobView = Backbone.Marionette.ItemView.extend({
	
	template: tpl,

	model: new Jobs(),

    modelEvents:{
    	'sync': 'render'
	},

	initialize: function(options){
		// this.model = options.model;
		// this.template = options.template ? options.template : tpl;
		// this.model = options.model ? options.model : model;
		this.model.fetch();
	},

	templateHelpers: function(){
		return {jobs: this.model.toJSON()}
	}

});

module.exports = JobView