#!/bin/bash

set -e
set -x

tar --transform 's,^,mini-tps/,' -czf mini-tps.tar.gz README.md mtps-* profiles/ viewer/
rpmbuild --define="_sourcedir $PWD" --define="%_srcrpmdir $PWD" -bs mini-tps.spec
