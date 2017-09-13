var client = require('./rpc_client');

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('qlyu044@gmail.com', 1, function(response) {
    console.assert(response != null);
});

// invoke "logNewsClickForUser"
client.logNewsClickForUser('qlyu044@gmail.com', 'XHe0M1b3RlpbpU2ttpJgQw==\n');