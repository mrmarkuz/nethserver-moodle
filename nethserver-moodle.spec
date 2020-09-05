Name: nethserver-moodle
Summary: Moodle integration in NethServer
Version: 0.1.3
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: https://download.moodle.org/download.php/direct/stable39/moodle-latest-39.tgz
Source2: https://moodle.org/plugins/download.php/21420/moosh_moodle38_2020042300.zip
BuildArch: noarch

BuildRequires: nethserver-devtools

Requires: rh-php73-php-fpm, rh-php73-php-mysqlnd, rh-php73-php-gd, nethserver-rh-mariadb103
Requires: rh-php73-php-intl, rh-php73-php-mbstring, rh-php73-php-xmlrpc
Requires: rh-php73-php-soap, rh-php73-php-opcache, rh-php73-php-ldap, nethserver-rh-php73-php-fpm
Requires: nethserver-httpd

AutoReqProv: no

#%define _strip_opts --debuginfo -x "mimetex*"
#%define debug_package %{nil}
#%define _binaries_in_noarch_packages_terminate_build 0
#%define _unpackaged_files_terminate_build 0
#%undefine _missing_build_ids_terminate_build
#%define __requires_exclude ^perl(\s|)\(.*\)$

%description
This package provides NethServer templates and actions needed to
integrate Moodle learning platform in NethServer.

%prep
%setup

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/var/lib/nethserver/moodledata

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar -xzf %{SOURCE1} -C %{buildroot}/usr/share/
unzip %{SOURCE2} -d %{buildroot}/usr/share/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/

%{genfilelist} %{buildroot} \
  --file /etc/sudoers.d/50_nsapi_nethserver_moodle 'attr(0440,root,root)' \
  --file /usr/libexec/nethserver/api/%{name}/read 'attr(775,root,root)' \
  --dir /var/lib/nethserver/moodledata 'attr(0770,apache,apache)' | grep -v /usr/share/moodle | grep -v /usr/share/moosh \
> %{name}-%{version}-filelist

exit 0

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-update
%dir /usr/share/moodle/ %attr(0755,root,root)
%attr(755,root,root) /usr/share/moodle/*
/etc/e-smith/events/nethserver-moodle-update/templates2expand/usr/share/moodle/config.php
/etc/e-smith/templates/usr/share/moodle/config.php/10base
/etc/e-smith/templates/usr/share/moodle/config.php/template-begin
/usr/share/moodle/.eslintignore
/usr/share/moodle/.eslintrc
/usr/share/moodle/.gherkin-lintrc
/usr/share/moodle/.gitattributes
/usr/share/moodle/.github/FUNDING.yml
/usr/share/moodle/.jshintignore
/usr/share/moodle/.jshintrc
/usr/share/moodle/.nvmrc
/usr/share/moodle/.shifter.json
/usr/share/moodle/.stylelintignore
/usr/share/moodle/.stylelintrc
/usr/share/moodle/.travis.yml

%dir /usr/share/moosh/ %attr(0755,root,root)
%attr(755,root,root) /usr/share/moosh/*

%changelog
* Sat Sep 05 2020 mrmarkuz <31746411+mrmarkuz@users.noreply.github.com> - 0.1.3-1
  - Add theme and mod dirs to backup
  - Preconfigure LDAP
  - Fix installation routine and add app button
  - Update to Moodle 3.9

* Fri Sep 04 2020 Markus Neuberger <dev@markusneuberger.at> - 0.1.2-3
- Update to moodle 3.9 LTS
- Include moosh
- Preconfigure AD/LDAP plugin

* Sat Apr 18 2020 Markus Neuberger <dev@markusneuberger.at> - 0.1.2-2
- Update to moodle 3.8

* Sat Dec 08 2018 Markus Neuberger <dev@markusneuberger.at> - 0.1.2-1
- Update to moodle 3.5

* Sun Mar 4 2018 Markus Neuberger <dev@markusneuberger.at> - 0.1.0-1
- Change to moodle 3.4
- Download tgz via source1 instead of epel requirement
- Change location to /usr/share/moodle and data to /var/lib/nethserver/moodledata
- Update mysql collation

* Wed Dec 7 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.9-1
- Add support to both alias and virtualhost configuration
- Update README.srt file to describe recent changes

* Tue Nov 29 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.7-1
- Update actions to expand moodle configuration files
- Remove empty line from final config.php file

* Mon Nov 28 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.6-1
- Add a property to restrict to the LAN if wanted
- Add moodle dependencies not included in moodle spec itself

* Sun Nov 27 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.5-1
- Remove /var/lib/nethserver/moodle directory
- Remove sudoers.d reference from package spec
- Remove 90_nethserver_moodle from sudoers.d
- Remove config.php from backup-data.d/moodle.include
- Automate password setting in config.php template

* Sun Nov 27 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.4-1
- Update README.rst
- Consider README.rst a documentation file

* Sat Nov 26 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.3-1
- Fix template header in config.php
- Remove duplicated php opening tag from final config.php file
- Remove ^M characters from config.php file
- Update config.php to use https instead of http as value to wwwroot

* Sat Nov 26 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.2-1
- Fix access control in moodle.conf
- Fix moodle's module class name definition

* Fri Nov 25 2016 Alain Reguera Delgado <alain.reguera@gmail.com> - 0.0.1-1
- Initial build.
