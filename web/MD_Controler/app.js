var express = require("express");

//body 解析器
var bodyParser = require("body-parser");

var http = require("http");
var app = express();
var path = require('path');

app.use(function(req, res,next){
	console.log("%s %s", req.method, req.url);
	next();
});

app.use(express.static( __dirname+'/'));

//body 解析器
app.use(bodyParser.urlencoded({extended: true}));

app.get("/about", function(request, response) {
  response.end("Welcome to the about page!");
});

app.post('/api/orders', function(req,res) {
	var data = req.body;
  console.log(data.name +"   "+ data.drink);

	res.send("yes");
});


app.get("*", function(request, response) {
  response.end("404!");
});

http.createServer(app).listen(1337);
