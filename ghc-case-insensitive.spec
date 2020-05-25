#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	case-insensitive
Summary:	Case insensitive string comparison
Summary(pl.UTF-8):	Porównywanie łańcuchów nie wrażliwe na wielkość liter
Name:		ghc-%{pkgname}
Version:	1.2.1.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/case-insensitive
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	c501248804f3aaf4c56e2f16d03c3969
URL:		http://hackage.haskell.org/package/case-insensitive
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-deepseq >= 1.1
BuildRequires:	ghc-hashable >= 1.0
BuildRequires:	ghc-text >= 0.3
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-deepseq-prof >= 1.1
BuildRequires:	ghc-hashable-prof >= 1.0
BuildRequires:	ghc-text-prof >= 0.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-deepseq >= 1.1
Requires:	ghc-hashable >= 1.0
Requires:	ghc-text >= 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The module Data.CaseInsensitive provides the CI type constructor which
can be parameterised by a string-like type like: String, ByteString,
Text, etc.. Comparisons of values of the resulting type will be
insensitive to cases.

%description -l pl.UTF-8
Moduł Data.CaseInsensitive udostępnia konstruktor typu C, który może
być parametryzowany typem typu łańcuchowego, takim jak String,
ByteString, Text itp. Porównywanie wartości typu wynikowego nie będzie
wrażliwe na wielkość liter.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-deepseq-prof >= 1.1
Requires:	ghc-hashable-prof >= 1.0
Requires:	ghc-text-prof >= 0.3

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScase-insensitive-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScase-insensitive-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScase-insensitive-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/CaseInsensitive
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/CaseInsensitive/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/CaseInsensitive/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScase-insensitive-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/CaseInsensitive/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
