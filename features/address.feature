Feature: address API endpoints

  Scenario: get balance node works
     Given we have a node running locally
      When we query balance of mybE8MiVBnUCBYq344cAM4q9Y4V1L8bm9xlalmybE8MiVBnUCBYq344cAM4q9Y4V1L8bm9x
      Then we should have a balance larger than 0 in the response