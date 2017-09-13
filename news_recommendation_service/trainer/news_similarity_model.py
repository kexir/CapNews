from pymongo import MongoClient
from news_recommendation_service.dataservice import DataService
import math

MONGO_HOST = localhost
MONGO_PORT = 27017

class Helper(object):
    @classmethod
    def cosine_similarity(cls,user_list1, user_list2):
        math_count = cls.__count_match(user_list1, user_list2)
        return float(math_count) / math.sqrt(len(user_list1)*len(user_list2))

    # __count_match is private method
    @classmethod
    def __count_match(cls,list1,list2):
        count = 0
        for element in list1:
            if element in list2:
                count += 1

        return count


def main():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    try:
        DataService.init(client)
        preference_list = DataService.retrieve_preference_list("qlyu044@gmail.com")
        # print Helper.cosine_similarity(preference_list1, preference_list2)
        click_history = DataService.retrieve_user_click_history("qlyu044@gmail.com")
        # print click_history
        # print list(set(click_history1) - set(click_history2))
        user_news_rate = DataService.retrieve_all_user_news_rate()
        print user_news_rate
    except Exception as e:
        print "exceptions: %s" %e
    finally:
        client.close()

if __name__ == "__main__":
    main()
