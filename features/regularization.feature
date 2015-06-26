Feature:  VW can regularize features consistently

@wip
 Scenario:  The model produced in daemon mode matches the model in offline mode
   Given a vw daemon running without regularization
     and a connection to the remote vw daemon
    when the regularization data set is provided
    then the model is identical to the previously saved non-regularized model


 Scenario:  The regularized model produced in daemon mode matches the model in offline mode
   Given a vw daemon running with regularization
     and a connection to the remote vw daemon
    when the regularization data set is provided
    then the model is identical to the previously saved regularized model