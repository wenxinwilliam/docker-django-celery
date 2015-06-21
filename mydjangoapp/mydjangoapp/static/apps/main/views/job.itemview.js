
var Job = require('../models/job.model.js')
var tpl = require('../templates/job.tpl.html')

var JobView = Backbone.Marionette.ItemView.extend({
	
	template: tpl,

	ui: {
		'submit': 'button[type="submit"]',
		'jobType': '#job-type',
		'jobArgs': '#job-args',
	},

	events: {
		'click ui.submit': 'createJob'
	},

	model: new Job(),

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
	},

	createJob: function(e){
		e.preventDefault();

		this.model = new Job({
			type: ui.jobType.val(),
			argument: ui.jobArgs.val()
		})

		this.model.save()
	}

});

module.exports = JobView