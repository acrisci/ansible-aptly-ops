# Ansible Aptly Ops

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

The `aptly-ops.py` script can publish a repository the command line. Use the `create-repos` command to publish the configured repositories.

```
./aptly-ops.py create-repos
```

#### Add Debian Packages

Now use the `aptly-ops.py` to add Debian packages to your configured repositories.

```
./aptly-ops.py add-debs ./dummy_0.1_all.deb
```


#### Using on the Client

First add your public key to trusted apt keys.

```
sudo apt-key add secrets/aptly/public.key
```

Then add an entry in your sources.list config directory.

```
# in file /etc/apt/sources.list.d/yourcompany-dev.list
deb http://[HOST]/yourcompany-dev trusty main
```

Now update apt with `sudo apt-get update` and your packages should be available to install.

## Todo

* mirrors

## License

This work is licensed under a BSD license (see LICENSE)

© 2016 Tony Crisci
