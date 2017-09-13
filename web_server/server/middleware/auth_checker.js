/**
 * Created by lyuqi on 4/6/17.
 */
const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
    console.log('auth_checker: req: ' + req.headers);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }
    // bear token
    const token = req.headers.authorization.split(' ')[1];

    console.log('auth_checker: token:' + token);
    // verify
    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) { return res.status(401).end(); }
        //sub store user id
        const email = decoded.sub;
        //check if a user exists
        return User.findById(email,(userErr, user) => {
            if (userErr || ! user) {
                return res.status(401).end();
            }

            return next();
        });
    });
};