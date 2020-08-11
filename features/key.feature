Feature: key endpoints

  Scenario: retrieving private key works
     Given we have a node running locally
     When we query the private key
     Then we should have a private key in the response