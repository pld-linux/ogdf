# TODO: system Coin (CoinUtils/Clp/Osi/OsiClp)
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Open Graph Drawing Framework / Open Graph algorithms and Data structures Framework
Summary(pl.UTF-8):	Otwarty szkielet algorytmów i struktur dla grafów
Name:		ogdf
Version:	2023.09
Release:	1
License:	GPL v2 or GPL v3 with limited linking exceptions
Group:		Libraries
#Source0Download: https://github.com/ogdf/ogdf/releases
Source0:	https://github.com/ogdf/ogdf/archive/elderberry-202309/%{name}-elderberry-202309.tar.gz
# Source0-md5:	139100ac0ace53ec9369ed5a375e25cd
Patch0:		%{name}-no-native.patch
Patch1:		%{name}-sse.patch
URL:		https://ogdf.uos.de/
BuildRequires:	CGAL-devel
BuildRequires:	cmake >= 3.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OGDF is a self-contained C++ library for graph algorithms, in
particular for (but not restricted to) automatic graph drawing. It
offers sophisticated algorithms and data structures to use within your
own applications or scientific projects.

%description -l pl.UTF-8
OGDF to samodzielna biblioteka C++ dla algorytmów grafowych, w
szczególności (ale nie tylko) do automatycznego rysowania grafów.
Oferuje wymyślne algorytmy i struktury danych do używania w
aplikacjach lub projektach naukowych.

%package devel
Summary:	Header files for OGDF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OGDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OGDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OGDF.

%package apidocs
Summary:	API documentation for OGDF library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OGDF
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for OGDF library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OGDF.

%prep
%setup -q -n %{name}-elderberry-202309
%patch -P0 -p1
%patch -P1 -p1

%build
install -d build
cd build
%cmake .. \
	-DOGDF_INCLUDE_CGAL=ON

%{__make}

%if %{with apidocs}
cd ../doc
doxygen ogdf-doxygen.cfg
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libogdf/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libCOIN.so
%attr(755,root,root) %{_libdir}/libOGDF.so

%files devel
%defattr(644,root,root,755)
# FIXME: system coin
%{_includedir}/coin
%{_includedir}/ogdf
%{_libdir}/cmake/OGDF
%{_examplesdir}/%{name}-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{search,*.{css,html,js,png}}
%endif
