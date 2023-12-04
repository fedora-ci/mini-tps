# Mini TPS (installability)

This is a lightweight version of the TPS.

Installability test checks that given RPMs can be:

- installed
- removed
- updated
- downgraded

mini-tps has no external dependencies. The original TPS runs on Red Hat products, mini-tps
was designed to be triggered early in the development process. It runs on Koji/Brew builds.

## How to run it locally

You will need a VM and a Koji/Brew task id of the build that you want to test.

Run the following commands in the VM:

1. Install mini-tps.

```
    dnf copr enable @osci/mini-tps
    dnf install -y mini-tps
```

2. Prepare the system.

```
    mtps-prepare-system -p <profile-name>
```

See `mtps-prepare-system --list` for the list of available profiles.

3. Fetch the Koji/Brew builds.

```
    mtps-get-task --recursive --task=${TASK_ID} --srpm
    mtps-get-task --createrepo --installrepofile --recursive --task=${TASK_ID} --download='/var/lib/brew-repo'
```

4. Run the test. The valid tests are: install, remove, update, downgrade.

```
    mtps-run-tests --critical --selinux=1 --test=${test} --repo=brew-${TASK_ID}
```

5. If you wish to test another package, remove `/etc/yum.repos.d/brew-${TASK_ID}.repo`
   and the files in `/var/lib/brew-repo` and repeat from the step 3.
