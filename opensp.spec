Summary:	OpenSP -- SGML parser
Summary(pl):	OpenSP -- parser SGML
%define	arname	OpenSP
Name:		opensp
Version:	1.4
Release:	2
Copyright:	Copyright (c) 1999 The OpenJade group (free)
Group:		Applications/Publishing/SGML
Group(pl):	Aplikacje/Publikowanie/SGML
Source0:	http://download.sourceforge.net/openjade/%{arname}-%{version}.tar.gz
Source1:	%{arname}-html.catalog
URL:		http://openjade.sourceforge.net/
Provides:	sgmlparser
Requires:	sgml-common <= 0.2-4
Prereq:		%{_sbindir}/fix-sgml-catalog
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	openjade <= 1.3-1
Obsoletes:	sp

%description
Package contains an SGML parser.

%description -l pl
pakiet zawiera parser SGML.

%package devel
Summary:	OpenSP header files
Summary(pl):	Pliki nag³ówkowe OpenSP
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
OpenSP header files and devel documentation.

%description -l pl devel
Pliki nag³ówkowe OpenSP.

%package static
Summary:	Static OpenSP libraries
Summary(pl):	Biblioteki statyczne OpenSP
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static OpenSP libraries.

%description -l pl static
Biblioteki statyczne OpenSP.

%prep
%setup -q -n %{arname}-%{version}

%build
LDFLAGS="-s"
export LDFLAGS
%configure \
	--enable-default-catalog=%{_datadir}/sgml/CATALOG:%{_prefix}/local/share/sgml/CATALOG:%{_sysconfdir}/sgml.catalog \
	--enable-default-search-path=%{_datadir}/sgml:%{_prefix}/local/share/sgml

make  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/{catalogs,html,%{name}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs/html.cat

make install DESTDIR=$RPM_BUILD_ROOT

cp -a $RPM_BUILD_ROOT%{_datadir}/%{arname}/* $RPM_BUILD_ROOT%{_datadir}/sgml/html/

# I don't want to have it in docs
rm -f doc/Makefile*

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

gzip -9nf AUTHORS COPYING ChangeLog NEWS README TODO

%post   
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog

%postun 
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc AUTHORS.gz COPYING.gz ChangeLog.gz NEWS.gz README.gz TODO.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sgml/html
%{_datadir}/sgml/catalogs/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%attr(644,root,root) %{_libdir}/lib*.a
