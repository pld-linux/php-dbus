#
# Conditional build:
%bcond_without	tests		# build without tests

%define		svnrev	1
%define		rel		0.1
%define		modname	dbus
Summary:	DBus binding for PHP
Name:		php-%{modname}
Version:	1.0
Release:	0.svn%{svnrev}.%{rel}
License:	New BSD License
Group:		Development/Languages/PHP
# revno=
# svn co http://php-dbus.googlecode.com/svn/trunk${revno:+@$revno} php-dbus
# tar -cjf php-dbus-$(svnversion php-dbus).tar.bz2 --exclude-vcs php-dbus
# ../dropin php-dbus-$(svnversion php-dbus).tar.bz2
Source0:	%{name}-%{svnrev}.tar.bz2
# Source0-md5:	bc29a6add663ae977fde560175ccf306
URL:		http://code.google.com/p/php-dbus/
BuildRequires:	dbus-devel
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.519
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-Bus is a message bus system, a simple way for applications to talk
to one another. In addition to interprocess communication, D-Bus helps
coordinate process lifecycle; it makes it simple and reliable to code
a "single instance" application or daemon, and to launch applications
and daemons on demand when their services are needed.

php-dbus is a binding of PHP and DBus.

%prep
%setup -qn %{name}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
