Summary:	OpenSP - SGML parser
Summary(pl):	OpenSP - parser SGML
%define	arname	OpenSP
Name:		opensp
Version:	1.5.1
Release:	3
Epoch:		1
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	http://dl.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
# Source0-md5:	f46fe0a04b76a4454ec27b7fcc84ec54
Patch0:		%{name}-nolibnsl.patch
Patch1:		%{name}-localedir.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool >= 2:1.4d
Requires:	sgml-common >= 0.5-1
Provides:	sgmlparser
Provides:	sp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	openjade <= 1.3-1
Obsoletes:	sp

%define		sgmldir		/usr/share/sgml
%define		_datadir	%{sgmldir}

%description
Package contains an SGML parser.

%description -l pl
pakiet zawiera parser SGML.

%package devel
Summary:	OpenSP header files
Summary(pl):	Pliki nag³ówkowe OpenSP
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
OpenSP header files and devel documentation.

%description devel -l pl
Pliki nag³ówkowe OpenSP.

%package static
Summary:	Static OpenSP libraries
Summary(pl):	Biblioteki statyczne OpenSP
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static OpenSP libraries.

%description static -l pl
Biblioteki statyczne OpenSP.

%prep
%setup -q -n %{arname}-%{version}
%patch0 -p1
%patch1 -p1

%build
#please don't run gettextize --copy --force
if [ ! -f po/LINGUAS ] ; then
	ls po/*.po |sed 's=po/\(.*\).po=\1=' > po/LINGUAS
fi
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-default-catalog=%{_sysconfdir}/sgml/catalog \
	--enable-default-search-path=%{sgmldir} \
	--enable-http

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgdocdir=%{_defaultdocdir}/%{name}-%{version}

for i in nsgmls sgmlnorm spam spcat spent; do
	ln -sf o$i $RPM_BUILD_ROOT%{_bindir}/$i
done

# sx conficts with sx from lrzsz package
ln -sf osx $RPM_BUILD_ROOT%{_bindir}/sgml2xml

%find_lang sp4

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f sp4.lang
%defattr(644,root,root,755)
%{_defaultdocdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{sgmldir}/OpenSP
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
