# elastream

Elastream is a python script that streams data from elasticsearch to postgresql. Released under the MIT license.

## Outline

[elastream/elastream.py](elastream/elastrem.py) fetches data  every hour, as defined by the `interval_seconds` variable. It issues a range query for Elasticsearch to fetch documents with a timestamp greater than the last recorded fetch. 

After fetching the data, the script reports the number of new documents found and inserts them into the PostgreSQL database. 

The last_fetch_time is updated with the current time after each fetch, so subsequent iterations fetch new data.

## Assumptions

* Recent python installed

## Setup

Install packages:

```
pip install elasticsearch psycopg2-binary
```

Configure PostgreSQL:
* [Configure psycopg2](https://www.postgresqltutorial.com/postgresql-python/connect/)

Clone this repo

```
git clone https://github.com/sidprobstein/elastream
```

Modify [elastream/elastream.py](elastream/elastream.py) with the appropriate elasticsearch details:

```
es = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
)
```

And also the PostgreSQL coordinates:

```
conn = psycopg2.connect(
    dbname="your_db_name",
    user="your_db_user",
    password="your_password",
    host="localhost"
)
```

Then, run the script:

```
python elastream/elastream.py
```

Console output should appear like so:

```
Fetched 30 new results since 2023-10-15T14:30:00
Fetched 20 new results since 2023-10-15T15:30:00
...
```

# Notes

* It should be possible to run multiple versions all hitting the same elasticsearch index by adjusting the range query. For example if there are 1,000,000s of records a day, modify the script so you can run one instance of elastream for each day. 

# To do

The script needs:
* Exception handling
* Logging instead of print()

