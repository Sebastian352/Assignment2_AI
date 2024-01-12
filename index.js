const express = require('express');
const { Socket } = require('socket.io');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const path = require('path')

const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

require("./game.sockets.js")(io);


app.get("/", (req, res)=>{
  res.render('home.ejs');
})


server.listen(port, function() {
  console.log("\x1b[41m",`Server is listening on ${port}!`,'\x1b[0m',)
})