require('bootstrap');

var app = require('./app');

// var HeaderView = require('./header/view');
// var SidebarView = require('./sidebar/view');
var UserToken = require('./models/ws-token.model.js');

var JobsLayoutView = require('./views/jobs.layoutview.js');

var TempFillerView = Backbone.Marionette.ItemView.extend({
    template: '<div>Coming Soon!</div>',
})

var Controller = Backbone.Marionette.Controller.extend({
    initialize: function(options) {
        app.user = {}
		//TODO: code to initialize
        new UserToken().fetch({
            success: function(model){
                app.user = model.toJSON();
                // app.user.ws_token = model.get('token');
                // console.log(app.user)
                var ws_socket_addr = "ws://" + window.location.hostname + 
                    ":8009" + "/api/ws/" + app.user.id + "/" + app.user.token;

                console.log(ws_socket_addr);
                app.ws_socket = new WebSocket(ws_socket_addr);

                app.ws_socket.onmessage = function(event) {
                    console.log(event.data);
                    var decoded_data = event.data.split(':');
                    var msg = {
                        type: decoded_data[0],
                        id: decoded_data[1],
                        body: decoded_data[2],
                    }
                    if(msg.type == 'job'){
                        alert('job(' + msg.id + ') ' + msg.body);
                        window.location.reload()
                    }
                };

                app.ws_socket.onopen = function (event) {
                    app.ws_socket.send('echo');
                };
            }
        })
    },

    start: function() {
        //TODO: code to start
    },

    showJobList: function(){
        console.log('init')
    	app.mcont.show(new JobsLayoutView());
    },
});

module.exports = Controller;
