invoker-docker
==============

Uses docker-compose to manage building, testing and publishing docker containers.

Commands
--------

* ``docker.build``: Builds the controlled docker containers and optionally applies
  a provided label.
* ``docker.test``: Tests the built container optionally building before hand. 
* ``docker.push``: Pushes the managed docker containers optionally building and
  before labeling beforehand

Parameters
----------

* ``docker_cmd``: The command used when running docker (default: `docker`)
* ``docker_compose_cmd``: The command to use when running docker-compose (default:
  ``docker-compose``)
* ``docker_compose_file``: The file to use when using docker-compose (default:
  ``docker-compose.yml``)
* ``docker_managed_services``: The names of the services to use when building
  and publishing images
* ``docker_compose_test_services``: A set of services and commands to run when
  testing (default: ``{'test': []}``)
