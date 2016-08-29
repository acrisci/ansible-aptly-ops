# Ansible Aptly Ops

**Work in progress**

Scripts to manage Debian repos and mirrors created with [Aptly](https://www.aptly.info/).

This project is based on the [ansible-aptly-role](https://github.com/alexey-sveshnikov/ansible-aptly-role) but as a standalone project with greater scope.

This project currently is only tested on Ubuntu 16.04 xenial, but other Debian flavors may be supported in the future.

## Usage

### Creating a Repository

Ansible aptly ops is capable of creating a custom Debian repository for your project.

#### Hosts Configuration

Hosts are configured in the `hosts` file. See the documentation for [Ansible Inventory](http://docs.ansible.com/ansible/intro_inventory.html) for more information about how to specify hosts. Use the `[repo-server]` group to decide which hosts should be repo servers.

#### Repository Configuration

Next configure your repository in the `group_vars/all` file. Here is an example configuration:

```yaml
aptly_repositories:
    -
        name: yourcompany-dev
        comment: Developent packages
        distribution: trusty
        component: main
        architectures: amd64,i386
```

See the [Aptly documentation](https://www.aptly.info/doc/aptly/repo/create/) for repos for more information on what each configuration parameter does.

#### Generate Keys

A public/private keypair is required to sign packages for the repository. The keys should be located under `secrets/aptly/private.key` and `secrets/aptly/public.key` respectively.

To use an existing key, export the keys to that location like this:

```
# find the key id you want to use (in this case 61B1BA69)
gpg --list-keys
# export the private key
gpg --export-secret-keys --armor 61B1BA69 > secrets/aptly/private.key
# export the public key
gpg --export --armor 61B1BA69 > secrets/aptly/public.key
```

Then add the key id to the `group_vars/all` file like this:

```yaml
aptly_secret_key_id: 61B1BA69
```

To create a new keypair for development and do all the above steps automatically, use the `./gen-key.sh` script (hint: key generation will go faster if you have `haveged` installed).

#### Publish Repository

The `aptly-ops.py` script can publish a list of Debian packages from the command line. Use the `publish-repos` command and give a list of Debian packages to publish to the repo.

```
./aptly-ops.py publish-repos ./dummy_0.1_all.deb
```

Alternatively, you can run the Ansible playbook yourself by adding the Debian packages to the `aptly_debs` var in `site.yml`.

```
ansible-playbook -i hosts --ask-become-pass site.yml
```

This step will drop and recreate the repos so they only include the given Debian packages.

## Todo

* better key management with vault
* mirrors
* replication
* command line utility
* nginx access controls

## License

This work is licensed under a BSD license (see LICENSE)

© 2016 Tony Crisci
