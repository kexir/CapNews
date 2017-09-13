import operator
from datetime import datetime,timedelta

class DataService(object):
    @classmethod
    def init(cls,client):
        cls.client = client
        cls.db = client['tap-news']
        cls.news = cls.db.news
        cls.user_preference_model = cls.db.user_preference_model
        cls.click_logs = cls.db.click_logs

    # return a dict {user_id, click_history}
    # timestamp of click history must be today
    @classmethod
    def retrieve_user_click_history(cls, user_id):
        result = {}
        cursor = cls.click_logs.find({"userId":user_id})
        if cursor is None:
            return []

        for click_log in cursor:
            if abs(click_log["timestamp"]-datetime.utcnow()) < timedelta(days=1):
                if result.get('userId') is None:
                    result['userId'] = user_id
                    click_list = list([click_log['newsId']])
                else:
                    click_list = result.get('click_list')
                    click_list.append(click_log['newsId'])
                result['click_list'] = click_list

        return result

    # return a top 5 preference_list
    @classmethod
    def retrieve_preference_list(cls,user_id):
        model = cls.user_preference_model.find_one({'userId':user_id})
        if model is None:
            return []

        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        # print sorted_tuples
        sorted_list = [sorted_tuples[0][0],sorted_tuples[1][0],sorted_tuples[2][0],sorted_tuples[3][0],sorted_tuples[4][0]]
        return sorted_list

    @classmethod
    def retrieve_news_class(cls,news_id):
        cursor = cls.news.find_one({'digest': news_id})
        if cursor is None or 'class' not in cursor:
            return []
        return cursor['class']

    @classmethod
    def retrieve_all_user_news_rate(cls):
        cursor = cls.click_logs.find({})
        result = []
        for click_log in cursor:
            preference_list = DataService.retrieve_preference_list(click_log["userId"])
            news_class = DataService.retrieve_news_class(click_log["newsId"])
            try:
                index_element = preference_list.index(news_class)
            except ValueError:
                click_log.update({"rate": 0})
            else:
                click_log.update({"rate": 5-index_element})
            result.append(click_log)
        return result