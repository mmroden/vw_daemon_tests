Basic Setup
-----------

This project contains a vagrant that will stand up a virtual machine to act as a container for a VW remote system.

To run:

     make check

This command is the same as calling

     make deps
     make run
     make check

The `deps` command will install `behave` in a local virtualenv as a framework from which tests can be run.  The `run` command will bring up a local virtualbox-backed Vagrant instance and copy the IP information into a local file so that ssh commands can be sent to the box through scripts.  Finally, `make check` will run `behave`-based tests against the vagrant instance.

If you choose to run `make check_aws` instead, a vagrant instance will be created on AWS.  The settings for the instance are located in the Vagrantfile, and default to using the us-west-2 region.  Using AWS will require:
 
 * An AWS account
 * A working installation of the `vagrant-aws` plugin for vagrant.  The current best version is 0.5.0; more recent versions introduced show-stopping rsync bugs.  Installing an old version of the `vagrant-aws` plugin can be done through invoking `vagrant plugin install vagrant-aws --plugin-version 0.5.0`
  * Appropriately configured aws security groups that leave the daemon port open.  We've called these groups `endpoint` for the daemon port and `vagrant-dev` for the ssh port
  * These environment variables must be set to the appropriate values
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_KEY`
     - `AWS_KEY_NAME` 
     - `AWS_KEY_PATH`

Running either on aws or locally will require that both [virtualenv](https://pypi.python.org/pypi/virtualenv) and [vagrant](https://www.vagrantup.com) be installed locally.  The python has only been tested with version 2.7, but should be python 3 compatible.

VW Versioning
-------------

VW is created as part of provisioning the Vagrantfile.  Changing the commit to which the VW project is synced can be done by changing the `VW_COMMIT_HASH` entry in the Makefile and then calling 

    make provision

Under The Hood
--------------
Behave is a framework for BDD.  In this case, there are several specified behaviors that the daemon mode for VW should be supporting, and this project is intended to be used as a check to ensure that a particular version of VW implements specified features properly.

The current features are listed in the `features` directory.  New features can be added either by editing the extant files or by adding new feature files.  The scripts in the `features/steps` directory impement the actual features, and behave can automatically produce stubs of specified features to be added into the appropriate place.

Bringing VW up and down for each test is accomplished in `features/environment.py`.