# living-lab

This repo contains code and (mostly) configurations for the living lab.
The basic idea is to test various attributes (bandwidth, jitter, latency, reliability) of a connection
(which may be behind a NAT) relative to a nearby upstream location.
This system is best for testing that will take place over weeks or months.
There are three parts to the setup:

- the management server
- the testing server
- the NanoPis (endpoints)

For a more detailed explanation of the role of each component see below.


## Components


### NanoPis

For this trial we used NanoPi NEO2s from FriendlyArm.
They are a small SBC, similar to a Raspberry Pi, but much smaller.
They also have a gigabit ethernet port.
In this use case, we ran Armbian on them.
They can be placed behind a gateway, or on the public internet,
and will perform tests from there to the testing server.
There are two types of tests that NanoPis perform:

- **Intense Tests:** These take place hourly at a time that is randomly chosen per NanoPi.
  During an intense test the NanoPi runs 4 sub-tests:

  - an iperf3 bandwidth test from the NanoPi to the testing server (also known as the "up" test)
  - an iperf3 bandwidth test from the testing server to the NanoPi (also known as the "down" test)
  - an iperf3 jitter test (results in milliseconds)
  - a sockperf one-way latency test (results in microseconds)

  After the successful completion of these tests, the results are uploaded to the management server.

- **Ping Tests:** These take place every two seconds.
  The result of a ping test is simple: either 'up' if the ping was successful,
  or 'down' if the ping was not successful.
  Ping tests use the standard `ping` command, and impose a timeout of 1 second on the command - 
  if the command does not return within this time, the link is considered down.
  While this standard is somewhat arbitrarily imposed,
  the thinking is that if a ping takes longer than this time to return
  the user's experience of the connection will be suboptimal.
  So, we consider the link to be down.

  Over time NanoPis accumulate the results of ping tests in local memory.
  There is another job which attempts to upload all ping tests to the management server
  every 5 minutes.
  If this job is unsuccessful the ping tests that it would have uploaded are included
  in the following (i.e. 5 minutes later) ping test upload.

#### Requirements
- apt
- systemd
- a sufficiently fast connection for testing whatever part of your network you want to test


### Testing Server
The testing server is the server that NanoPis test against.
It hosts servers for various protocols (a modification of iperf3, sockperf).

#### Requirements
- apt
- systemd
- should be capable of serving the maximum bandwidth that several concurrent iperf3 tests will require;
  otherwise your bandwidth results may be inaccurate


### Management Server
The purpose of the management server is to host a RESTful API that:

- tracks NanoPi metadata
- stores test results, which are uploaded from nanopis

The code for the API is stored in a [separate repository](https://github.com/adamkpickering/living-lab-api)
for ease of use with Ansible.
It uses Django and Django Rest Framework.

#### Requirements
- apt
- systemd


## Usage

This scheme uses Ansible to capture the configuration in code.
In order to use this you'll want to have at least a basic understanding of it.
For installation follow
[this guide.](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

Then, follow this process:

1.  Fill in `inventory.yml`.
    See the comments in `inventory.yml` for an explanation of what each variable represents.
    I like to leave `inventory.yml` empty and create a separate `filled_inventory.yml` so that
    I don't accidentally commit sensitive information.
    You may consider using an Ansible vault if it makes sense for your use case.

2.  Run the command: `ansible-playbook -i [filled inventory file] -K management.yml`.
    You will need to add -k to this command if you haven't configured have passwordless access to
    the management server.

3.  Log onto the management server and do

        ~/management/app/manage.py makemigrations
        ~/management/app/manage.py migrate
        ~/management/app/manage.py createsuperuser

    Enter in the credentials you want the superuser to have.
    Alternatively, there is code in `roles/management/tasks/other.yml` that is commented out that
    will take care of these steps for you, but I prefer to do them manually, especially the migrations.

4.  Run the command `ansible-playbook -i [filled inventory file] -K testing.yml`.
    This configures the testing server.
    The same advice about -k as with the management server applies here.

5.  Now you can configure the nanopis.
    Ensure that they are accessible and listed under nanopis.hosts in your inventory, and run:

        ansible-playbook -i [filled inventory file] -K endpoint.yml

    The same advice about -k as with the management server applies here.
    This step configures the nanopis to set up a local SSH tunnel to the management server's API,
    and a remote SSH tunnel accesible from the management server so it is possible to
    reconfigure them even if they are behind a NAT.

6.  You now have a choice. You may wait until the nanopis are in place (they may already be)
    or you may do the final configuration now. Either way, the command to run is

        ansible-playbook -i [filled inventory file] -K nanopi.yml

    After this step the nanopis will follow their schedule of tests against the testing server,
    and upload the results of each test to the management server.

At any point during testing you may view the results at the API.
