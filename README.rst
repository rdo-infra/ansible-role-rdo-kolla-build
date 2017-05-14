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


Build and push all (default) supported containers to a private insecure docker-registry
---------------------------------------------------------------------------------------
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

Build and push all (default) supported containers to an authenticated registry
------------------------------------------------------------------------------
.. note:: Note that the default list of container images to build is provided
          by `tripleo-common`_.

::

    ---
    # playbook.yml
    # An OpenShift registry does not require to set a username and email
    - name: Build Kolla images
      hosts: build_node
      become: yes
      become_user: root
      vars:
        kolla_registry: "trunk.registry.rdoproject.org"
        kolla_push: true
        kolla_registry_password: openshift-token
        kolla_registry_cacert: |
          -----BEGIN CERTIFICATE-----
          MIIC6jCCAdKgAwIBAgIBATANBgkqhkiG9w0BAQsFADAmMSQwIgYDVQQDDBtvcGVu
          c2hpZnQtc2lnbmVyQDE0OTQ2MjU3ODQwHhcNMTcwNTEyMjE0OTQzWhcNMjIwNTEx
          MjE0OTQ0WjAmMSQwIgYDVQQDDBtvcGVuc2hpZnQtc2lnbmVyQDE0OTQ2MjU3ODQw
          ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDR5SMhOK/LrXA9Hr6Ij/hi
          rW++SIiIR3NI9pGWM8b58tyb//tlQCCxpAVd2NDKHlRGEYWOc6cq3Br/uGpyVxKO
          pWNJoGCXlGlwQtUne56ICOBbk39DVqFiWshtU7JCkiI3Q7Lr3AXaUJQ8ZnBlYSaL
          If4rx4l7qQLzqsBY8RQB8ZZ5wgL2sHux4l1u+mX3678VaeibigWduR6g/6KrBwz0
          p4okfhOxfNVImWeYktv0lke+WpROIkXRZXH/dzskLpyvsqKuGo8QeKqAdhHSzr49
          fO5yYYK0phkFRXSSMOf2SFymUAYHEkkmWDq3me6+fmeOv02F8Rzjjck1K1cuQOhb
          AgMBAAGjIzAhMA4GA1UdDwEB/wQEAwICpDAPBgNVHRMBAf8EBTADAQH/MA0GCSqG
          SIb3DQEBCwUAA4IBAQAp9MCNzfl487S2wGyAtL1qVbLQyDUnOZOqvXDAq2cxMcuC
          sKK+U00rPF1L9qf6tlWKczR0b1HSfBFuYZ8+F5Z5AdVUjSsbkfswQJXvesXpGY1/
          TzFP7V3deW5r9KIPMvQb7zzWNIbYxCel5ZfFcfp0Ruryzh1wl8BepmwEoqbTP2pw
          64ozdU38BV6ygQ1b5sRla/ibwIrJn7WwZPwAvr93q0xmv9i/h06wp4FA5k9i41oD
          Ff/jqQBPskGarOLaKjCxvMI83LbDn3VDcafXxVEDrYHfq4AzbCd3oWPe7M4kyf54
          YCeM/13GP41SdtgPCL0+CovbGxlrcSwcPFK90FhF
          -----END CERTIFICATE-----
      tasks:
        - include_role:
            name: "kolla-build"

``ansible-playbook -i hosts playbook.yml``

This will, on a CentOS host in the ``build_node`` Ansible inventory group:

- Install and configure Docker
- Install and configure Kolla
- Build all default supported containers
- Push them to the registry

.. _tripleo-common: https://github.com/openstack/tripleo-common/blob/master/container-images/overcloud_containers.yaml
