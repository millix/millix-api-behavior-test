Feature: wallet endpoints

  Scenario: retrieving mnemonic works
     Given we have a node running locally
     When we query the mnemonic
     Then we should have mnemonic in the response