var jayson = require('jayson');

const yaml = require('js-yaml');
const fs = require('fs');
let config = {};
try {
    config = yaml.safeLoad(fs.readFileSync('../../config.yml', 'utf8'));
} catch (e) {
    console.log(e);
}
var rpcConfig = config.default.web_server.RpcServerConfig;
var client = jayson.client.http(rpcConfig);

// Get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Log a news click event for a user
function logNewsClickForUser(user_id, news_id) {
    client.request('logNewsClickForUser', [user_id, news_id], function(err, error, response) {
        if (err) throw err;
        console.log(response);
    });
}

function updateUserInterest(user_id, interest) {
    client.request('updateUserInterest', [user_id, interest], function (err, error, response) {
        if (err) throw err;
        console.log(response);
    })
}
module.exports = {
    getNewsSummariesForUser : getNewsSummariesForUser,
    logNewsClickForUser : logNewsClickForUser,
    updateUserInterest : updateUserInterest
};
