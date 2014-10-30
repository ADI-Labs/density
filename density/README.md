
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
    - **TODO**: Figure out how to give group id's to users.
  - building_id
    - The numerical ID of the building.
    - **TODO**: Figure out how to give id's to users
  - day
    - **TODO**: Figure out the format of the date (Currently using ISO 8601)
  - time
    - **TODO**: Figure out the format of the time range
- Outputs
  - **TODO**: Figure out output format.

###Routes
- Latest Data
  - **/latest**
    - Returns the most recent data.
  - **/latest/group/&lt;group_id&gt;**
    - Returns the most recent data for the specified group.
  - **/latest/building/&lt;building_id&gt;**
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

- Day Aggregate
  - **/day/&lt;day&gt;/group/&lt;group_id&gt;**
    - Returns the aggregate data for the specified day and group.
  - **/day/&lt;day&gt;/building/&lt;building_id&gt;**
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
  - **/window/&lt;time&gt;/group/&lt;group_id&gt;**
    - Returns the aggregate data for the specified time range and group.
  - **/window/&lt;time&gt;/building/&lt;building_id&gt;**
    - Returns the aggregate data for the specified time range and building.
  - **Return Format**
    - See Day Aggregate

###Errors

Not implemented yet!


###Rate limiting

Not implemented yet!

