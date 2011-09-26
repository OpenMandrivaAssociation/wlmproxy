%define svnversion g8daae3e

Name: wlmproxy
Summary: wlmproxy is a transparent proxy server for the MSN protocol
Version: 0.1.3
Release: %mkrel 1
License: GPLv3
Group: Monitoring
Source: http://github.com/poetinha/%{name}/tarball/master/%{version}/poetinha-%{name}-v%{version}-0-%{svnversion}.tar.gz
Source1: wlmproxy.sysconfig
Source2: wlmproxy.init
URL:	http://wlmproxy.org
BuildRequires: openssl, boost-static-devel, dolphin-connector, dolphin-connector-devel
%if %{_arch} == i386
BuildRequires: libevent-devel, libxml2_2, libxml2-devel, libevent2
%else
BuildRequires: lib64event-devel, lib64xml2_2, lib64xml2-devel, lib64event2
%endif
BuildRoot: %_tmppath/%{name}-%{version}-buildroot

%description
wlmproxy is a transparent proxy server for the MSN protocol.
It supports all versions of MSNP, from 8 up to 21.

Main Features:

- Access control lists (ACLs)
- The wildcard character * (asterisk) can be used as part of a user identifier
- Wordfilter with regular expressions
- Client version control
- Conversation history
- Automatic user registration
- Group-based rules
- Contact management and presence information
- Disclaimer message
- Policy enforcement notification

%prep
rm -rf %{buildroot}
%setup -q -n poetinha-%{name}-cf05d38/

%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

mkdir -p -m 755 %{buildroot}%{_sysconfdir}/%{name}
mkdir -p -m 755 %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}

install -p -m 755 wlmproxy %{buildroot}%{_sbindir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 744 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
install -p -m 640 wlmproxy.conf %{buildroot}%{_sysconfdir}/%{name}

%pre
getent group wlmproxy >/dev/null || groupadd -r wlmproxy
getent passwd wlmproxy >/dev/null || \
useradd -r -f wlmproxy -d '/' -s /sbin/nologin \ 
    -c 'wlmproxy daemon account' wlmproxy
exit 0

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ]; then
	/sbin/service %{name} stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi
%files
%defattr(-,root,root-)
%doc ChangeLog create_mysql.sql LICENSE README TODO
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%attr(755,wlmproxy,wlmproxy) %dir %{_localstatedir}/run/%{name}
%attr(755,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,wlmproxy) %config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/*

