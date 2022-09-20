// we use express and multer libraries to send images
const express = require('express');
const multer = require('multer');
var AWS = require('aws-sdk');
const { response } = require('express');
const server = express();
const PORT = 3000;

// uploaded images are saved in the folder "/upload_images"
const upload = multer({dest: __dirname + '/upload_images'});

server.use(express.static('public'));

// "myfile" is the key of the http payload
server.post('/', upload.single('myfile'), function(request, respond) {
  if(request.file) console.log(request.file);
  let s3 = new AWS.S3({apiVersion: '2020-03-01'});
  var fs = require('fs');
  fs.rename(__dirname + '/upload_images/' + request.file.filename, __dirname + '/upload_images/' + request.file.originalname, function(err) {
    if ( err ) console.log('ERROR: ' + err);
  });
  let filestream = fs.createReadStream(__dirname + '/upload_images/' + request.file.originalname);
  AWS.config.update({region: 'us-east-1'})
  const SQS = new AWS.SQS({apiVersion: '2020-03-01'})
  queue_url = "https://sqs.us-east-1.amazonaws.com/432013769693/my_SQS_Queue"
    const params = {
      QueueUrl: queue_url,
      MessageBody: JSON.stringify({
        'filename':request.file.originalname, 
        'result':filestream
      })
    }
    SQS.sendMessage(params, (err, result) => {
      if (err) {
        console.log(err)
      }
      console.log(result)
    })
  uploadParams = {Bucket:"cloudcomputinginputbucket",Body:"",Key:""}
  uploadParams.Body = filestream
  uploadParams.Key = request.file.originalname
  s3.upload(uploadParams,function(err, data) {
      if (err) {
        console.log("Error", err);

      } else {
        respond.send(data);
      }
    });
  respond.send("hello")
  // Call S3 to list the buckets
  // 
  // save the image
  
  // respond.end(request.file.originalname + ' uploaded!');
});


// You need to configure node.js to listen on 0.0.0.0 so it will be able to accept connections on all the IPs of your machine
const hostname = '0.0.0.0';
server.listen(PORT, hostname, () => {
    console.log(`Server running at http://${hostname}:${PORT}/`);
  });




