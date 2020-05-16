Summary:	OpenSP - SGML parser
Summary(pl.UTF-8):	OpenSP - parser SGML
Name:		opensp
Version:	1.5.2
Release:	7
Epoch:		2
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	http://downloads.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
# Source0-md5:	670b223c5d12cee40c9137be86b6c39b
Patch0:		%{name}-nolibnsl.patch
Patch1:		%{name}-localedir.patch
Patch2:		%{name}-automake.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.14.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	xmlto
Requires:	sgml-common >= 0.5-1
Provides:	sgmlparser
Provides:	sp
Obsoletes:	sp
Conflicts:	openjade <= 1.3-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sgmldir		/usr/share/sgml
%define		_datadir	%{sgmldir}

%description
This package contains an SGML parser.

%description -l pl.UTF-8
Ten pakiet zawiera parser SGML.

%package devel
Summary:	OpenSP header files
Summary(pl.UTF-8):	Pliki nagłówkowe OpenSP
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}
Requires:	libstdc++-devel

%description devel
OpenSP header files and devel documentation.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenSP.

%package static
Summary:	Static OpenSP libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenSP
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static OpenSP libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenSP.

%prep
%setup -q -n OpenSP-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub .
%configure \
	--enable-default-catalog=%{_sysconfdir}/sgml/catalog \
	--enable-default-search-path=%{sgmldir} \
	--enable-http

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_prefix}/share/locale \
	pkgdocdir=%{_docdir}/%{name}-%{version}

# tidy@mozilla-firefox
install -d $RPM_BUILD_ROOT%{_includedir}/OpenSP/nsgmls
install nsgmls/NsgmlsMessages.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/nsgmls
install -d $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Parser.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/ParserState.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Undo.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/EventQueue.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Id.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/OutputState.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Recognizer.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/LpdEntityRef.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/events.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Trie.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib
install lib/Priority.h $RPM_BUILD_ROOT%{_includedir}/OpenSP/lib

for i in nsgmls sgmlnorm spam spcat spent; do
	ln -sf o$i $RPM_BUILD_ROOT%{_bindir}/$i
done

# sx conficts with sx from lrzsz package
ln -sf osx $RPM_BUILD_ROOT%{_bindir}/sgml2xml

%find_lang sp5

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f sp5.lang
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/nsgmls
%attr(755,root,root) %{_bindir}/onsgmls
%attr(755,root,root) %{_bindir}/osgmlnorm
%attr(755,root,root) %{_bindir}/ospam
%attr(755,root,root) %{_bindir}/ospcat
%attr(755,root,root) %{_bindir}/ospent
%attr(755,root,root) %{_bindir}/osx
%attr(755,root,root) %{_bindir}/sgml2xml
%attr(755,root,root) %{_bindir}/sgmlnorm
%attr(755,root,root) %{_bindir}/spam
%attr(755,root,root) %{_bindir}/spcat
%attr(755,root,root) %{_bindir}/spent
%attr(755,root,root) %{_libdir}/libosp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosp.so.5
%{_datadir}/OpenSP
%{_mandir}/man1/onsgmls.1*
%{_mandir}/man1/osgmlnorm.1*
%{_mandir}/man1/ospam.1*
%{_mandir}/man1/ospcat.1*
%{_mandir}/man1/ospent.1*
%{_mandir}/man1/osx.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/libosp.so
%{_libdir}/libosp.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libosp.a
