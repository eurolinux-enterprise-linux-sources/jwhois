%define	name	jwhois
%define	version	4.0
%define	release	1
%define	prefix	/usr

# set to 0 to have jwhois not replace or conflict with the
# system installed whois.
%define provide_whois 1

Summary:	The GNU Whois client
Name:		%{name}
Version:	%{version}
Release:	%{release}
Prefix:		%{prefix}
License:	GPL 
Group:		Applications/Internet
URL:		http://www.gnu.org/software/jwhois
Vendor:		Jonas Oberg <jonas@gnu.org>
Source:		ftp://ftp.gnu.org/gnu/jwhois/%{name}-%{version}.tar.gz
BuildRoot:	/var/tmp/%{name}-%{version}-root
Prereq:		/sbin/install-info
BuildRequires:	gdbm-devel
%{?provide_whois:Obsoletes:	fwhois}

%description
JWHOIS is an Internet Whois client that queries hosts for information
according to RFC 954 - NICNAME/WHOIS. JWHOIS is configured via a
configuration file that contains information about all known Whois servers.
Upon execution, the host to query is selected based on the information
in the configuration file. 

The configuration file is highly customizable and makes heavy use of
regular expressions. 

%prep
%setup -q

%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure --prefix=%{prefix} --sysconfdir=/etc \
	    --enable-GROUP=nobody --localstatedir=/var/cache/jwhois
make

%install
if [ -d ${RPM_BUILD_ROOT} ]; then rm -rf ${RPM_BUILD_ROOT}; fi
make prefix=${RPM_BUILD_ROOT}%{prefix} \
     sysconfdir=${RPM_BUILD_ROOT}/etc install-strip

install -d -m 755 ${RPM_BUILD_ROOT}/etc
install -d -m 755 ${RPM_BUILD_ROOT}/var/cache/jwhois

# Modify and install jwhois.conf
perl -pi -e 's(^#cachefile.*$)(cachefile = "/var/cache/jwhois/jwhois.db";)g; \
	    s(^#cacheexpire.*$)(cacheexpire = 24;)g' example/jwhois.conf
install -m 644 example/jwhois.conf ${RPM_BUILD_ROOT}/etc

%if %{provide_whois}
	ln -s jwhois ${RPM_BUILD_ROOT}%{prefix}/bin/whois
	ln -s jwhois.1 ${RPM_BUILD_ROOT}%{prefix}/man/man1/whois.1
%endif

%clean
if [ -d ${RPM_BUILD_ROOT} ]; then rm -rf ${RPM_BUILD_ROOT}; fi

%pre
[ -f /var/cache/jwhois/jwhois.db ] && rm -f /var/cache/jwhois/jwhois.db

%post
/sbin/install-info %{prefix}/info/jwhois.info %{prefix}/info/dir

%preun 
/sbin/install-info --delete %{prefix}/info/jwhois.info %{prefix}/info/dir
[ -f /var/cache/jwhois/jwhois.db ] && rm -f /var/cache/jwhois/jwhois.db

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%config /etc/jwhois.conf
%attr(6755,nobody,nobody) %{prefix}/bin/jwhois
%{prefix}/man/man1/jwhois.1
%{prefix}/info/jwhois.info
%{prefix}/share/locale/*/LC_MESSAGES/jwhois.mo
%attr(6755,nobody,nobody) /var/cache/jwhois

%if %{provide_whois}
	%{prefix}/bin/whois
	%{prefix}/man/man1/whois.1
%endif

%changelog

