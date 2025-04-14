%define		realname   fontconfig
Summary:	Font configuration and customization tools - cross MinGW32 version
Summary(pl.UTF-8):	Narzędzia do konfigurowania fontów - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.16.2
Release:	1
License:	MIT
Group:		Development/Libraries
# up to 2.16.0:
#Source0:	https://www.freedesktop.org/software/fontconfig/release/%{realname}-%{version}.tar.xz
# now at gitlab only
#Source0Download: https://gitlab.freedesktop.org/fontconfig/fontconfig/-/releases
Source0:	https://gitlab.freedesktop.org/api/v4/projects/890/packages/generic/fontconfig/%{version}/%{realname}-%{version}.tar.xz
# Source0-md5:	02e32c1b5e4b53b20dce65b3c38014ed
Patch0:		%{realname}-bitstream-cyberbit.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf >= 2.71
BuildRequires:	automake >= 1:1.11
BuildRequires:	crossmingw32-expat
BuildRequires:	crossmingw32-freetype >= 2.9
BuildRequires:	crossmingw32-gcc
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	rpmbuild(macros) >= 2.036
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-expat
Requires:	crossmingw32-freetype >= 2.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_docdir			%{_sysprefix}/share/doc
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
# i486 instructions required for atomic operations
%define		optflags	-O2 -march=i486
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

Paket ten zawiera wersję skrośną dla Win32.

%package static
Summary:	Static freetype library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka freetype (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static freetype library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka freetype (wersja skrośna MinGW32).

%package dll
Summary:	DLL freetype library for Windows
Summary(pl.UTF-8):	Biblioteka DLL freetype dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-expat-dll
Requires:	crossmingw32-freetype-dll >= 2.9
Requires:	wine

%description dll
DLL freetype library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL freetype dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch -P0 -p1

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__gettextize -d po-conf}
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--with-arch=%{target} \
	--disable-docs \
	--disable-silent-rules \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# fc_cachedir=/dummy is to avoid creating ${DESTDIR}LOCAL_APPDATA_FONTCONFIG_CACHE dir
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	fc_cachedir=/dummy

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# runtime
%{__rm} -r $RPM_BUILD_ROOT/etc/fonts \
	$RPM_BUILD_ROOT%{_datadir}/{fontconfig,locale,xml/fontconfig}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/fc-*.exe
# if needed, use ITS data from native package
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gettext/its

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
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
