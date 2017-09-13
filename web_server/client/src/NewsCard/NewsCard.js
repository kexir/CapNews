import React from 'react';
import Auth from '../Auth/Auth';
import { myConfig } from '../../config/config.js';
import './NewsCard.css';

class NewsCard extends React.Component{
    redirectToUrl(url) {
        this.sendClickLog();
        window.open(url, '_blank');
    }

    sendClickLog() {
        // console.log(myConfig.apiUrl);
        let url = myConfig.apiUrl + '/news/userId/' + Auth.getEmail()
            + '/newsId/' + this.props.news.digest;

        let request = new Request(encodeURI(url), {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false});

        fetch(request);
    }

    render() {
        return (
            <div className="news-container" onClick={() => this.redirectToUrl(this.props.news.url)}>
                <div className='row'>
                    <div className='col s12 m12 l4 responsive-img fill'>
                        <img src={this.props.news.urlToImage} alt='NewsCard'/>
                    </div>
                    <div className="col s12 m12 l8 ">
                        <div className="news-intro-panel">
                            <h4>{this.props.news.title}</h4>
                            <div className="news-description">
                                {this.props.news.description}
                            </div>
                            <div>
                                {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                                {this.props.news.time != null && <div className='chip amber news-chip'>{this.props.news.time}</div>}
                                {this.props.news.class != null && <div className='chip amber news-chip'>{this.props.news.class}</div>}
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        )
    };
}

export default NewsCard;