![Lightsaber logo](https://github.com/nolski/lightsaber/blob/master/logo.png?raw=true)

[![License: BSD 3-Clause License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Lightsaber has been adopted by Justin Flory's [Swiss Army Toolkit](https://gitlab.com/jwflory/swiss-army/). It's an ansible-driven configuration management for maintaining a preferred environment (base system and app configurations)



## About

Lightsaber's purpose is to manage the setup of my preferred operational environment. Like any lightsaber, it is tailor made to my exact preferences but hopefully serves as a guide or template for others to use. Some of the primary additions on top of jwflory's setup are the addition of `swaywm` and integration of theming.

Lightsaber is a set of Ansible playbooks and roles.
Roles are split into two categories:

* `system`: base system configuration (e.g. package installation)
* `apps`: specific app installation and configuration (e.g. dotfile management)

For a fully automated setup, two environments are supported: **Fedora** and **CentOS/RHEL**.


## How to use

See [`docs/how-to-use.adoc`](https://github.com/nolski/lightsaber/blob/master/docs/how-to-use.adoc "How to use jwflory/swiss-army").


## Reusing and remixing swiss-army?

This repository is licensed under the [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/ "BSD 3-Clause “New” or “Revised” License").
Reuse anything you want in your own configurations.

From @jwflory
> If you publish your remixed work on GitHub, drop a link back here in your README please. :memo:
> And you can say :wave: to me in your git commit.
> Tag me!
> `@jwflory`
