var Handlebars = require('handlebars-template-loader').Handlebars;

Handlebars.registerHelper("x", function (expression, options) {
  var fn = function(){}, result;

  // in a try block in case the expression have invalid javascript
  try {
    // create a new function using Function.apply, notice the capital F in Function
    fn = Function.apply(
      this,
      [
        'window', // or add more '_this, window, a, b' you can add more params if you have references for them when you call fn(window, a, b, c);
        'return ' + expression + ';' // edit that if you know what you're doing
      ]
    );
  } catch (e) {
    console.warn('[warning] {{x ' + expression + '}} is invalid javascript', e);
  }

  // then let's execute this new function, and pass it window, like we promised
  // so you can actually use window in your expression
  // i.e expression ==> 'window.config.userLimit + 10 - 5 + 2 - user.count' //
  // or whatever
  try {
    // if you have created the function with more params
    // that would like fn(window, a, b, c)
    result = fn.bind(this)(window);
  } catch (e) {
    console.warn('[warning] {{x ' + expression + '}} runtime error', e);
  }
  // return the output of that result, or undefined if some error occured
  return result;
});