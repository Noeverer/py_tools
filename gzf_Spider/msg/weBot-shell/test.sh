curl --location 'http://localhost:3001/webhook/msg/v2?token=X4SEmGI-wbn5' \
--header 'Content-Type: application/json' \
--data '{
    "to": "Ante",
    "data": { "content": "你好👋" }
}'


curl --location 'http://localhost:3001/webhook/msg/v2?token=X4SEmGI-wbn5' \
--header 'Content-Type: application/json' \
--data '{
    "to": "Ante",
    "data": { 
      "type": "fileUrl" , 
      "content": "https://download.samplelib.com/jpeg/sample-clouds-400x300.jpg?$alias=cloud.jpg" 
    }
}'