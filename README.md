# Netguru recruitment task

Application for fetching and storing cars data from https://vpic.nhtsa.dot.gov/api/

There are 4 main endpoints:

```GET /api/v1/cars``` to retrieve list of all cars already present in application database with their current average rate

```GET /api/v1/cars/popular``` to retrieve top cars already present in the database ranking based on number of rates 

```POST /api/v1//cars/{id}/rate``` with body 
```
{ 
    "rating" : 1 
}
```
To add a rate for a car from 1 to 5

```POST /api/v1/cars``` with body 
```
{
    "make": "Mercedes",
    "name": "S-Class"
} 
```

# Building

```sh
$ git clone https://github.com/senkuqq/netguru_recruitment_task.git
$ cd netguru_recruitment_task
$ docker build -t web:latest .
```

# Running the application
Run docker image.
```sh
$ docker run -d --name app -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

To ensure everything is running properly run.

```sh
$ docker exec -it app python manage.py test
```
Create superuser.
```sh
$ docker exec -it app python manage.py createsuperuser
```


# Online
You can check online version on [heroku](http://netguru-recruitment-task.herokuapp.com/).

There is file netguru.postman_collection.json which You can import to Postman and try endpoints by yourself! 

# Comments
* I decided to change a little bit location of endpoints to make it more predictable
