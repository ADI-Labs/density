
# Wireless Density API

CUIT has graciously worked with ESC & ADI to provide snapshots of the number of connections in various locations on campus.
The plan is to provide this data through a restful HTTP API as well as provide client libraries for easy consumption.

## Data

We receive a digest of data every 15 minutes.
The dataset is given in a JSON that is very simple.
Each endpoint group has an ID that is the key.
The value consists of the `name`, `client_count` and `parent_id`.
Groups in the same building share the same `parent_id`.

```js
// Example data from 9/21 @ 8 PM:
{
  "152" : {
    "name" : "Lerner 3",
    "client_count" : 70,
    "parent_id" : 84
  },
  "131" : {
    "name" : "Butler Library 3",
    "client_count" : 328,
    "parent_id" : 103
  },
  "155" : {
    "name" : "JJ's Place",
    "client_count" : 90,
    "parent_id" : 75
  },
  "130" : {
    "name" : "Butler Library 2",
    "client_count" : 412,
    "parent_id" : 103
  }
}
```






## Updating Data

A separate daemon process should watch for new files to be added to the server.
Upon receiving a new digest it should be processed and inserted to the database.
The updates should be logged.
The details of this implementation are very flexible.



# API

In the proposed endpoints:

- `group` refers to a group of endpoints i.e. "Lerner 3".
  - this is specified using the ID number.
- `building` refers to the aggregate of group of endpoints with the same parent_id i.e. 103 for Butler
  - this is specified using the ID number.
- `time_window` refers to a time window
  - options: [ hour , day , week , month ]


All endpoints involving a time delimiter will include total, average, minimum and maximum values as well as the start time for each window.
The average/minimum/maximum will be calculated from the 15 minute windows.


All data from ranges wil be returned from newest to oldest data.



### Response Format:





#### Individual Queries


```
{
  "time": "2014-02-28T15:15:00",
  "group_id": "butler-3",
  "count": 58
}
```


#### Ranged Queries

Keys:

- `next_start_time`: The value to use in the next query's parameter of `start_time`
- `< ID >`: (`groupID` or `buildingID`) refers to the group or building that is being queried.
- `count`: the number of results in the array
- `results`: holds the list of results


```
{
  "next_start_time: "2014-02-28"
  "< ID >": "butler-3",
  "count": 100,
  "results": [
    {
      "start_time": "2014-03-28",
      "average": 10,
      "minimum": 0,
      "maximum": 100
    },
    {
      "start_time": "2014-03-27",
      "average": 10,
      "minimum": 0,
      "maximum": 100
    },
    ....
  ]
}
```


### Endpoints:

latest data

- `/latest`
  - latest dump of data for all endpoints
- `/latest/group/< group >`
  - latest dump of data for the specified group
- `/latest/building/< building >`
  - latest dump of data for the specified building


data from exact window

- `/day/< day >/group/< group >`
  - specify syntax for a day, get all info for that day
- `/day/< day >/building/< building >`
  - specify syntax for a day, get all info for that building


range

- `/range/< start_time >/< start_time >/group/< group >`
- `/range/< start_time >/< start_time >/building/< group >`


aggregate views


- `/window/< time_window >/group/< group >`
  - list of objects for a group split by the specified time delimiter
  - query parameters:
    - `start_time`: ISO 8601 start time
- `/window/< time_window >/building/< building >`
  - list of objects for a building split by the specified time delimiter
  - query parameters:
    - `start_time`: ISO 8601 start time



## Tools

#### Language

For ease of development we will use Python with the [Flask framework](http://flask.pocoo.org/).
Flask allows simple monkey patching of [Gevent](http://www.gevent.org/) for performance.


#### Database

All queries returning stats for windows of time are expensive as they must find aggregates for a large section of the data.
By using a relational database, we can leverage [materialized views](http://en.wikipedia.org/wiki/Materialized_view) to minimize repeated work to find these aggregates.
Postgres has [materialized views](https://wiki.postgresql.org/wiki/Materialized_Views) and many ADI members have experience so it will be used.

#### Authentication

The data is given to us with the understanding that we will only allow access to users with a Columbia UNI.
This can be easily accomplished with Google Oauth and a check for "@columbia.edu" / "@barnard.edu" ending the address.
This will be implemented using a [Google+ OAuth](https://developers.google.com/+/web/signin/) flow.







## Roadmap

#### Clients

The more easily a programmer can consume the data, the more the API will be used.
Adding client libraries for Python and Javascript will greatly increase the use of the API.
The API of the clients should closely mirror that of the API.
An added benefit of building clients is that we can implement the caching for them and prevent unnecessary server queries.



#### Streaming

A streaming endpoint would emit fresh data every time it is acquired.
This data would reflect the same data found in `/latest`.
Equivalent functionality could easily be implemented in client libraries.

Flask comes with streaming functionality built in (http://flask.pocoo.org/docs/0.10/patterns/streaming/).


