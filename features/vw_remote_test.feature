Feature: Can update remote model in vw

  Scenario: Can train the remote model
    Given a connection to a remote vw cluster
     when training data is provided
      and testing data is sent
     then the remote cluster responds appropriately