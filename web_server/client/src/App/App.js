import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

import React from 'react';
import logo from '../../public/logo.png';
import './App.css';

import FilterablePanel from '../FilterablePanel/FilterablePanel';

class App extends React.Component{
    render() {
        return(
            <div>
                <center>
                    <img className='logo' src={logo} alt='logo'/>
                </center>
                <div className='container'>
                    <FilterablePanel />
                </div>
            </div>
        );
    }
}

export default App;
