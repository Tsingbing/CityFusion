var express = require("express");

//body 解析器
var bodyParser = require("body-parser");
//rabbitmq
// var amqp = require('amqp');
var amqp = require('amqplib/callback_api');
var http = require("http");
var app = express();
var path = require('path');


app.use(function(req, res,next){
	//console.log("%s %s", req.method, req.url);
	next();
});

app.use(express.static( __dirname+'/'));

//body 解析器
app.use(bodyParser.urlencoded({extended: true}));

app.get("/about", function(request, response) {
  response.end("Welcome to the about page!");
});

amqp.connect('amqp://localhost', function(err, conn) {
  conn.createChannel(function(err, ch) {
    var ex = 'messages_exchange';
    var args = process.argv.slice(2);
    // var msg = args.slice(1).join(' ') || 'Hello World!';
    // var severity = (args.length > 0) ? args[0] : 'info';
		var msg = 'Hello World!';
    var severity = 'messages_key';
		ch.assertExchange(ex, 'direct', {durable: false});

		//接收web页面的信息
		app.post('/api/orders', function(req,res) {
			var data = req.body;
			//var data = JSON.stringify(req.body);
			console.log(data.name +"   "+ data.drink);
			//
			// ch.publish(ex, severity, new Buffer(msg));
			ch.publish(ex, severity, new Buffer(data.name));
			res.send("yes");
		});
		console.log(" [x] Sent %s: '%s'", severity, msg);
  });

  //setTimeout(function() { conn.close(); process.exit(0) }, 500);
});

app.get("*", function(request, response) {
  response.end("404!");
});

http.createServer(app).listen(1337);
