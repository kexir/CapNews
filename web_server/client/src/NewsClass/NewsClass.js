/**
 * Created by lyuqi on 5/20/17.
 */
import React from 'react';
import PropTypes from 'prop-types';

class NewsClass extends React.Component{
    constructor(props){
        super(props);
        this.handleFilterClassInputChange = this.handleFilterClassInputChange.bind(this);
    }
    handleFilterClassInputChange(e) {
        if(e.target.checked === true){
            this.props.onAddFilterClassInput(e.target.id);
        }
        if (e.target.checked === false){
            this.props.onDeleteFilterClassInput(e.target.id);
        }
    }
    render(){
        return(
            <form onClick={this.handleFilterClassInputChange}>
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
        )
    }
}

NewsClass.propTypes = {
    onAddFilterClassInput: PropTypes.func.isRequired,
    onDeleteFilterClassInput: PropTypes.func.isRequired,
};

export default NewsClass
