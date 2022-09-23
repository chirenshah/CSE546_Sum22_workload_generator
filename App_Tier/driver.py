import boto3
import json
import datetime
import os
import base64
from image_classification import classification

with open("aws_config.json") as config_file:
        config = json.load(config_file)
session = boto3.Session(
        aws_access_key_id= config["accessKey"],
        aws_secret_access_key= config["secretKey"]
    )

sqs = session.client('sqs', config["awsRegion"])
s3 = session.client('s3')

while True:
    try:
        response = sqs.receive_message(
            QueueUrl=config["inputQueue"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )
    except sqs.exceptions.QueueDoesNotExist:
        timer_start_time = datetime.datetime.now()
        number_of_requests_processed = 0
        print("error")
        continue

    try:
        messages = response["Messages"]
        print(messages)
    except:
        print("No messages in the queue")
        print(input("Press a Key"))
        continue

    for message in messages:
        receipt = message["ReceiptHandle"]
        body = json.loads(message["Body"])
        image_store_filename = body["filename"]
        image_bytes = bytes(body["result"], 'utf-8')
        image_base64 = base64.decodebytes(image_bytes)

        # create an image write the base64 encoded from received message
        image_file_full_path = f"./{config['input']}/{image_store_filename}"
        os.mkdir(config['input']) if not os.path.isdir(config['input']) else None
        image_file = open(image_file_full_path, 'wb')
        image_file.write(image_base64)
        image_file.close()
        s3.upload_file(image_file_full_path, config["inputBucket"],image_file)
        try:
            input,output = classification(image_file_full_path)
        except:
            pass
        message = dict({
                'filename': input,
                'result': output, 
                'timestamp': datetime.datetime.now().isoformat()
                })
        r = sqs.send_message(
            QueueUrl=config["outputQueue"],
            DelaySeconds=5,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'Results S3 Info'
                }
            },
            MessageBody=json.dumps(message)
        )
        sqs.delete_message(
                    QueueUrl=config["inputQueue"],
                    ReceiptHandle=receipt
        )
        s3.upload_file(image_store_filename,config["outputBucket"],output)
        
    