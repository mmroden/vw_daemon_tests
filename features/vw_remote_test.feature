Feature: Can update remote model in vw

  Scenario: Can train the remote model
    Given a simple running vw daemon
      and a connection to the remote vw daemon
     when training data is provided
      and testing data is sent
     then the remote cluster responds appropriately