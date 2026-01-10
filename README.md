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


## Interactive CLI

Lightsaber includes an interactive command-line utility (`lightsaber-cli.py`) that provides an easy way to run Ansible playbooks and roles with a menu-driven interface. The CLI features an animated yellow ASCII lightsaber that activates when you enter interactive mode!

### Installation

The CLI is available as a symlink in `~/wkspc/bin/lightsaber` (if that directory is in your PATH). If not already set up, you can create the symlink:

```bash
mkdir -p ~/wkspc/bin
ln -sf /path/to/lightsaber/scripts/lightsaber-cli.py ~/wkspc/bin/lightsaber
chmod +x ~/wkspc/bin/lightsaber
```

### Usage

**Interactive Mode (Menu-Driven):**

Simply run `lightsaber` without arguments to enter interactive mode:

```bash
lightsaber
```

This will display an animated lightsaber turning on, followed by an interactive menu where you can:

- Run a playbook
- Run specific tags
- Perform a dry run (check mode)
- List available playbooks
- List available tags for a playbook

**Non-Interactive Mode (Command-Line Arguments):**

You can also use the CLI with command-line arguments:

```bash
# List available playbooks
lightsaber --list-playbooks

# List tags for a playbook
lightsaber --list-tags playbooks/fedora-workstation.yml

# Run a playbook with specific tags
lightsaber --playbook playbooks/fedora-workstation.yml --tags powerline,cursor

# Run in check mode (dry run)
lightsaber --playbook playbooks/fedora-workstation.yml --check

# Run with verbose output
lightsaber --playbook playbooks/fedora-workstation.yml -vv

# Get help
lightsaber --help
```

### Features

- **Animated ASCII Lightsaber**: Enjoy a yellow ASCII lightsaber animation when entering interactive mode
- **Menu-Driven Interface**: Easy-to-use menu system for selecting playbooks and tags
- **Tag Support**: Run specific Ansible tags to target specific configurations
- **Dry Run Mode**: Test changes before applying them with check mode
- **Verbose Output**: Multiple verbosity levels for debugging (`-v`, `-vv`, `-vvv`, `-vvvv`)
- **Automatic BECOME**: All playbooks are run with privilege escalation enabled


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
