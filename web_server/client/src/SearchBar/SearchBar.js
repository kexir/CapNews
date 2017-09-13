/**
 * Created by lyuqi on 5/19/17.
 */
import React from 'react';
import PropTypes from 'prop-types';

class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.handleFilterTextInputChange = this.handleFilterTextInputChange.bind(this);
    }

    handleFilterTextInputChange(e) {
        this.props.onFilterTextInput(e.target.value);
    }

    render(){
        return(
            <div className="search-bar">
                <input
                    type="text"
                    placeholder="Search..."
                    value={this.props.filterText}
                    onChange={this.handleFilterTextInputChange}
                />
            </div>

        )
    }
}

SearchBar.propTypes = {
    onFilterTextInput: PropTypes.func.isRequired,
    filterText: PropTypes.string.isRequired,
};

export default SearchBar
