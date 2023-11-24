Name: mini-tps
Version: 0.1
Release: 162%{?dist}
Summary: Mini TPS - Test Package Sanity

License: GPLv2
URL:     https://github.com/fedora-ci/mini-tps
Source0: %{name}.tar.gz
Requires: yum-utils
# List of packages for wich do not run 'remove' test.
Requires: openssh-server yum
BuildArch: noarch

%if 0%{?rhel} > 7
# bug: https://bugzilla.redhat.com/show_bug.cgi?id=1641631
Requires: rpm-plugin-selinux
Requires: dnf-plugins-core
Requires: libselinux-utils
%endif

%description
Light version of TPS

%prep
%autosetup -n %{name}

%build

%install
mkdir -p %{buildroot}%{_prefix}/local/bin/
cp -rfp mtps* %{buildroot}%{_prefix}/local/bin/
mkdir -p %{buildroot}%{_sysconfdir}/dnf/protected.d
cp -pf mini-tps.conf %{buildroot}%{_sysconfdir}/dnf/protected.d/

# viewer
mkdir -p %{buildroot}%{_datarootdir}/mini-tps/viewer/
cp -pf viewer/viewer.html %{buildroot}%{_datarootdir}/mini-tps/viewer/
mkdir -p %{buildroot}%{_libexecdir}/mini-tps/viewer/
cp -pf viewer/generate-result-json %{buildroot}%{_libexecdir}/mini-tps/viewer/

# profiles
mkdir -p %{buildroot}%{_datarootdir}/mini-tps/profiles/{rhel,centos-stream,fedora}/
# rhel
cp -rfp profiles/rhel/{repos,optrepos}/ %{buildroot}%{_datarootdir}/mini-tps/profiles/rhel/
# centos-stream
cp -rfp profiles/centos-stream/{repos,optrepos}/ %{buildroot}%{_datarootdir}/mini-tps/profiles/centos-stream/
# fedora
cp -rfp profiles/fedora/repos/ %{buildroot}%{_datarootdir}/mini-tps/profiles/fedora/

# prepare scripts
mkdir -p %{buildroot}%{_libexecdir}/mini-tps/{rhel,centos-stream,fedora}/
# rhel
cp -pf profiles/rhel/prepare-system %{buildroot}%{_libexecdir}/mini-tps/rhel/
# centos-stream
cp -pf profiles/centos-stream/prepare-system %{buildroot}%{_libexecdir}/mini-tps/centos-stream/
# fedora
cp -pf profiles/fedora/prepare-system %{buildroot}%{_libexecdir}/mini-tps/fedora/

%files
%{_prefix}/local/bin/mtps*
%{_sysconfdir}/dnf/protected.d/mini-tps.conf
%{_datarootdir}/mini-tps/*
%{_libexecdir}/mini-tps/*

%changelog
* Fri Nov 24 2023 Jiri Popelka <jpopelka@redhat.com> - 0.1-162
- URL update

* Mon Jul 31 2023 Andrei Stepanov <astepano@redhat.com> - 0.1-161
- new build

* Fri Jul 28 2023 Michal Srb <michal@redhat.com> - 0.1-160
- Add profiles for Fedora

* Wed Jul 26 2023 Michal Srb <michal@redhat.com> - 0.1-159
- Add option to rpm-verify installed packages (OSCI-1240)

* Wed Mar 29 2023 Michal Srb <michal@redhat.com> - 0.1-158
- Ignore known scriptlet false positives

* Wed Mar 29 2023 Michal Srb <michal@redhat.com> - 0.1-157
- Add HTML result viewer

* Wed Mar 08 2023 Michal Srb <michal@redhat.com> - 0.1-156
- Add option to check for problems in scriptlet outputs (OSCI-1230)

* Wed Feb 08 2023 Michal Srb <michal@redhat.com> - 0.1-155
- Add flatpak repos for RHEL 9

* Tue Jan 17 2023 Andrei Stepanov <astepano@redhat.com> - 0.1-154
- Build with the latest merged PRs.

* Sun Dec 04 2022 Andrei Stepanov <astepano@redhat.com> - 0.1-153
- Build with the latest merged PRs.

* Tue Oct 25 2022 Michal Srb <michal@redhat.com> - 0.1-152
- Add support for scratch builds

* Tue Sep 13 2022 Michal Srb <michal@redhat.com> - 0.1-151
- Add profile for CentOS Stream 9

* Fri Sep 09 2022 Michal Srb <michal@redhat.com> - 0.1-150
- Make profiles configurable for different operating systems.

* Tue Sep 06 2022 Michal Srb <michal@redhat.com> - 0.1-149
- Fix --onlyinrepo option in mtps-get-task.

* Wed Oct 13 2021 Michal Srb <michal@redhat.com> - 0.1-145
- Build with the latest changes.

* Tue Feb 02 2021 Andrei Stepanov <astepano@redhat.com> - 0.1-144
- Build with the latest changes.

* Tue Feb 02 2021 Andrei Stepanov <astepano@redhat.com> - 0.1-143
- Build with the latest changes.

* Mon Jan 25 2021 Andrei Stepanov <astepano@redhat.com> - 0.1-142
- Build with the latest changes.

* Mon Jan 25 2021 Andrei Stepanov <astepano@redhat.com> - 0.1-141
- Build with the latest changes.

* Mon Jan 18 2021 Andrei Stepanov <astepano@redhat.com> - 0.1-140
- Build with the latest changes.

* Thu Jun 25 2020 Andrei Stepanov <astepano@redhat.com> - 0.1-139
- Build with the latest merged PRs.
