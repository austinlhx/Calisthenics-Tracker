var express = require('express');
var cors = require('cors');
const process = require('process');
var cookieParser = require('cookie-parser');

var app = express();
app.use(express.static('.'))
      .use(cors())
      .use(cookieParser())
      .use(express.json());

var port = process.env.PORT || 8888;
app.listen(port);
console.log(`Listening on port: ${port}`);