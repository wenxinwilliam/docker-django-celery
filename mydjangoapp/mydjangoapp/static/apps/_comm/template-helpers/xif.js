require('./x');

var Handlebars = require('handlebars-template-loader').Handlebars;

Handlebars.registerHelper("xif", function (expression, options) {
    return Handlebars.helpers["x"].apply(this, [expression, options]) ? options.fn(this) : options.inverse(this);
});