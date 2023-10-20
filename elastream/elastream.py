from elasticsearch import Elasticsearch, helpers
import psycopg2
import json
import time
from datetime import datetime, timedelta

es = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
)

conn = psycopg2.connect(
    dbname="your_db_name",
    user="your_db_user",
    password="your_password",
    host="localhost"
)
cur = conn.cursor()

table_creation_query = """
CREATE TABLE IF NOT EXISTS elasticsearch_data (
    id SERIAL PRIMARY KEY,
    data JSONB,
    timestamp TIMESTAMP
)
"""
cur.execute(table_creation_query)
conn.commit()

# Insert data into PostgreSQL
insert_query = """
INSERT INTO elasticsearch_data (data, timestamp) VALUES (%s, %s)
"""

# Function to fetch and insert data
def fetch_and_insert(new_data_start_date):
    query = {
        "query": {
            "range": {
                "date": {
                    "gte": new_data_start_date.isoformat(),
                    "lt": datetime.now().isoformat()
                }
            }
        },
        "sort": [
            {"date": "asc"}
        ]
    }

    results = helpers.scan(
        es,
        query=query,
        scroll='5m',
        index='your_index',
        _source=True
    )

    count = 0
    for result in results:
        document = result['_source']
        cur.execute(insert_query, (json.dumps(document), result['_source']['date']))
        count += 1

    conn.commit()
    return count

last_fetch_time = datetime.now()
interval_seconds = 3600  # checks every hour

try:
    while True:
        new_data_count = fetch_and_insert(last_fetch_time)

        print(f"Fetched {new_data_count} new results since {last_fetch_time.isoformat()}")

        # update the last fetch time
        last_fetch_time = datetime.now()

        # sleep until the next interval
        time.sleep(interval_seconds)

except Exception as e:
    print(str(e))

finally:
    cur.close()
    conn.close()
