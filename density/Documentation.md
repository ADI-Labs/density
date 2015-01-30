##Overview
Columbia has shared with ADI a live stream of the number of devices connected to routers at various locations on campus. New counts are added every fifteen minutes. 

###Get an API Key
API keys are [available](http://density.adicu.com/auth) for Columbia University affiliates with valid email addresses `uni@*.columbia.edu` `uni@barnard.edu`.

Visit [density.adicu.com/auth](density.adicu.com/auth) and click on `get access`. 

###Using API Keys
Most routes require an API key to return data. Without the API key, you'll get an error (described under errors). 

To include the API key in your request, you can either:
   
   - Append `?auth_token=[your auth token]` to your query URL.
    
   - Include a header parameter `Authorization-Token` with your auth token in your request. 


###Definitions
Please see [http://density.adicu.com/docs/building_info](http://density.adicu.com/docs/building_info) for a table of the available building names, group names, building ids and group ids. 

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
- Ranged Data
  - **/window/\<start_time\>/\<end_time\>/group/\<group_id\>**
    - Returns the data points within the specified range of times for the group.
  - **/window/\<start_time\>/\<end_time\>/building/\<building_id\>**
    - Returns the data points within the specified range of times for the building.

- Day Aggregate
  - **/day/\<day\>/group/\<group_id\>**
    - Returns the aggregate data for the specified day and group.
  - **/day/\<day\>/building/\<building_id\<**
    - Returns the aggregate data for the specified day and building.
 - **Return Format**	
  	
  	- JSON with client_count, dumptime, group_id, group_name, parent_id, and parent_name 	
    
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
    ```

###Errors
Parameter errors will be returned in JSON format with a string representation of the error under the field `error`.

- Authentication
  - "No authorization token provided."
	- No authentication token was provided with your request. API requests must include authentication tokens, acquired at http://density.adicu.com/auth.
  - "Invalid authentication token."
    - An expired or improper authentication token was used with your request. Ensure you're using the most recent token generated with your e-mail. 

