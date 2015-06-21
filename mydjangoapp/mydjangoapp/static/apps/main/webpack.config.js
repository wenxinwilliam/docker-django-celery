var path = require("path");
var webpack = require("webpack");

module.exports = {
  entry: ["./app.js"],
  output: {
    path: "../../dist/main/",
    filename: "app.js",
    chunkFilename: "app[id].js"
  },
  module: {
    loaders: [
      // { test: /\.js$/, loader: 'es6-loader' }, // loaders can take parameters as a querystring
      { test: /\.css$/, loader: "style!css" },
      { test: /\.jpe?g$|\.gif$|\.png$|\.svg$|\.woff$|\.ttf$|\.wav$|\.mp3$/, loader: "file-loader" },
      // { test: /\.html$/, loader: "html-loader" },
      { test: /\.html$/, loader: "handlebars-template-loader" },
    ],
  },
  node: {
      fs: "empty" //avoids error messages
  },
  resolve: {
    alias:{
      // 'jquery': 'jquery/jquery',
      // 'handlebars': 'handlebars/dist/handlebars',
      'bootstrap': 'bootstrap/dist/js/bootstrap',
      'routefilter': 'routefilter/dist/backbone.routefilter',

      // 'moment': 'moment/moment',
      // 'bootstrap-daterangepicker': 'bootstrap-daterangepicker',

    },
    modulesDirectories: ['node_modules', '_comm', 'bower_components']
  },

  externals: {
    // require("jquery") is external and available
    //  on the global var jQuery
    "jquery": "jQuery",
    "backbone": "Backbone",
    "backbone.marionette": "Backbone.Marionette",
    "underscore": "_",
    "handlebars": "Handlebars",
  },

  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
      "root.jQuery": "jquery",

      _: 'underscore',
      'Backbone': 'backbone',
      'Backbone.Marionette': 'backbone.marionette',
      // 'Handlebars': 'handlebars',
    })
  ],

  // ?
  // amd: { jQuery: true },

  // watch: true,
  // watchDelay: 500,
  // debug: true,
  // devtool: 'source-map', 
}
