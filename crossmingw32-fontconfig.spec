%define		realname   fontconfig
Summary:	Font configuration and customization tools - cross MinGW32 versoin
Summary(pl.UTF-8):	Narzędzia do konfigurowania fontów - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.10.2
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://fontconfig.org/release/%{realname}-%{version}.tar.gz
# Source0-md5:	025e08b3d7fe45c433de5718e441ed15
Patch0:		%{realname}-blacklist.patch
Patch1:		%{realname}-bitstream-cyberbit.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	crossmingw32-expat
BuildRequires:	crossmingw32-freetype >= 2.1.5
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-expat
Requires:	crossmingw32-freetype >= 2.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

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
Requires:	crossmingw32-freetype-dll >= 2.1.5
Requires:	wine

%description dll
DLL freetype library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL freetype dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--with-arch=%{target} \
	--with-freetype-config="pkg-config freetype2" \
	--disable-docs \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# runtime
%{__rm} -r $RPM_BUILD_ROOT/etc/fonts \
	$RPM_BUILD_ROOT%{_datadir}/{fontconfig,xml/fontconfig}

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