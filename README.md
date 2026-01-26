# Ray serve with FastAPI, UV and Feast

It is a simple example working with Ray serve.
The [postman collection](Ray%20Serv%20Example.postman_collection.json) of request to Ray Serve.

Start all:
`make start_compose`

1. Feast UI: http://localhost:8888
2. Ray Serve app: http://localhost:8000
3. Ray clustar status: http://localhost:8265  

In feast pod use command for checking data:
```
feast get-online-features \
  --features "player_features:avg_deposit" \
  --entities player_id=1
```

Check app:
```
curl --location 'http://0.0.0.0:8000/predict' \                    
--header 'Content-Type: application/json' \
--data '{                                               
    "entity_id": 123
}'                                                       
```