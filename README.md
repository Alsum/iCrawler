# iCrawler

This project includes
Basic setup for Scrapyd + Django , scrap website data and then save cleaned data to Mongo


## Setup
1 - Install requirements
````
$ pip install -r requirements.txt
````
2 - Configure the database
````
$ python manage.py migrate
````
## Start the project
In order to start this project you will need to have running Django and Scrapyd at the same time.

In order to run Django
````
$ python manage.py runserver
````
In order to run Scrapyd
````
$ cd scrapy_app
$ scrapyd
````

At this point you will be able to send job request to Scrapyd.
````
curl -d "url=https://www.jumia.com.eg/laptops/" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:8000/api/crawl/
````

The crawled data will be automatically be saved in the MongoDB

