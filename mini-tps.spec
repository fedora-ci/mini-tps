Name: mini-tps
Version: 0.1
Release: 148%{?dist}
Summary: Mini TPS - Test Package Sanity

License: GPLv2
URL: https://gitlab.cee.redhat.com/osci/mini-tps
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
%setup -n %{name}

%build

%install
mkdir -p %{buildroot}%{_prefix}/local/bin/
cp -rfp mtps* %{buildroot}%{_prefix}/local/bin/
mkdir -p %{buildroot}%{_sysconfdir}/dnf/protected.d
cp -pf mini-tps.conf %{buildroot}%{_sysconfdir}/dnf/protected.d/
mkdir -p %{buildroot}%{_datarootdir}/mini-tps/profiles
cp -rfp profiles/*.repo %{buildroot}%{_datarootdir}/mini-tps/profiles
mkdir -p %{buildroot}%{_datarootdir}/mini-tps/optrepos
cp -rfp optrepos/*.repo %{buildroot}%{_datarootdir}/mini-tps/optrepos

%files
%{_prefix}/local/bin/mtps*
%{_sysconfdir}/dnf/protected.d/mini-tps.conf
%{_datarootdir}/mini-tps/*

%changelog
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
