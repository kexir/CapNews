/**
 * Created by lyuqi on 5/19/17.
 */
import React from 'react';
import SearchBar from '../SearchBar/SearchBar';
import NewsClass from '../NewsClass/NewsClass';
import NewsPanel from '../NewsPanel/NewsPanel';

class FilterablePanel extends React.Component{
    constructor() {
        super();
        this.state = {
            filterText: '',
            filterClass: []
        };
        this.handleFilterTextInput = this.handleFilterTextInput.bind(this);
        this.handleAddFilterClassInput = this.handleAddFilterClassInput.bind(this);
        this.handleDeleteFilterClassInput = this.handleDeleteFilterClassInput.bind(this);
    }

    handleFilterTextInput(filterText){
        this.setState({
            filterText: filterText
        });
    };

    handleAddFilterClassInput(addClass){
        this.setState({
            filterClass: this.state.filterClass.concat(addClass)
        });
    }

    handleDeleteFilterClassInput(deleteClass){
        let news_class = this.state.filterClass.filter(function(news_class) {
            return (news_class !== deleteClass);
        });
        console.log(news_class);
        this.setState({
            filterClass: news_class
        });
    }
    render(){
        return(
            <div className="row">
                <div className="col s4">
                    <SearchBar
                        filterText={this.state.filterText}
                        onFilterTextInput={this.handleFilterTextInput}
                    />
                    <NewsClass
                        onAddFilterClassInput={this.handleAddFilterClassInput}
                        onDeleteFilterClassInput={this.handleDeleteFilterClassInput}
                    />
                </div>
                <div className="col s8">
                    <NewsPanel
                        filterText={this.state.filterText}
                        filterClass={this.state.filterClass}
                    />
                </div>
            </div>
        )
    }
}

export default FilterablePanel;