Location processing api built with event driven framewrok using fastAPI , Rabbitmq and Docker. 


## Build docker images of all  the services

```
docker build -t main_api .
docker build -t process_dist .
docker build -t db_service .
```

## Create a network to be used by all the containers

```
docker network create <network-name>
```

## Run the rabbitmq container first inside the network

```
docker run -d --hostname rabbitmq --name rabbitmq --network <network-name> -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
## Run all the containers inside the network

```
docker run -d --name main_api_container --network <network-name> -p 8000:8000 main_api

docker run -d --name process_dist_container --network <network-name> -p 8201:8201 process_dist

docker run -d --name db_service_container --network <network-name> -p 8205:8205 db_service
```


# Testing

## Send a post request through postman 

api-endpoint: http://localhost:8000/send

```
Body:
{
  "lat": 28.7,
  "long": 77.30,
  "email": "abc@gmail.com"
}
```
