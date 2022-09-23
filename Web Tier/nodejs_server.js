// we use express and multer libraries to send images
const express = require("express");
const multer = require("multer");
var AWS = require("aws-sdk");
const { response } = require("express");
const server = express();
const PORT = 3000;
var fs = require('fs');
// uploaded images are saved in the folder "/upload_images"
const upload = multer({ dest: __dirname + "/upload_images" });
server.use(express.static("public"));

const config = JSON.parse(fs.readFileSync('config.json'));
// "myfile" is the key of the http payload
server.post("/", upload.single("myfile"), function (request, respond) {
  if (request.file) console.log(request.file);
  AWS.config.update({ region: "us-east-1" });
  var fs = require("fs");
  const SQS = new AWS.SQS({ apiVersion: "2020-03-01" });
  fs.rename(
    __dirname + "/upload_images/" + request.file.filename,
    __dirname + "/upload_images/" + request.file.originalname,
    () => {
      const contents = fs.readFileSync(
        __dirname + "/upload_images/" + request.file.originalname,
        { encoding: "base64" }
      );
      const params = {
        QueueUrl: config.inputQueue,
        MessageBody: JSON.stringify({
          filename: request.file.originalname,
          result: contents,
          date: new Date().toISOString(),
        }),
      };
      SQS.sendMessage(params, (err, result) => {
        if (err) {
          console.log(err);
        }
        console.log(result);
      });
    }
  );

  const replyListener = () => {
    var params = {
      AttributeNames: [
         "SentTimestamp"
      ],
      MaxNumberOfMessages: 10,
      MessageAttributeNames: [
         "All"
      ],
      QueueUrl: config.outputQueue,
      VisibilityTimeout: 20,
      WaitTimeSeconds: 0
     };
    SQS.receiveMessage(
      params,
      (err, data) => {
        if (err) {
          console.log("Receive Error");
          console.log(err)
        }
        if (data.Messages) {
          respond.end("Received Messages Count: " + data.Messages.length);
          data.Messages.forEach((msg) => {
            SQS.deleteMessage(
              {
                QueueUrl: config.outputBucket,
                ReceiptHandle: msg.ReceiptHandle,
              },
              (err) => {
                if (err) {
                  console.log("Delete Error");
                  console.log(err)
                }
              }
            );
          });
        }
      }
    );
  };

  setInterval(replyListener,1000);

  // uploadParams = {Bucket:"cloudcomputinginputbucket",Body:"",Key:""}
  // uploadParams.Body = filestream
  // uploadParams.Key = request.file.originalname
  // s3.upload(uploadParams,function(err, data) {
  //     if (err) {
  //       console.log("Error", err);

  //     } else {
  //       respond.send(data);
  //     }
  //   });
  // respond.send("hello")
  // Call S3 to list the buckets
  //
  // save the image
});

// You need to configure node.js to listen on 0.0.0.0 so it will be able to accept connections on all the IPs of your machine
const hostname = "0.0.0.0";
server.listen(PORT, hostname, () => {
  console.log(`Server running at http://${hostname}:${PORT}/`);
});
