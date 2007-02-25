#
# Conditional build
%bcond_with	bytecode	# use bytecode hinting instead of autohinting by default
%define		_realname   fontconfig
Summary:	Font configuration and customization tools - cross Mingw32 versoin
Summary(pl.UTF-8):Narzędzia do konfigurowania fontów - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Ferramentas para configuração e customização do acesso a fontes
Name:		crossmingw32-%{_realname}
Version:	2.4.2
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{_realname}-%{version}.tar.gz
# Source0-md5:	f035852f521b54677f2b5c9e2f6d54a4
Patch0:		%{name}-dll.patch
Patch1:		%{_realname}-blacklist.patch
Patch2:		%{_realname}-autohint.patch
Patch3:		%{_realname}-bitstream-cyberbit.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-expat
BuildRequires:	crossmingw32-freetype >= 2.1.5
BuildRequires:	crossmingw32-pkgconfig
Requires:	crossmingw32-freetype >= 2.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_aclocaldir		%{_datadir}/aclocal
%define		_pkgconfigdir		%{_libdir}/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains tools and documentation.

%description -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

Paket ten zawiera programy narzędziowe i dokumentację.

%description -l pt_BR.UTF-8
Fontconfig é uma biblioteca para configuração e customização do
acesso a fontes.

Este pacote contém as ferramentas e documentação.

%prep
%setup -q -n %{_realname}-%{version}
#%patch0 -p1
%patch1 -p1
%if %{with bytecode}
%patch2 -p1
%endif
%patch3 -p1

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--with-arch=%{target} \
	--disable-docs

#%{__sed} -i -e 's/^deplibs_check_method=.*/deplibs_check_method="pass_all"/' libtool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{1,3,5},/var/cache/fontconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -f conf.d/README README.confd

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
# Is this needed?
#HOME=/tmp %{_bindir}/fc-cache -f 2>/dev/null || :

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.confd
#%dir %{_sysconfdir}/fonts
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/fonts.conf
#%{_sysconfdir}/fonts/fonts.dtd
#%dir %{_sysconfdir}/fonts/conf.avail
#%{_sysconfdir}/fonts/conf.avail/*.conf
#%{_sysconfdir}/fonts/conf.avail/README
#%dir %{_sysconfdir}/fonts/conf.d
#%config(noreplace,missingok) %verify(not link md5 mtime size) %{_sysconfdir}/fonts/conf.d/*.conf
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_bindir}/*.dll
%dir %{_includedir}/fontconfig
%{_includedir}/fontconfig/*.h
%{_pkgconfigdir}/fontconfig.pc
