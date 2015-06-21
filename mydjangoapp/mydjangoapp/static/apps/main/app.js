
__webpack_public_path__ = STATIC_URL + 'dist/main/';

var app = new Backbone.Marionette.Application({});

app.addInitializer(function(options) {

    require(['./router', './controller'], function(AppRouter, AppController){

        // create controller
        var controller = new AppController({});
        // initialize the router
        var router = new AppRouter({
          controller: controller
        });

        app.router = router;
        // app.router.path = '';

        Backbone.history.start();
        // Backbone.history.start({pushState: true, root: '/app/stats/reports/'});

        // $(document).on('click', 'a:not([data-bypass])', function (evt) {

        //     var href = $(this).attr('href');
        //     var protocol = this.protocol + '//';

        //     if (href.slice(protocol.length) !== protocol) {
        //         evt.preventDefault();
        //         router.navigate(href, true);
        //     }
        // });

    })
});

app.on("start", function(){
    // Start Backbone history a necessary step for bookmarkable URL's
    // console.log('app started')
});

app.addRegions({
    mcont: '#app'
});

/* start: calls addInitializer() and trigger 'start' event */
app.start({});

module.exports = app;
