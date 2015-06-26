Feature: Saving the model does not change vw behavior

Scenario: saving does not change behavior
   Given a simple running vw daemon that can save models
     and a connection to the remote vw daemon
    when initial training data is provided
     and more training data is provided and results are saved to a file
     and the vw daemon is killed
   given a simple running vw daemon that can save models
     and a connection to the remote vw daemon
    when initial training data is provided
     and a save command is sent
    then more training data is run and saved to a second file
     and there is no difference between the saved outputs

Scenario: saving without decay learning rate does not change behavior
   Given a vw daemon running that has no decay learning rate
     and a connection to the remote vw daemon
    when initial training data is provided
     and more training data is provided and results are saved to a file
     and the vw daemon is killed
   given a vw daemon running that has no decay learning rate
     and a connection to the remote vw daemon
    when initial training data is provided
     and a save command is sent
    then more training data is run and saved to a second file
     and there is no difference between the saved outputs