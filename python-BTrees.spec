# TODO:
# - fix tests:   ... skipped 'ZODB not available'   , ZODB though depends on BTrees
# - fix docs build

# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	BTrees
%define		pypi_name	%{module}

Summary:	Scalable persistent object containers
Summary(pl.UTF-8):	Skalowalne trwałe kontenery dla obiektów
Name:		python-%{module}
Version:	4.4.1
Release:	7
License:	ZPL 2.1
Group:		Libraries/Python
#Source0:	https://files.pythonhosted.org/packages/source/B/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
#Source0:	https://pypi.python.org/packages/source/B/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:	https://pypi.python.org/packages/6a/e2/d8c2a5b4cbc493b1ccb440d61bf0f62b8a0cb1c7b5aa403d5e18847545b3/BTrees-%{version}.tar.gz
# Source0-md5:	6a0178e30b94cf0cc44ae62e93187ecc
URL:		http://packages.python.org/BTrees
BuildRequires:	rpm-pythonprov
# for the py_build, py_install macros
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-persistent >= 4.0.4
#BuildRequires:	python-setuptools
BuildRequires:	python-transaction
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-persistent >= 4.0.4
#BuildRequires:	python3-setuptools
BuildRequires:	python3-transaction
%endif

# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
%requires_eq	python-persistent
Requires:	python-transaction
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules
%requires_eq	python3-persistent
Requires:	python3-transaction

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%{py_sitedir}/%{module}/*.[ch]
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.[ch]
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
