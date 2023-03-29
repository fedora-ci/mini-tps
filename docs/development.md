# How to build SRPM

```sh
tar --transform 's,^,mini-tps/,' -czf mini-tps.tar.gz README.md mini-tps.conf mtps-* profiles/ viewer/
rpmdev-bumpspec --comment='Build with the latest changes.' --userstring='Andrei Stepanov <astepano@redhat.com>' mini-tps.spec
rpmbuild --define="_sourcedir $PWD" --define="%_srcrpmdir $PWD" -bs mini-tps.spec
```

# Aux commands

```
xmllint --xpath 'string(//member[name="build_id"]/value/int/text())' list.xml
curl -k --data @xml-list-rpms "${BREWHUB}" > listg
brewbuild echo 'ls //member[value/string="src"]/../member[name="nvr"]/value/string/text()' | xmllint --shell list.xml 
echo 'ls //member[value/string="noarch"]/../member[name="nvr"]/value/string/text()' | xmllint --shell listg | sed -n -e 's/^.*[[:space:]]//p' 
curl -k --data @xmldownloadTaskOutput.xml "${BREWHUB}"
brew -d --debug-xmlrpc taskinfo 18326749    
koji list-api
git archive --format=tar.gz --prefix mini-tps/ -o mini-tps.tar.gz -v master
rpmdev-bumpspec --comment='Build with the latest merged PRs.' --userstring='Andrei Stepanov <astepano@redhat.com>' mini-tps.spec
rpmbuild --define="_sourcedir $PWD" --define="%_srcrpmdir $PWD" -bs mini-tps.spec
brew --authtype=kerberos build --scratch rhel-8.0-build mini-tps-0.1-2.el7.centos.src.rpm
copr-cli --config ~/.config/copr2 build @osci/mini-tps mini-tps-0.1-66.el7.src.rpm
https://copr.fedorainfracloud.org/coprs/g/osci/mini-tps/package/mini-tps/
```
