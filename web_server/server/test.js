var AWS = require('aws-sdk');

var s3 = new AWS.S3();

var myBucket = 'my.unique.bucket.name';

var myKey = 'myBucketKey';

s3.createBucket({Bucket: myBucket}, function(err, data) {
    if (err) {
        console.log(err);
    } else {
        params = {Bucket: myBucket, Key: myKey, Body: 'Hello!'};
        s3.putObject(params, function(err, data) {
            if (err) {
                console.log(err)
            } else {
                console.log("Successfully uploaded data to myBucket/myKey");
            }
        });
    }
});

// host: process.env.RDS_HOSTNAME,
// user: process.env.RDS_USERNAME,
// password: process.env.RDS_PASSWORD
// port: process.env.RDS_PORT