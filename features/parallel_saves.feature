Feature: two save commands sent in quick succession should cause a model to be saved

Scenario: one save command is sent and a model is saved
   Given a simple running vw daemon that can save models
     and a connection to the remote vw daemon 
    when training data is provided
     and a save command is sent
    then a model is saved

Scenario: two save commands are sent and a model is saved
   Given a simple running vw daemon that can save models
     and a connection to the remote vw daemon 
    when training data is provided
     and two save commands are sent in rapid succession
    then a model is saved
