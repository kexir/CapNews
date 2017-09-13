const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
// var Promise = require('mpromise');
// var assert = require('assert');

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
    console.log("you are in signup_passport.js");
    const newUser = new User (userData);
    newUser.save((err) => {
        console.log('Save new user!');
        if (err) {
            console.log('Save error');
            return done(err);
        }

        return done(null);
    });
    // var promise = newUser.save();
    // console.log("you are in signup_passport.js");
    // assert.ok(promise instanceof Promise);
    // console.log("you are in signup_passport.js");
    // promise.then((err) => {
    //     console.log('Save new user!');
    //     if (err) {
    //         console.log('Save error');
    //         promise.reject(err);
    //         return done(err);
    //     }
    //
    //     return done(null);
    // });
});