# Mini TPS

Light version of [original TPS].

Project page can be found at [confluence].

# WHY?

There are:

1. Original TPS.
2. CIPS effort.

mini-tps is very lightweight implementation. No external dependencies.
Where original TPS supposed to be run against RedHat products, mini-tps
triggered immediately for new Brew builds.

# How to run locally

The instructions below assume you are using 1minutetip to provision a recent RHEL 8 compose. You will need to get the brew task ID of the package you wish to test. 

1. Provision your system with: `1minutetip rhel8`
2. Remove system repos, add mini-tps repo and install mini-tps:

```
    REPOFILE="https://copr.devel.redhat.com/coprs/astepano/mini-tps/repo/rhel-8.dev/astepano-mini-tps.repo"
    cd /etc/yum.repos.d
    curl --retry 5 --insecure --fail --location --show-error --remote-name --remote-header-name "$REPOFILE"
    sed -i -e 's/https/http/' $(basename "$REPOFILE")
    dnf install -y mini-tps
    rm -f beaker-client.repo beaker-harness.repo beaker-tasks.repo qa-tools.repo redhat.repo rhel-latest.repo rhel.repo standard-test-roles.repo
```

3. Prepare RHEL system:

    `mtps-prepare-system -p <profile-name>`

See `mtps-prepare-system --list` for the list of available profiles.

4. Get Brew build payload:

    `mtps-get-task --recursive --task=${my_task} --srpm`
    `mtps-get-task --createrepo --installrepofile --recursive --task=${my_task} --download='/var/lib/brew-repo'`

5. Run the command below substituting the desired test for ${test} for each test you wish to run. Valid tests are: install, remove, update, downgrade. Results are logged to the console and in the `mtps-logs` directory.

    `mtps-run-tests --critical --selinux=1 --test=${test} --repo=brew-${my_task}`

6. If you wish to test another package, remove `/etc/yum.repos.d/brew-${my_task}.repo` and the files in `/var/lib/brew-repo` and repeat steps.

# How to build RPM

```sh
tar --transform 's,^,mini-tps/,' -czf mini-tps.tar.gz README.md mini-tps.conf mtps-* profiles/
rpmdev-bumpspec --comment='Build with the latest changes.' --userstring='Andrei Stepanov <astepano@redhat.com>' mini-tps.spec
rpmbuild --define="_sourcedir $PWD" --define="%_srcrpmdir $PWD" -bs mini-tps.spec
copr-cli --config ~/.config/copr2 build astepano/mini-tps mini-tps-0.1-29.el7.src.rpm
# Where ~/.config/copr2 is a config for https://copr.devel.redhat.com/
```

# Triggers

https://docs.engineering.redhat.com/display/RHELPLAN/Pipeline+Triggers

# Side tags

```sh
cat brew-build-group.json| jq '..|.artifact?.builds[]?.id'
cat brew-build-group.json| jq '..|.artifact?.id | select (.!=null)'
```

(Project info)[https://docs.engineering.redhat.com/display/RHELPLAN/Build+Group+Testing]

(datagrepper msg)[https://datagrepper.engineering.redhat.com/id?id=ID:ptp-jenkins.rhev-ci-vms.eng.rdu2.redhat.com-42901-1555143607874-46345:1:1:1:1&is_raw=true&size=extra-large]

(datagrepper msgs)[https://datagrepper.engineering.redhat.com/raw?topic=/topic/VirtualTopic.eng.ci.brew-build-group.build.complete&delta=1278000]


[original TPS]: https://wiki.test.redhat.com/ReferenceManual/Tps
[confluence]: https://docs.engineering.redhat.com/display/RHELPLAN/Installability+Testing

# Aux commands

```
xmllint --xpath 'string(//member[name="build_id"]/value/int/text())' list.xml
curl -k --data @xml-list-rpms https://brewhub.engineering.redhat.com/brewhub > listg
brewbuild echo 'ls //member[value/string="src"]/../member[name="nvr"]/value/string/text()' | xmllint --shell list.xml 
echo 'ls //member[value/string="noarch"]/../member[name="nvr"]/value/string/text()' | xmllint --shell listg | sed -n -e 's/^.*[[:space:]]//p' 
curl -k --data @xmldownloadTaskOutput.xml https://brewhub.engineering.redhat.com/brewhub 
brew -d --debug-xmlrpc taskinfo 18326749    
koji list-api
git archive --format=tar.gz --prefix mini-tps/ -o mini-tps.tar.gz -v master
rpmdev-bumpspec --comment='Build with the latest merged PRs.' --userstring='Andrei Stepanov <astepano@redhat.com>' mini-tps.spec
rpmbuild --define="_sourcedir $PWD" --define="%_srcrpmdir $PWD" -bs mini-tps.spec
brew --authtype=kerberos build --scratch rhel-8.0-build mini-tps-0.1-2.el7.centos.src.rpm
copr-cli --config ~/.config/copr2 build astepano/mini-tps mini-tps-0.1-66.el7.src.rpm
https://copr.devel.redhat.com/coprs/astepano/mini-tps/package/mini-tps/
```

# RHEL8 notes

```
  brew list-targets --name=rhel-8.2.0-z-candidate
  8.0.0-z stream != 8.0.1-z stream
```

## At the same time could be fresh builds for 8.1.0 and 8.1.0-z

Example:

8.1.0 is at `devel/test` phase.
8.1.0-z is already present.
8.1.0 all commits require release+ and either exception+ or blocker+..
-z target is created at freeze moment for GA. The same time when 0-day
z-stream.
