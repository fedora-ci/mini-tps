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
    dnf -y install mini-tps
```

2. Prepare the system.

```
    mtps-prepare-system -p <profile-name>
```

See `mtps-prepare-system --list` for the list of available profiles.

3. Fetch the Koji/Brew builds.

```
    mtps-get-task --createrepo --installrepofile --recursive --task=${TASK_ID} --download='/var/lib/brew-repo'
```

4. Run the test. The valid tests are: install, remove, update, downgrade.

```
    mtps-run-tests --critical --selinux=1 --test=${test} --repo=brew-${TASK_ID}
```

5. If you wish to test another package, remove `/etc/yum.repos.d/brew-${TASK_ID}.repo`
   and the files in `/var/lib/brew-repo` and repeat from the step 3.

See how the installability pipeline in fedora and RHEL do that:

- [fedora prepare.sh](https://github.com/fedora-ci/installability-pipeline/blob/master/prepare.sh)
- [fedora installability_runner.sh](https://github.com/fedora-ci/installability-pipeline/blob/master/installability_runner.sh)
- [rhel prepare.sh](https://gitlab.cee.redhat.com/osci-pipelines/installability-pipeline/-/blob/master/prepare.sh) (internal GitLab)
- [rhel](https://gitlab.cee.redhat.com/osci-pipelines/installability-pipeline/-/blob/master/installability_runner.sh) (internal GitLab)

## Copr RPM builds

### From a pull request

The [.packit.yaml](.packit.yaml) tells [Packit](https://packit.dev) to build RPMs from
pull requests in Copr. RPMs from each PR are in a separate repository which you can enable
to install the RPM.

For example, for [PR#43](https://github.com/fedora-ci/mini-tps/pull/43)
the repository is [packit/fedora-ci-mini-tps-43](https://copr.fedorainfracloud.org/coprs/packit/fedora-ci-mini-tps-43/) (might be already deleted).
You can either run `dnf copr enable packit/fedora-ci-mini-tps-43 ` or if you need a URL to the
repo file then you can find it in the `Repo Download` on the Copr page.

### From the main branch

Currently, we don't build automatically because there are no tests and
an unnoticed push to `main` could silently break our RHEL/Fedora pipelines.
To create a new SRPM, either:

- run `packit srpm` or
- run `rpmdev-bumpspec mini-tps.spec` and `packit srpm --no-update-release`

Then, go to [@osci/mini-tps New Build](https://copr.fedorainfracloud.org/coprs/g/osci/mini-tps/add_build_upload),
select the SRPM file and hit `Build`

To enable the automatic builds, all you need to do is uncomment the `copr_build` job
in the [.packit.yaml](.packit.yaml).

## Testing your change in a Jenkins pipeline

Mini-TPS is used in the installability pipeline in Fedora and RHEL. The way you can test a
change from a (yet unmerged) pull request in those pipelines:

#### Fedora

- Replace `dnf -y copr enable @osci/mini-tps` with `dnf -y copr enable packit/fedora-ci-mini-tps-<PR-number>`
  in [prepare.sh](https://github.com/fedora-ci/installability-pipeline/blob/master/prepare.sh#L13)
  and open a PR in the [repo](https://github.com/fedora-ci/installability-pipeline).
- Once the PR appears in [pipelines for PRs](https://osci-jenkins-1.ci.fedoraproject.org/job/fedora-ci/job/installability-pipeline/view/change-requests/), submit `Build with Parameters`.

#### RHEL

- Replace [repo url](https://gitlab.cee.redhat.com/osci-pipelines/installability-pipeline/-/blob/ae25435bb668a59e431e2bc33ff299839023f11d/prepare.sh#L34)
  with `https://copr.fedorainfracloud.org/coprs/packit/fedora-ci-mini-tps-<PR-number>/repo/epel-${EPEL_VERSION}` and open an MR in the
  [repo](https://gitlab.cee.redhat.com/osci-pipelines/installability-pipeline).
- Once the MR appears in [pipelines for MRs](https://jenkins.prod.osci.redhat.com/job/OSCI-Pipelines/job/osci-pipelines%252Finstallability-pipeline/view/change-requests/),
  submit `Build with Parameters`.
