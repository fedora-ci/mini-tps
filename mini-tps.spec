Name: mini-tps
Version: 0.1
Release: 163%{?dist}
Summary: Mini TPS - Test Package Sanity

License: GPLv2
URL:     https://github.com/fedora-ci/mini-tps
Source0: %{name}.tar.gz
# 'remove' test won't be run for these packages
Requires: yum yum-utils openssh-server
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
mkdir -p %{buildroot}%{_sbindir} # epel7
install -pD -m 0755 --target-directory=%{buildroot}%{_sbindir} mtps-*
mkdir -p %{buildroot}%{_sysconfdir}/dnf/protected.d/
# Make mini-tps (and all packages mini-tps requires) protected (from removal)
echo mini-tps > %{buildroot}%{_sysconfdir}/dnf/protected.d/mini-tps.conf
# viewer
install -pD -m 0755 viewer/generate-result-json %{buildroot}%{_libexecdir}/mini-tps/viewer/generate-result-json
install -pD -m 0644 viewer/viewer.html %{buildroot}%{_datarootdir}/mini-tps/viewer/viewer.html

# profiles
mkdir -p %{buildroot}%{_datarootdir}/mini-tps/profiles/{rhel,centos-stream,fedora}/
cp -rfp profiles/rhel/{repos,optrepos}/ %{buildroot}%{_datarootdir}/mini-tps/profiles/rhel/
cp -rfp profiles/centos-stream/{repos,optrepos}/ %{buildroot}%{_datarootdir}/mini-tps/profiles/centos-stream/
cp -rfp profiles/fedora/repos/ %{buildroot}%{_datarootdir}/mini-tps/profiles/fedora/

# prepare scripts
install -pD -m 0755 profiles/rhel/prepare-system %{buildroot}%{_libexecdir}/mini-tps/rhel/prepare-system
install -pD -m 0755 profiles/centos-stream/prepare-system %{buildroot}%{_libexecdir}/mini-tps/centos-stream/prepare-system
install -pD -m 0755 profiles/fedora/prepare-system %{buildroot}%{_libexecdir}/mini-tps/fedora/prepare-system

%files
%{_sbindir}/mtps-*
%config %{_sysconfdir}/dnf/protected.d/mini-tps.conf
%{_datarootdir}/mini-tps/*
%{_libexecdir}/mini-tps/*


%changelog
* Thu Dec 07 2023 Jiri Popelka <jpopelka@redhat.com> - 0.1-163
- remove the Requires: python-gobject-base

* Fri Nov 24 2023 Jiri Popelka <jpopelka@redhat.com> - 0.1-162
- URL update
- move mtps-* executables from /usr/local/bin/ to /usr/sbin/
- use install instead of mkdir & cp
- mtps-mutils Requires: python-gobject-base

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
