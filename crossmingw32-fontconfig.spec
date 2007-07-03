#
%define		_realname   fontconfig
Summary:	Font configuration and customization tools - cross Mingw32 versoin
Summary(pl.UTF-8):	Narzędzia do konfigurowania fontów - wersja skrośna dla Mingw32
Name:		crossmingw32-%{_realname}
Version:	2.4.2
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://fontconfig.org/release/%{_realname}-%{version}.tar.gz
# Source0-md5:	f035852f521b54677f2b5c9e2f6d54a4
Patch0:		%{_realname}-blacklist.patch
Patch1:		%{_realname}-bitstream-cyberbit.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-expat
BuildRequires:	crossmingw32-freetype >= 2.1.5
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	crossmingw32-expat
Requires:	crossmingw32-freetype >= 2.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_libdir}/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

Paket ten zawiera wersję skrośną dla Win32.

%package static
Summary:	Static freetype library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka freetype (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static freetype library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka freetype (wersja skrośna mingw32).

%package dll
Summary:	DLL freetype library for Windows
Summary(pl.UTF-8):	Biblioteka DLL freetype dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-expat-dll
Requires:	crossmingw32-freetype-dll >= 2.1.5
Requires:	wine

%description dll
DLL freetype library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL freetype dla Windows.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1
%patch1 -p1

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

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/man
# runtime
rm -rf $RPM_BUILD_ROOT/etc/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libfontconfig.dll.a
%{_libdir}/libfontconfig.la
%{_libdir}/fontconfig.def
%dir %{_includedir}/fontconfig
%{_includedir}/fontconfig/*.h
%{_pkgconfigdir}/fontconfig.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfontconfig.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libfontconfig-*.dll
