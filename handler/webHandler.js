let createError = require('http-errors');
let express = require('express');
let cors = require('cors')
let path = require('path');
let cookieParser = require('cookie-parser');
let logger = require('morgan');

let usersRouter = require('../api/userApi');
let devicesRouter = require('../api/deviceApi');
let nodeRouter = require('../api/nodeApi');

let Response = require('../models/responseModel');

let app = express();

// view engine setup
app.set('views', path.join(__dirname, '../views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));

app.use('', cors(), usersRouter);
app.use('', cors(), devicesRouter);
app.use('', cors(), nodeRouter);

app.get('*', function (req, res) {
  var code = 404;
  let response = new Response(code, null, null)
  res.status(code).send(response);
  //return;
})

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  //console.log(req.app.get('env'));

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
