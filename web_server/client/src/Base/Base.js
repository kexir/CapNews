import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';
import Auth from '../Auth/Auth';
// Base component: Base
// children is a function: represent Login page or Sign up page
const Base = ({ children }) => (
    <div>
        <nav className="nav-bar grey-text text-lighten-4">
            <div className="nav-wrapper">
                <a href="/" className="brand-logo left">&nbsp;&nbsp;Tap News</a>
                <ul id="nav-mobile" className="right">
                    {Auth.isUserAuthenticated() ?
                        (<div>
                            <li>{Auth.getEmail()}</li>
                            <li><Link to="/profile">Profile</Link ></li>
                            <li><Link to="/chart">Chart</Link ></li>
                            <li><Link to="/logout">Log out</Link ></li>
                        </div>)
                        :
                        (<div>
                            <li><Link to="/login">Log in</Link ></li>
                            <li><Link to="/signup">Sign up</Link ></li>
                        </div>)
                    }
                </ul>
            </div>
        </nav>
        <br/>
        {children}
        <footer className="page-footer">
            <div className="container">
                <div className="row">
                    <div className="col l6 s12">
                        <h5 className="white-text">Footer Content</h5>
                        <p className="grey-text text-lighten-4">You can use rows and columns here to organize your footer content.</p>
                    </div>
                    <div className="col l4 offset-l2 s12">
                        <h5 className="white-text">Links</h5>
                        <ul>
                            <li><a className="grey-text text-lighten-3" href="#!">Link 1</a></li>
                            <li><a className="grey-text text-lighten-3" href="#!">Link 2</a></li>
                            <li><a className="grey-text text-lighten-3" href="#!">Link 3</a></li>
                            <li><a className="grey-text text-lighten-3" href="#!">Link 4</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div className="footer-copyright">
                <div className="container">
                    © 2014 Copyright Text
                    <a className="grey-text text-lighten-4 right" href="#!">More Links</a>
                </div>
            </div>
        </footer>
    </div>
);

Base.propTypes = {
    children: PropTypes.object.isRequired
};

export default Base;

