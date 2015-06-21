require('routefilter');
require('jquery-extensions/jquery.deparam.js');

var app = require('./app');

var Router = Backbone.Marionette.AppRouter.extend({
    appRoutes: {
      "": "showJobList",

      "jobs": "showJobList",

    },
    /* standard routes can be mixed with appRoutes/Controllers above */
    routes: {

    },

    before: function(route, params){
      // console.log(params)
      var qs = params[0] != null ? $.deparam(params[0]) : {};
      this.query_params = qs;
    },

    onRoute: function(name, path, params){
      // console.log('on route: %o', name)
    	
      this.path = path;
      // console.log('params=%o', this.query_params);
    	app.vent.trigger('route:changed', name, path, params);
    }

});

module.exports = Router;