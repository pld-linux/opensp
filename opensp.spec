Summary:	OpenSP -- SGML parser
Summary(pl):	OpenSP -- parser SGML
%define	arname	OpenSP
Name:		opensp
Version:	1.5
Release:	1
Epoch:		1
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	http://download.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
URL:		http://openjade.sourceforge.net/
Requires:	sgml-common >= 0.5-1
Provides:	sgmlparser
Provides:	sp
BuildRequires:	gettext-devel
BuildRequires:	autoconf
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
Requires:	%{name} = %{version}

%description devel
OpenSP header files and devel documentation.

%description devel -l pl
Pliki nagłówkowe OpenSP.

%package static
Summary:	Static OpenSP libraries
Summary(pl):	Biblioteki statyczne OpenSP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static OpenSP libraries.

%description static -l pl
Biblioteki statyczne OpenSP.

%prep
%setup -q -n %{arname}-%{version}

%build
#please don't run gettextize --copy --force
#autoconf
if [ ! -f po/LINGUAS ] ; then
	ls po/*.po |sed 's=po/\(.*\).po=\1=' > po/LINGUAS
fi
%configure \
	--enable-default-catalog=%{_sysconfdir}/sgml/catalog \
	--enable-default-search-path=%{_datadir}/sgml \
	--datadir=%{_datadir}/sgml \
	--enable-http 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	pkgdocdir=%{_defaultdocdir}/%{name}-%{version}

for i in nsgmls sgmlnorm spam spcat spent; do
	ln -sf o$i $RPM_BUILD_ROOT%{_bindir}/$i
done

# sx conficts with sx from lrzsz package
ln -sf osx $RPM_BUILD_ROOT%{_bindir}/sgml2xml

%find_lang sp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f sp.lang
%defattr(644,root,root,755)
%{_defaultdocdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sgml/OpenSP
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
