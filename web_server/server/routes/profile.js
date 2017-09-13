var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

/* POST news click event. */
router.post('/userId/:id', function(req,res, next) {
    console.log('post interest...');
    user_id = req.params['id'];
    interest = req.body;
    console.log(user_id);
    console.log(interest);
    rpc_client.updateUserInterest(user_id, interest);
    res.send("success");
});

module.exports = router;
