Summary:	OpenSP -- SGML parser
%define	arname	OpenSP
Name: 		opensp
Version: 	1.4
Release: 	1
Summary(pl):	OpenSP  -- parser SGML
Provides:	sgmlparser
Prereq:		%{_sbindir}/fix-sgml-catalog
Requires: 	sgml-common <= 0.2-4
Conflicts:	openjade <= 1.3-1
URL: 		http://openjade.sourceforge.net/
Source:		http://download.sourceforge.net/openjade/%{arname}-%{version}.tar.gz
Source1:	%{arname}-html.catalog
Copyright:	Copyright (c) 1999 The OpenJade group (free)
BuildRoot: 	/tmp/%{name}-%{version}-root
Group:  	Applications/Publishing/SGML
Group(pl):      Aplikacje/Publikowanie/SGML


%description

%description -l pl


%package devel
Summary:	%{name} header files.
Summary(pl):	Pliki nag³ówkowe %{name}
Requires:	%{name} = %{version}
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description devel

%description -l pl devel


%prep
%setup -q -n %{arname}-%{version}

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-default-catalog=/usr/share/sgml/CATALOG:/usr/local/share/sgml/CATALOG:/etc/sgml.catalog			  			\
	--enable-default-search-path=/usr/share/sgml:/usr/local/share/sgml \


#	--enable-shared 			\
#	--prefix=%{_prefix}			\
#	--datadir=/usr/share/sgml 		\
#	--sharedstatedir=/usr/share/sgml 	\
#	--enable-http 				\
#	--disable-mif				\
#	--enable-html 				\
#	--with-gnu-ld --prefix=/usr 		\

make  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/{catalogs,html,%{name}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs/html.cat

make install DESTDIR=$RPM_BUILD_ROOT

cp -a $RPM_BUILD_ROOT/%{_datadir}/%{arname}/*  $RPM_BUILD_ROOT%{_datadir}/sgml/html/

# I don't want to have it in docs
rm -f doc/Makefile*

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
%attr(755,root,root) %{_libdir}/*.so.*
%{_datadir}/sgml/html
%{_datadir}/sgml/catalogs/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{arname}
%attr(755,root,root) %{_libdir}/*.so
