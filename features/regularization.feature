Feature:  VW can regularize features consistently

 Scenario:  The model produced in daemon mode matches the model in offline mode
   Given a vw daemon running without regularization
     and a connection to the remote vw daemon
     and a saved non-regularized model made in offline mode
    when the regularization data set is provided
     and a save command is sent
    then a model is saved
     and the model is identical to the previously saved non-regularized model

 Scenario:  The regularized model produced in daemon mode matches the model in offline mode
   Given a vw daemon running with regularization
     and a connection to the remote vw daemon
     and a saved regularized model made in offline mode
    when the regularization data set is provided
     and a save command is sent
    then a model is saved
     and the model is identical to the previously saved regularized model