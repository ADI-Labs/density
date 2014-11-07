
#Overview

### `density.py`

This is the executable file for the project.


###Definitions
- Building
  - Lerner Hall, Hamilton Hall, etc.
- Group
  - Each building has multiple routers, which are grouped together.
  - Lerner-1, Hamilton-3, etc.
- Inputs
  - group_id
    - The numerical ID of the router group.
    - A table of id's will be given to the user when a bad id is provided.
  - building_id
    - The numerical ID of the building.
    - A table of id's will be given to the user when a bad id is provided.
  - day
    - Use ISO 8601 formatting!
    - http://en.wikipedia.org/wiki/ISO_8601
  - time
    - **TODO**: Figure out the format of the time range
- Outputs
  - **TODO**: Figure out output format.

###Routes
- Latest Data
  - **/latest**
    - Returns the most recent data.
  - **/latest/group/\<group_id\>**
    - Returns the most recent data for the specified group.
  - **/latest/building/\<building_id\>**
    - Returns the most recent data for the speciifed building.
  - **Return Format**
    - Dictionary with router group ID as the key.
    - name - Name of router group
    - client_count - Number of devices connected
    - parent_id - Building ID.
    ```
    {
      "results": {
        "152": {
          "name": "Lerner 3",
          "client_count": 70,
          "parent_id": 84
        }.
        "130": {
          "name": "Butler Library 3",
          "client_count": 328,
          "parent_id": 103
        }
        ...
      }
    }
    ```
- Ranged Data
  - **/range/\<start_time\>/\<end_time\>/group/\<group_id\>**
    - Returns the data points within the specified range of times for the group.
  - **/range/\<start_time\>/\<end_time\>/building/\<building_id\>**
    - Returns the data points within the specified range of times for the building.
  - ** Return Format **
    - next_start_time - The next time (for pagination)
    - < ID > - the building or group ID
    - count - number of data points
    ```
    {
      "next_start_time": "2014-10-27",
      "< ID >": 152,
      "count": 100,
      "results": [
        {
          "start_time": "2014-10-20",
          "average": 10,
          "minimum": 0,
          "maximum": 100
        },
        ...
      ]
    }
    ```

- Day Aggregate
  - **/day/\<day\>/group/\<group_id\>**
    - Returns the aggregate data for the specified day and group.
  - **/day/\<day\>/building/\<building_id\<**
    - Returns the aggregate data for the specified day and building.
  - **Return Format (TENTATIVE)**
    - start_time - The start of the time frame.
    - average - Average number of devices connected.
    - minimum - Minimum number of devices connected.
    - maximum - Maximum number of devices connected.
    ```
    {
      "start_time": "2014-03-28",
      "average": 10,
      "minimum": 0,
      "maximum": 100
    }
    ```

- Custom Time Frame Aggregate
  - **/window/\<time\>/group/\<group_id\>**
    - Returns the aggregate data for the specified time range and group.
  - **/window/\<time\>/building/\<building_id\>**
    - Returns the aggregate data for the specified time range and building.
  - **Return Format**
    - See Day Aggregate

###Errors

Not implemented yet!


###Rate limiting

Not implemented yet!

