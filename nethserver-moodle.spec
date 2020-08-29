Name: nethserver-moodle
Summary: Moodle integration in NethServer
Version: 0.1.2
Release: 3%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: https://download.moodle.org/download.php/direct/stable39/moodle-latest-39.tgz
BuildArch: noarch

BuildRequires: nethserver-devtools

Requires: rh-php73-php-fpm, rh-php73-php-mysqlnd, rh-php73-php-gd, nethserver-rh-mariadb103
Requires: rh-php73-php-intl, rh-php73-php-mbstring, rh-php73-php-xmlrpc
Requires: rh-php73-php-soap, rh-php73-php-opcache, rh-php73-php-ldap, nethserver-rh-php73-php-fpm
#Requires: moodle >= 3.1.2
# Moodle dependencies (not included in moodle spec).
#Requires: php-soap, php-pecl-zendopcache, php-ldap
# NethServer dependencies.
Requires: nethserver-httpd

%description
This package provides NethServer templates and actions needed to
integrate Moodle learning platform in NethServer.

%prep
%setup

%build
perl createlinks

%install
rm -rf %{buildroot}
mkdir -p root/usr/share/moodle
cp %{SOURCE1} root/usr/share/moodle.tgz
rm -rf %{buildroot}
#(cd root/etc/e-smith/templates/usr/share/moodle/config.php/; ln -s /etc/e-smith/templates-default/template-begin-php template-begin)
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING README.rst
%dir %{_nseventsdir}/%{name}-update

%changelog
* Sat August 29 2020 Markus Neuberger <dev@markusneuberger.at> - 0.1.2-3
- Update to moodle 3.9 LTS

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
