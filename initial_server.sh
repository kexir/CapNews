cd backend_server
python service.py & 

cd ../news_recommendation_service
python recommendation_service.py & 

cd ../news_topic_modeling_service/server
python server.py & 

echo "=================================================="
