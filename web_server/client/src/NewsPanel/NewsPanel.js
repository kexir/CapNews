import './NewsPanel.css';
import _ from 'lodash';

import React from 'react';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';
import NewsCard from '../NewsCard/NewsCard';
import { myConfig } from '../../config/config.js';

class NewsPanel extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            news:null,
            pageNum:1,
            totalPages:1,
            loadedAll:false
        };
        this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount() {
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        window.addEventListener('scroll', this.handleScroll);
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            console.log('Loading more news');
            this.loadMoreNews();
        }
    }

    loadMoreNews() {
        if (this.state.loadedAll === true) {
            return;
        }
        // console.log(myConfig.apiUrl);
        let url = myConfig.apiUrl + '/news/userId/' + Auth.getEmail()
            + '/pageNum/' + this.state.pageNum;

        let request = new Request(encodeURI(url), {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false});

        fetch(request)
            .then((res) => res.json())
            .then((news) => {
                if (!news ||  news.length === 0) {
                    this.setState({loadedAll: true});
                }
                this.setState({
                    news: this.state.news? this.state.news.concat(news) : news,
                    pageNum: this.state.pageNum + 1
                });
            });
    }

    renderNews() {
        console.log("render called!");
        let news_list = [];
        let class_list = this.props.filterClass;
        const regex = new RegExp(this.props.filterText, 'i');
        this.state.news.filter(function(news) {
            return (news.title.search(regex) > -1 || news.description.search(regex) > -1);
        }).filter(function (news) {
            if(class_list.length === 0) {
                return (true);
            } else {
                return (class_list.indexOf(news.class.split(' ')[0]) !== -1)
            }
        }).map((news) =>{
            news_list.push(
            <a className='list-group-item' href="#">
                <NewsCard key={news.title} news={news} />
            </a>
            )
        });

        // this.state.news.map((news) => {
        //     if (news.title.toLowerCase().indexOf(this.props.filterText) === -1 &&
        //         news.description.toLowerCase().indexOf(this.props.filterText) === -1) {
        //         return;
        //     }
        //     news_list.push(
        //         <a className='list-group-item' href="#">
        //             <NewsCard key={news.title} news={news} />
        //         </a>);
        // });

        return(
            <div className="container-fluid">
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        );
    }

    render() {
        if (this.state.news) {
            return(
                <div>
                    {this.renderNews()}
                </div>

            );
        } else {
            return(
                <div>
                    <div id='msg-app-loading'>
                        Loading
                    </div>
                </div>
            );
        }
    }
}
NewsPanel.propTypes = {
    filterText: PropTypes.string.isRequired,
    filterClass: PropTypes.array.isRequired,
};
export default NewsPanel;
