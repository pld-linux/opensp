Summary:	OpenSP -- SGML parser
Summary(pl):	OpenSP -- parser SGML
%define	arname	OpenSP
Name:		opensp
Version:	1.4
Release:	7
LIcense:	Copyright (c) 1999 The OpenJade group (free)
Group:		Applications/Publishing/SGML
Group(de):	Applikationen/Publizieren/SGML
Group(pl):	Aplikacje/Publikowanie/SGML
Source0:	ftp://download.sourceforge.net/pub/sourceforge/openjade/%{arname}-%{version}.tar.gz
#Source1:	%{arname}-html.catalog
Patch0:		OpenSP-DESTDIR.patch
URL:		http://openjade.sourceforge.net/
Provides:	sgmlparser
Requires:	sgml-common >= 0.2-4
Prereq:		%{_sbindir}/fix-sgml-catalog
Prereq:		/sbin/ldconfig
Provides:	sp
BuildRequires:	gettext-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	openjade <= 1.3-1
Obsoletes:	sp

%description
Package contains an SGML parser.

%description -l pl
pakiet zawiera parser SGML.

%package devel
Summary:	OpenSP header files
Summary(pl):	Pliki nagłówkowe OpenSP
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
OpenSP header files and devel documentation.

%description -l pl devel
Pliki nagłówkowe OpenSP.

%package static
Summary:	Static OpenSP libraries
Summary(pl):	Biblioteki statyczne OpenSP
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static OpenSP libraries.

%description -l pl static
Biblioteki statyczne OpenSP.

%prep
%setup -q -n %{arname}-%{version}
%patch -p1 

%build
#please don't run gettextize --copy --force
%configure \
	--enable-default-catalog=%{_datadir}/sgml/CATALOG:%{_prefix}/local/share/sgml/CATALOG:%{_sysconfdir}/sgml.catalog \
	--enable-default-search-path=%{_datadir}/sgml:%{_prefix}/local/share/sgml

%ifarch alpha
%{__make} CXXFLAGS="%{!?debug:-O0}%{!?debug:-O -g}"
%else
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/{catalogs,html,%{name}}

##install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs/html.cat


%{__make} install DESTDIR=$RPM_BUILD_ROOT

#cp -a $RPM_BUILD_ROOT%{_datadir}/%{arname}/* $RPM_BUILD_ROOT%{_datadir}/sgml/html/

# I removed sx from this list because it conficts with lrzsz package /klakier
for i in nsgmls sgmlnorm spam spcat spent; do
	ln -sf o$i $RPM_BUILD_ROOT%{_bindir}/$i
done

# I don't want to have it in docs
rm -f doc/Makefile*

## what is this???
ln -sf $RPM_BUILD_ROOT%{_bindir}/opensp

gzip -9nf AUTHORS COPYING ChangeLog NEWS README TODO

%find_lang sp

%post   
/sbin/ldconfig
%attr(755,root,root) %{_sbindir}/fix-sgml-catalog

%postun 
/sbin/ldconfig
%attr(755,root,root) %{_sbindir}/fix-sgml-catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files -f sp.lang
%defattr(644,root,root,755)
%doc doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
##%{_datadir}/sgml/html
##%{_datadir}/sgml/catalogs/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
