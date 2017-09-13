import Base from './Base/Base';
import App from './App/App';
import LoginPage from './Login/LoginPage';
import SignUpPage from './SignUp/SignUpPage';
import Chart from './Chart/chart';
import Profile from './Profile/ProfilePage';
import Auth from './Auth/Auth';


const routes = {
    // base component (wrapper for the whole application).
    component: Base,
    // put component in children  in Base, React protocol
    childRoutes: [

        {
            path: '/',
            getComponent: (location, callback) => {
                if (Auth.isUserAuthenticated()) {
                    callback(null, App);
                } else {
                    callback(null, LoginPage);
                }
            }
        },

        {
            path: '/login',
            component: LoginPage
        },

        {
            path: '/signup',
            component: SignUpPage
        },

        {
            path: '/logout',
            onEnter: (nextState, replace) => {
                Auth.deauthenticateUser();
                // change the current URL to /
                replace('/');
            }
        },
        {
            path: '/chart',
            component: Chart
        },
        {
            path: '/profile',
            component: Profile
        }
    ]
};

export default routes;
