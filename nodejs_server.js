// we use express and multer libraries to send images
const express = require('express');
const multer = require('multer');
var AWS = require('aws-sdk');
const server = express();
const PORT = 3000;

// uploaded images are saved in the folder "/upload_images"
const upload = multer({dest: __dirname + '/upload_images'});

server.use(express.static('public'));

// "myfile" is the key of the http payload
server.post('/', upload.single('myfile'), function(request, respond) {
  if(request.file) console.log(request.file);
  // save the image
  var fs = require('fs');
  fs.rename(__dirname + '/upload_images/' + request.file.filename, __dirname + '/upload_images/' + request.file.originalname, function(err) {
    if ( err ) console.log('ERROR: ' + err);
  });

  respond.end(request.file.originalname + ' uploaded!');
});

server.get('/info',function(request,respond){
  let s3 = new AWS.S3({apiVersion: '2020-03-01'});
  
  // Call S3 to list the buckets
  s3.listBuckets(function(err, data) {
    if (err) {
      console.log("Error", err);
    } else {
      respond.send(data.Buckets);
    }
  });
})

// You need to configure node.js to listen on 0.0.0.0 so it will be able to accept connections on all the IPs of your machine
const hostname = '0.0.0.0';
server.listen(PORT, hostname, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
  });
