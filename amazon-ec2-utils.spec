Name:      amazon-ec2-utils
Summary:   A set of tools for running in EC2
Version:   2.1.0
Release:   1%{?dist}
License:   MIT
Group:     System Tools

Source0:   ec2-metadata
Source1:   ec2udev-vbd
Source2:   51-ec2-hvm-devices.rules
Source16:  60-cdrom_id.rules
Source22:  70-ec2-nvme-devices.rules
Source23:  ec2nvme-nsid
Source24:  ebsnvme-id
Source25:  51-ec2-xen-vbd-devices.rules
Source26:  53-ec2-read-ahead-kb.rules

URL:       https://github.com/aws/amazon-ec2-utils
BuildArch: noarch
Provides:  ec2-utils = %{version}-%{release}
Obsoletes: ec2-utils < 2.1
Provides:  ec2-metadata = %{version}-%{release}
Obsoletes: ec2-metadata <= 0.1
Requires:  curl
Requires:  python3
BuildRequires: python3-devel
BuildRequires: systemd-rpm-macros
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
amazon-ec2-utils contains a set of utilities for running in ec2.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_udevrulesdir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/

install -m755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sbindir}
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_udevrulesdir}
install -m644 %{SOURCE25} $RPM_BUILD_ROOT%{_udevrulesdir}
install -m644 %{SOURCE26} $RPM_BUILD_ROOT%{_udevrulesdir}
# Install 60-cdrom_id.rules to /etc rather than %{_udevrulesdir}
# because it is intended as an override of a systemd-provided rules
# file:
install -m644 %{SOURCE16} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/

#udev rules for nvme block devices and supporting scripts
install -m644 %{SOURCE22} $RPM_BUILD_ROOT%{_udevrulesdir}
install -m755 %{SOURCE23} $RPM_BUILD_ROOT%{_sbindir}/ec2nvme-nsid
install -m755 %{SOURCE24} $RPM_BUILD_ROOT/%{_sbindir}

%check
%{python3} -m py_compile %{SOURCE24}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/ec2-metadata
%{_sbindir}/ec2nvme-nsid
%{_sbindir}/ebsnvme-id
%{_sbindir}/ec2udev-vbd
/usr/lib/udev/rules.d/51-ec2-hvm-devices.rules
/usr/lib/udev/rules.d/51-ec2-xen-vbd-devices.rules
/usr/lib/udev/rules.d/53-ec2-read-ahead-kb.rules
/usr/lib/udev/rules.d/70-ec2-nvme-devices.rules
/etc/udev/rules.d/60-cdrom_id.rules

%changelog

* Thu Apr  6 2023 Noah Meyerhans <nmeyerha@amazon.com> - 2.1.0-1
- Add --quiet option to ec2-metadata
- Add --partition support to ec2-metadata

* Fri Feb 11 2022 Noah Meyerhans <nmeyerha@amazon.com> 2.0.1-1
- Don't lose NVME symlinks on udev change events

* Thu Jan 20 2022 Noah Meyerhans <nmeyerha@amazon.com> 2.0-1
- Update to 2.0
- Update python dependencies to python3
- Install udev rules to %{_udevrulesdir} rather than a hardcoded /etc/udev
  location.
- Install binaries to %{_sbindir} rather than hardcoded /sbin
- Move ec2nvme-nsid to /usr/sbin rather than /usr/lib/udev
- Drop ec2udev-vpcu and related udev rules
- Fix an invalid substitution in 53-ec2-read-ahead-kb.rules
- Drop the /opt/aws/bin/ec2-metadata symlink

* Wed Nov 17 2021 Noah Meyerhans <nmeyerha@amazon.com> 1.3-5
- Restrict NVME udev rules to "add" events

* Wed Nov 17 2021 Hailey Mothershead <hailmo@amazon.com> 1.3-4
- Add udev rule to increase read_ahead_kb when an NFS share is mounted

* Wed Jul 14 2021 Sai Harsha <ssuryad@amazon.com> 1.3-3
- Disable timeout on EBS volumes

* Thu Oct 29 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-2
- Add testing of python syntax to spec file

* Mon May 18 2020 Suraj Jitindar Singh <surajjs@amazon.com> 1.3-1
- Add udev rule to add by-path links for xen vbd devices

* Tue Apr 28 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-1
- Rename the project to amazon-ec2-utils
- Add README file

* Tue Feb 25 2020 Frederick Lefebvre <fredlef@amazon.com> 1.2-1
- Fix output of multi-line fields

* Wed Jan 15 2020 Frederick Lefebvre <fredlef@amazon.com> 1.1-1
- Add IMDSv2 support

* Tue Aug 27 2019 Anchal Agarwal <anchalag@amazon.com> 1.0-2
- Add udev rule to define lower timeout for instance storage volumes

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
