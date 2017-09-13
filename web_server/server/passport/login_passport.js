/**
 * Created by lyuqi on 4/9/17.
 */
const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password.trim()
    };

    return User.findOne ({email: userData.email}, (err, user) => {
         if (err) { return done(err); }

         if (!user) {
             const error = new Error('Incorrect email or password');
             error.name = 'IncorrectCredentialError';

             return done(error);
         }

         return user.comparePassword(userData.password, (passwordErr, isMatch) => {
             if (err) { return done(err); }

             if (!isMatch) {
                 const error = new Error('Incorrect email or password');
                 error.name = 'IncorrectCredentialError';

                 return done(error);
             }

             const payload = {
                 sub: user.id
             };
             //TODO: change jwt secrete, this may be a bug
             const token = jwt.sign(payload,config.jwtSecret);

             const data = {
                 name: user.email
             };

             return done(null,token,data);
         })
    })
});