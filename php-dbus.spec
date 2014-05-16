#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	dbus
Summary:	DBus binding for PHP
Name:		%{php_name}-%{modname}
Version:	0.1.2
Release:	3
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://labs.gree.jp/data/source/php-dbus-%{version}.tgz
# Source0-md5:	2fc2b92ac805128326ecfa382f6807ab
URL:		http://labs.gree.jp/Top/OpenSource/DBus-en.html
BuildRequires:	%{php_name}-devel >= 4:5.0.4
BuildRequires:	dbus-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.519
%{?requires_php_extension}
Obsoletes:	php-dbus < 0.1.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PHP Dbus is a PHP extension to handle D-Bus functions. This module
provides D-Bus interfaces via PHP classes and enables Inter Porcess
Communication in D-Bus.

%prep
%setup -q -n php-%{modname}-%{version}

%build
phpize
CPPFLAGS="%{rpmcppflags} -DDBUS_API_SUBJECT_TO_CHANGE"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
