
var tpl = require('../templates/jobs.layout.tpl.html');

var JobItemView = require('../views/job.itemview.js');
var JobsCollectionView = require('../views/jobs.collectionview.js');

var JobsLayoutView = Backbone.Marionette.LayoutView.extend({
	template: tpl,

	regions: {
		job: "#add-job",
		jobList: "#job-list"
	},

	onRender: function(){
		this.getRegion('job').show(
			new JobItemView(
				// {
				// 	template: require('../templates/job.tpl.html'), 
				// 	model: new require('../models/job.model.js')(),
				// }
			)
		);
		this.getRegion('jobList').show(new JobsCollectionView());
	}
});

module.exports = JobsLayoutView