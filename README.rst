ansible-role-rdo-kolla-build
============================

This Ansible role provides the ability to build, tag and push Docker containers
for usage in TripleO_ with tooling provided by Kolla_.

.. _TripleO: http://tripleo.org/
.. _Kolla: https://github.com/openstack/kolla

Requirements
============
This Ansible role uses ARA_ to do reporting on the results of the role
execution as well as track metadata on what the containers were built with.

To set up ARA::

    pip install ara

    ara_location=$(python -c "import os,ara; print(os.path.dirname(ara.__file__))")
    export ANSIBLE_CALLBACK_PLUGINS="${ara_location}/plugins/callbacks"
    export ANSIBLE_ACTION_PLUGINS="${ara_location}/plugins/actions"
    export ANSIBLE_LIBRARY="${ara_location}/plugins/modules"

ARA can also be configured to be used through your `ansible.cfg file`_.

.. _ARA: https://github.com/openstack/ara
.. _ansible.cfg file: https://ara.readthedocs.io/en/latest/configuration.html#using-ansible-cfg

Parameters and configuration
============================
For the full list of parameters and configuration available for this role,
refer to the `default variable file`_.

.. _default variable file: https://github.com/rdo-infra/ansible-role-rdo-kolla-build/blob/master/defaults/main.yml

Example usage
=============
Only build containers related to nova
-------------------------------------
::

    ---
    # playbook.yml
    - name: Build Nova Kolla images
      hosts: build_node
      become: yes
      become_user: root
      vars:
        kolla_rdo_images:
          - nova
      tasks:
        - include_role:
            name: "kolla-build"

``ansible-playbook -i hosts playbook.yml --tags "setup,build"``

This will, on a CentOS host in the ``build_node`` Ansible inventory group:

- Install and configure Docker
- Install and configure Kolla
- Build only nova related containers (and their parent layers)


Build and push all (default) supported containers to a private registry
-----------------------------------------------------------------------
.. note:: Note that the default list of container images to build is provided
          by `tripleo-common`_.

::

    ---
    # playbook.yml
    - name: Build Kolla images
      hosts: build_node
      become: yes
      become_user: root
      vars:
        kolla_registry: "127.0.0.1:5000"
        kolla_insecure_registry: true
        kolla_push: true
      tasks:
        - include_role:
            name: "kolla-build"

``ansible-playbook -i hosts playbook.yml``

This will, on a CentOS host in the ``build_node`` Ansible inventory group:

- Install and configure Docker
- Install and configure Kolla
- Build all default supported containers
- Push them to the private registry 127.0.0.1:5000

.. _tripleo-common: https://github.com/openstack/tripleo-common/blob/master/container-images/overcloud_containers.yaml