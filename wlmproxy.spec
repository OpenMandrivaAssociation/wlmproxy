%define svnversion g8daae3e

Name:		wlmproxy
Summary:	wlmproxy is a transparent proxy server for the MSN protocol
Version:	0.1.3
Release:	6
License:	GPLv3
Group:		Monitoring
Source0:	http://github.com/poetinha/%{name}/tarball/master/%{version}/poetinha-%{name}-v%{version}-0-%{svnversion}.tar.gz
Source1:	wlmproxy.sysconfig
Source2:	wlmproxy.service
Url:		http://wlmproxy.org
BuildRequires:	openssl
BuildRequires:	boost-static-devel
BuildRequires:	dolphin-connector
BuildRequires:	dolphin-connector-devel
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libxml-2.0)

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
%setup -q -n poetinha-%{name}-cf05d38/

%build
%make CXXFLAGS="%{optflags}"

%install
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/%{name}
mkdir -p -m 755 %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}

install -p -m 755 wlmproxy %{buildroot}%{_sbindir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 640 wlmproxy.conf %{buildroot}%{_sysconfdir}/%{name}

sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/%{name}.service

%pre
# % _pre_groupadd %{name}
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /sbin/nologin

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name}
%systemd_postun_with_restart %{name}.service

%files
%doc ChangeLog create_mysql.sql LICENSE README TODO
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(755,wlmproxy,wlmproxy) %dir %{_localstatedir}/run/%{name}
%attr(755,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,wlmproxy) %config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/*

