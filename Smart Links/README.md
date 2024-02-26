SmartLinks
You can link from recognized portions of log lines in the search results. For example, you may want to have the value of a field called userId link to that user's page in your company directory. To do that, you configure the link in your /scalyr/logs configuration file:

searchResultLinks: [
 {
  regex: "(\\d+)",
  url: "https://dir.example.com/lookup?id=${1}",
  searchFields: "userId"
 }
]

See full docs here

https://app.scalyr.com/help/smart-links
