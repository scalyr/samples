Scalyr sample of JSON for a starting point to use in your projects.

 - Alerts
 - Dashboards
 - Monitors
 - Parsers
 - Configs
 
 Most of them can be dropped in as is or with modifications as needed.
 
 Pull Requests are welcome.
 Help and Documentation can be found on Scalyr. https://app.scalyr.com/help/



**This data will flow into our log generator: toolkit.s1.ninja/generate**

# to add a new log samples to the toolkit

1.  Export a powerquery as json, or upload a csv of your data (csv data doesnt have types so i discourage the use of csv if you want to graph integers)
2.  upload to the `/logs` directory
3.  add dashbaord to `/dashboards` directory
4.  add parser to `/parser` directory 
5.  add mappings to `mappings.json` file
6.  refresh list toolkit.s1.ninja/generate 
7.  refresh page 
