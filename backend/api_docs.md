Welcome to GdzieJestTenCholernyTramwaj api description
===================

For our communication between frontend (AngularJS) and backend (Python Tornado) we are using RESTful API.

To test api calls we recommend to use software as **curl** or some dedicated REST client for your favorite browser.

First of all, you need to set up your backend, in order to do that, please refer to [this readme-file instruction](https://github.com/evemorgen/GdzieJestTenCholernyTramwajProject/blob/master/backend/schedule_worker/README.md)

In the following examples, we will assume that you have your backend running on your local machine on port 8888.

Currently avaliable endpoints are:
  1. /healthcheck
  2. /mpk_db


----------


###1. Healthcheck
    Healthcheck is an endpoint which provides only one method to check if your application did not crashed.
<table>
    <tr><td>Method: POST</td></tr>
    <tr><td>Format: JSON</td></tr>
    <tr><td>Parameters: <br /><br />
        This method does not requires any parameters, you need to pass an empty object. - {}
        </tr></td>
    <tr><td>Returns:     <br /><br />
    Json object with: <br />
        <ul>
            <li>status - current backend state, normally should return "OK" string </li>
            <li>number - random number between 0 and 9 </li>
</table>

Usage example:

Call:
```
curl -X POST -d '{}' http://localhost:8888/healthcheck
```
Return:
```
{
    "number": 7,
    "status": "OK"
}
```

----------

### 2. Mpk_db
    Mpk_db endpoint is there to provide info about current public transport estimated location for certain trams/busses.

Avaliable methods:
    1. force_update
    2. get_status
    3. get_position

##### 1. force_update
    force_update method forces backend do download new database containing actual public transport schedules. Until new db is downloaded, backend worker uses old db.

<table>
    <tr><td>Method: POST</td></tr>
    <tr><td>Format: JSON</td></tr>
    <tr><td>Parameters: <br /><br />
        This method does not requires any parameters, you need to pass an empty object. - {}
        </tr></td>
    <tr><td>Returns:     <br /><br />
    Json object with: <br />
        <ul>
            <li>status - current operation state, normally should return "OK" string </li>
</table>

Usage example:

Call:
```
curl -X POST -d '{}' http://localhost:8888/mpk_db/force_update
```
Return:
```
{
    "status": "OK"
}
```
-------------

##### 2. get_status
    get_status method allows you to get last N backend states. This mechanism is very usefull for debuging purposes. Also known as application logs.

<table>
    <tr><td>Method: POST</td></tr>
    <tr><td>Format: JSON</td></tr>
    <tr><td>Parameters: <br /><br />
            <ul> <li> number - number of logs to return </li> </ul>
    </tr></td>
    <tr><td>Returns:     <br /><br />
    Json object with: <br />
        <ul>
            <li>status - array of logs arrays. Log array contains log string and timestamp</li>
</table>

Usage example:

Call:
```
curl -X POST -d '{"number": 3}' http://localhost:8888/mpk_db/get_status
```
Return:
```
{"status":
    [
        ["get_status requested", "2016-12-04 12:55:44.992554"],
        ["fetching line 64", "2016-12-04 12:48:58.989501"],
        ["filling przystanki db cache", "2016-12-04 12:48:27.558909"]
    ]
}
```
-------------
##### 3. get_position
    get_position method provides frontend information about current tram/bus position including estimated delay
<table>
    <tr><td>Method: POST</td></tr>
    <tr><td>Format: JSON</td></tr>
    <tr><td>Parameters: <br /><br />
        #fixme, not yet implemented
        </tr></td>
    <tr><td>Returns:     <br /><br />
        #fixme, not yet implemented
        </tr> </td>
</table>

Usage example:

Call:
```
curl -X POST -d '
{
    "mock": "argument",
    "not": "implemented"
}' http://localhost:8888/mpk_db/get_position
```
Return:
```
{
    "noone": "cares",
    "number": -0
}
```
-------------
