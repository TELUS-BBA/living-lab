# living-lab

This repository contains code and (mostly) configurations for a connection testing system.
It allows you to test various attributes (bandwidth, jitter, latency, reliability) of a connection
between an endpoint (which may be beind NAT) and a single testing server.
It is also possible to change the testing behaviour on a per-endpoint basis.
This system is intended to carry out testing over a timeframe of weeks or months.

- [Components](#components)
  - [NanoPis](#nanopis)
  - [Testing Server](#testing-server)
  - [Management Server](#management-server)
- [Security Model](#security-model)
- [Usage](#usage)
  - [Initial Configuration](#initial-configuration)
  - [Updating Components](#updating-components)


## Components


### NanoPis

For this trial we used NanoPi NEO2s from FriendlyArm, though any system that fits the requirements can be used.
NanoPis are small SBCs that are similar to a Raspberry Pi, but smaller.
They also have a gigabit ethernet port.
In this use case, we ran Armbian on them.
They can be placed behind a gateway, or on the public internet.
All tests involve the connection between the NanoPi and the testing server.
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
  While this standard may seem arbitrary,
  the thinking is that if a ping takes longer than this time to return
  the user's experience of the connection will be impacted.
  Thus, we consider the link to be down.

  Over time NanoPis accumulate the results of ping tests in local memory.
  There is another job which attempts to upload all ping tests to the management server every 5 minutes.
  If this job is unsuccessful the ping tests that it would have uploaded are included
  in the following (i.e. 5 minutes later) ping test upload.

#### Requirements

- apt
- systemd
- a sufficiently fast connection for testing whatever part of your network you want to test


### Testing Server

The testing server is the server that NanoPis test against.
It hosts servers for various protocols
(currently sockperf and a modification of iperf3 that allows for concurrent tests, called iperf3-mux).

#### Requirements

- apt
- systemd
- should be capable of serving the maximum bandwidth that the configured number of concurrent iperf3 tests
  will require (see inventory variable `max_iperf_concurrent_tests`); otherwise your bandwidth results
  may be inaccurate


### Management Server

The purpose of the management server is to host a RESTful API that:

- tracks NanoPi metadata
- stores test results, which are uploaded from NanoPis

The code for the API is stored in a [separate repository](https://github.com/adamkpickering/living-lab-api)
for ease of use with Ansible.
It uses Django and Django Rest Framework.

#### Requirements

- apt
- systemd


## Security Model

This system is secured with SSH tunnels.
The API on the management is only accessible locally (i.e. localhost:5000).
This forces all outside access to go through an SSH local tunnel, which is relatively secure.
This also enables us to simplify authentication by using HTTP Basic Authentication,
which would otherwise be unsecure since it sends credentials in plain text in the headers of each request.
So, NanoPis are configured to set up two SSH tunnels:

- a local SSH tunnel to the management server's API, and
- a remote SSH tunnel from the NanoPi to the management server, which makes it possible to
  - ssh into each NanoPi to do manual configuration/maintenance
  - run Ansible playbooks from the management server that configure the NanoPis
    (because of undetermined reasons, possibly problems with tunnelling TCP over TCP, this
    is about 95% effective - you may need to re-run playbooks in the event that a connection drops)

When each NanoPi is provisioned (i.e. a profile is created for it in the API) it is assigned
a unique primary key (id) by Django.
Typically these start at 1 and increase by increments of 1.
Since we can't have any two NanoPis trying to open a remote tunnel on the same port,
the primary key is used to calculate a unique port number according to the formula

    [remote tunnel port] = 6000 + [primary key]

So if I have a NanoPi with an id (primary key) of 14,
I'll be able to ssh into it from the management server with the command

    ssh nanopi@localhost -p 6014


## Usage

### Initial Configuration

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

2.  Run the command

        ansible-playbook -i [filled inventory file] -K management.yml

    You will need to add -k to this command if you haven't configured have passwordless access to
    the management server.

3.  SSH into the management server and run

        ~/management/app/manage.py makemigrations
        ~/management/app/manage.py migrate
        ~/management/app/manage.py createsuperuser

    Enter in the credentials you want the superuser to have.
    Alternatively, there is code in `roles/management/tasks/other.yml` that is commented out that
    will take care of these steps for you, but I prefer to do them manually, especially the migrations.

4.  Configure the testing server with the command

        ansible-playbook -i [filled inventory file] -K testing.yml

    The same advice about -k as with the management server applies here.

5.  Now you can configure the NanoPis.
    Ensure that they are accessible and listed under `nanopis.hosts` in your inventory, and run:

        ansible-playbook -i [filled inventory file] -K endpoint.yml

    The same advice about -k as with the management server applies here.
    This step configures the NanoPis to set up reliable SSH tunnels to the management server.
    See the above section on security for more details. 

6.  You now have a choice. You may wait until the NanoPis are in place (they may already be)
    or you may do the final configuration now, disconnect them, and reconnect them
    at the place you want to test from. Either way, the command to run is

        ansible-playbook -i [filled inventory file] -K nanopi.yml

    If the NanoPis are behind a NAT you'll have to run this command from the management
    server with the inventory group `nanopis` configured as (for example)

        nanopis:
          vars:
            ansible_host: localhost
            ansible_user: nanopi_user
            ...
          hosts:
            nanopi1:
              ansible_port: 6001
            nanopi2:
              ansible_port: 6002
            nanopi3:
              ansible_port: 6003

    After this step the NanoPis will periodically run their tests against the testing server,
    and upload the results of each test to the management server.


### Updating Components

These playbooks are all idempotent, with one exception:
the minute of the hour that the NanoPi performs an intense test will change each time you run `nanopi.yml`.
However, this shouldn't be a problem.
The fact that the playbooks are idempotent means that you can run them as many times as you want,
and the same final state will still be achieved.

So if you change something with the NanoPis, simply run (from the management server)

    ansible-playbook -i [filled inventory file] -K nanopi.yml

as before and the NanoPi will be updated with your changes.
Similarly, you may re-run the playbooks for the management server and testing server
to deploy changes you've made to their code.
Keep in mind that if any of the management server API's models change
you'll need to update the database manually by SSHing in and running

    ~/management/app/manage.py makemigrations
    ~/management/app/manage.py migrate
