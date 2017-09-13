import React from 'react';
import Auth from '../Auth/Auth';
import './ProfilePage.css';

class Profile extends React.Component{
    constructor() {
        super();
        this.state = {
            interest: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.updatePreference = this.updatePreference.bind(this);
    }
    handleChange(e){
        if(e.target.checked === true){
            this.setState({
                interest: this.state.interest.concat(e.target.id)
            });
        }
        if (e.target.checked === false){
            console.log(e.target.id);
            let interest_class = this.state.interest.filter(function(interest) {
                return (interest !== e.target.id);
            });
            console.log(interest_class);
            this.setState({
                interest: interest_class
            });
        }
    }
    updatePreference() {
        if(this.state.interest.length === 0) {
            console.log("here");
            return ;
        }
        let url = 'http://localhost:3000/profile/userId/' + Auth.getEmail();
        let request = new Request(encodeURI(url),{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.state.interest),
            cache: false
        });
        fetch(request);
    }
    render(){
        return (
            <div className="container center-align">
                <h4> select your topic </h4>
                <form className="" onClick={this.handleChange}>
                    <p>
                        <input type="checkbox" className="filled-in" id="Colleges" />
                        <label htmlFor="Colleges">Colleges & Schools</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Environmental" />
                        <label htmlFor="Environmental">Environmental</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="World" />
                        <label htmlFor="World">World</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Entertainment" />
                        <label htmlFor="Entertainment">Entertainment</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Media" />
                        <label htmlFor="Media">Media</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Politics" />
                        <label htmlFor="Politics">Politics & Government</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Regional" />
                        <label htmlFor="Regional">Regional News</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Religion" />
                        <label htmlFor="Religion">Religion</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Sports" />
                        <label htmlFor="Sports">Sports</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Technology" />
                        <label htmlFor="Technology">Technology</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Traffic" />
                        <label htmlFor="Traffic">Traffic</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Weather" />
                        <label htmlFor="Weather">Weather</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Economic" />
                        <label htmlFor="Economic">Economic & Corp</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Advertisements" />
                        <label htmlFor="Advertisements">Advertisements</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Crime" />
                        <label htmlFor="Crime">Crime</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Magazine" />
                        <label htmlFor="Magazine">Magazine</label>
                    </p>
                    <p>
                        <input type="checkbox" className="filled-in" id="Other" />
                        <label htmlFor="Other">Other</label>
                    </p>
                </form>
                <button className="btn waves-effect waves-light submit_button" type="submit" name="action" onClick={this.updatePreference}>
                    Submit <i className="material-icons right">send</i>
                </button>
            </div>
        );
    }
}


export default Profile;