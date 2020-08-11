Feature: transaction endpoints

  Scenario: sending millix works
     Given we have a node running locally
      And we have a balance of atleast 100 millix
      And we query the balance of mxhqb6JX4UkG3M2MfBLVaRUWxRUqC2BTYalalmxhqb6JX4UkG3M2MfBLVaRUWxRUqC2BTYa
     When we send 1 millix to mnmKVTVcwXB2w6n816dHRttQgZP7SuUhKW
      And we wait 5 seconds
     Then we should have 1 millix less when we query

  Scenario: creating many transactions in row
    Given we have a node running locally
      And we have a balance of atleast 100 millix
      And we query the balance of mxhqb6JX4UkG3M2MfBLVaRUWxRUqC2BTYalalmxhqb6JX4UkG3M2MfBLVaRUWxRUqC2BTYa
    When we send 1 millix to mnmKVTVcwXB2w6n816dHRttQgZP7SuUhKW 5 times with 10 seconds interval
      Then we should have 5 millix less when we query


  Scenario: getting transaction output works
    Given we have a node running locally
    When we query transaction output of transaction BbYAZLcxbx6adN3KwHZSTGjE6VpeDhiJ3ZPrXs6EMAGqDPfi5 at position 0 in shard shard_zero
    Then we should have an output with 9000000000000000 millix in the response