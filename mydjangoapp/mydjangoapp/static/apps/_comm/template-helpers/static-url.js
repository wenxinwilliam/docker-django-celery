var Handlebars = require('handlebars-template-loader').Handlebars;

Handlebars.registerHelper('STATIC_URL', function(x) {    
    return window.STATIC_URL;
});