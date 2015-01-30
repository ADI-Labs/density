##Overview
Columbia has shared with ADI a live stream of the nubmer of devices connected to routers at various locations on campus. New counts are added every fifteen minutes. 

###Get an API Key
API keys are [available](http://density.adicu.com/auth) for Columbia univserity affiliates with valid email addresses `uni@*.columbia.edu` `uni@barnard.edu`

Visit [density.adicu.com/auth](density.adicu.com/auth) and click on `get access`


###Definitions
Please see [http://desnity.adicu.com/docs/building_info](http://desnity.adicu.com/docs/building_info) for a table of the available building names, group names, building id's and group id's. 

- Building
  - Lerner, John Jay, etc.
- Group
  - Some buildings have multiple routers which are grouped together, typically by floor.
  - Lerner-1, Butler-2, etc.
- Inputs
  - group_id
    - The numerical ID of the router group.
  - building_id a.k.a. parent_id   
    - The numerical ID of the building.        
  - time
  	- Times are in Eastern Standard Time
  	- Please use [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601) formatting: `YYYY-MM-DDThh:mm`

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
  - **/window/\<start_time\>/\<end_time\>/group/\<group_id\>**
    - Returns the data points within the specified range of times for the group.
  - **/window/\<start_time\>/\<end_time\>/building/\<building_id\>**
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

###Errors
- Authentication
  - "No authorization token provided."
	- No authentication token was provided with your request. API requests must include authentication tokens, acquired at http://density.adicu.com/auth
  - "Invalid authentication token."
    - An expired or improper authentication token was used with your request. Ensure you're using the most recent token generated with your e-mail. 

