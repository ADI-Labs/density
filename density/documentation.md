# Introduction

Welcome to the Density API! Thanks to CUIT, ADI has a live stream of the
number of connected devices to various locations on campus. New counts are
received every 15 minutes.

# Authentication

For security purposes, we require an API key, which you can acquire
[here](https://density.adicu.com/auth). Only Columbia University affiliated
email addresses (e.g. `uni@barnard.edu` or `uni@*.columbia.edu`) are allowed.

To include the API key, you can either:
- Include the key as an HTTP header: `Authorization: [your auth token]`
- Append `?auth_token=[your auth token]` to your query URL


## Definitions

Please see
[http://density.adicu.com/docs/building_info](http://density.adicu.com/docs/building_info)
for a table of the available building names, group names, building ids and
group ids. 

- Building
  - Lerner, John Jay, etc.
- Group
  - Some buildings have multiple routers which are grouped together, typically
    by floor.
  - Lerner-1, Butler-2, etc.
- Inputs
  - group_id
    - The numerical ID of the router group.
  - building_id a.k.a. parent_id
    - The numerical ID of the building.
  - time
    - Times are in Eastern Standard Time
    - Please use [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601) formatting:
      `YYYY-MM-DDThh:mm`

# Routes
- `/latest` -- Returns the most recent data.
- `/latest/group/<group_id>` -- Returns the most recent data for the specified
  group.
- `/latest/building/<building_id>` -- Returns the most recent data for the
  speciifed building.
- `/window/<start_time>/<end_time>/group/<group_id>` -- Returns the data points
  within the specified range of times for the group.
- `/window/<start_time>/<end_time>/building/<building_id>` -- Returns the data
  points within the specified range of times for the building.
- `/day/<day>/group/<group_id>` -- Returns the aggregate data for the
  specified day and group.
- `/day/<day>/building/<building_id>` -- Returns the aggregate data for the
  specified day and building.

# Return Format
These routes return a JSON object, with the list of data points under the
`data` field. If there are additional data points not displayed, there will
also be a `next_page` field with a URL to more data points.

```
{
  "data": [
    {
      "client_count": 2, 
      "dump_time": "Fri, 02 Jan 2015 00:00:00 GMT", 
      "group_id": 23, 
      "group_name": "Uris/Watson Library", 
      "parent_id": 2, 
      "parent_name": "Uris"
    }, 
    ...
  ],
  "next_page": "http://density.adicu.com/..."
}
```

Errors will be returned in JSON format with a string representation of the
error under the field `error`. The possible errors are:

- "No authorization token provided." -- No authentication token was provided
  with your request. API requests must include authentication tokens, acquired
  at http://density.adicu.com/auth.
- "Invalid authentication token." -- An expired or improper authentication
  token was used with your request.  Ensure you're using the most recent token
  generated with your e-mail. 

## Example

### Input URL:
```
http://density.adicu.com/window/2014-10-10T08:00/2014-10-10T21:30/building/75?auth_token=[auth token]
```

### Result:
```
{
  "data": [
    {
      "client_count": 4, 
      "dump_time": "Fri, 10 Oct 2014 21:15:00 GMT", 
      "group_id": 155, 
      "group_name": "JJ's Place", 
      "parent_id": 75, 
      "parent_name": "John Jay"
    }, 
    {
      "client_count": 3, 
      "dump_time": "Fri, 10 Oct 2014 21:15:00 GMT", 
      "group_id": 125, 
      "group_name": "John Jay Dining Hall", 
      "parent_id": 75, 
      "parent_name": "John Jay"
    }, 
    ...
    {
      "client_count": 6, 
      "dump_time": "Fri, 10 Oct 2014 09:00:00 GMT", 
      "group_id": 125, 
      "group_name": "John Jay Dining Hall", 
      "parent_id": 75, 
      "parent_name": "John Jay"
    }
  ], "next_page": "http://density.adicu.com/window/2014-10-10T08:00/2014-10-10T21:30/building/75?auth_token=[auth token]&offset=100"
} 
```

or 

```
{
  "error": "Invalid authorization token"
}
```
