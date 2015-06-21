var Job = require('./job.model.js');

var Jobs = Backbone.PageableCollection.extend({

	model: Job,

	initialize: function(options) {
	},

	url: "/api/jobs/",

	parseRecords: function(response){
		return response.results
	},

	parseState: function(response, queryParams, state){
		return {totalRecords: response.count}
	},

	state: {
		// You can use 0-based or 1-based indices, the default is 1-based.
		// You can set to 0-based by setting ``firstPage`` to 0.
		firstPage: 1,
		pageSize: 10,
	},

	// You can configure the mapping from a `Backbone.PageableCollection#state`
	// key to the query string parameters accepted by your server API.
	queryParams: {

		// `Backbone.PageableCollection#queryParams` converts to ruby's
		// will_paginate keys by default.
		currentPage: "page_num",
		pageSize: "page_size",
	}
	
})

module.exports = Jobs