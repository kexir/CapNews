class Auth {
    /**
     * Authenticate a user
     * save token, email in local storage
     * @param token
     * @param email
     */
    static authenticateUser(token, email) {
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }

    /**
     * check if token is aved in local storage
     * check if user is authenticated
     */
    static isUserAuthenticated() {
        return localStorage.getItem('token') !== null;
    }

    /**
     * remove token email from local storage
     */
    static deauthenticateUser() {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }

    /**
     * return token string
     */
    static getToken() {
        return localStorage.getItem('token');
    }

    /**
     * return user email
     */
    static getEmail() {
        return localStorage.getItem('email');
    }
}

export default Auth;
