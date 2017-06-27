
// var amqp = require('amqplib/callback_api');
//
// amqp.connect('amqp://localhost', function(err, conn) {
//   conn.createChannel(function(err, ch) {
//     var q = 'hello';
//     var msg = 'Hello World!';
//
//     ch.assertQueue(q, {durable: false});
//     // Note: on Node 6 Buffer.from(msg) should be used
//     ch.sendToQueue(q, new Buffer(msg));
//     console.log(" [x] Sent %s", msg);
//   });
//   setTimeout(function() { conn.close(); process.exit(0) }, 500);
// });
var amqp = require('amqplib/callback_api');

var connect , channel;
amqp.connect('amqp://localhost', function(err, conn) {
  connect = conn;
  connect.createChannel(function(err, ch) {
    channel = ch;
    var q = 'hello';
    var msg = 'Hello World!';

    channel.assertQueue(q, {durable: false});
    // Note: on Node 6 Buffer.from(msg) should be used
    channel.sendToQueue(q, new Buffer(msg));
    console.log(" [x] Sent %s", msg);
  });
  //setTimeout(function() { conn.close(); process.exit(0) }, 500);
});

channel.sendToQueue(q, new Buffer(msg));
