# TODO: optional ZODB for tests (circular dependency)

# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	BTrees

Summary:	Scalable persistent object containers
Summary(pl.UTF-8):	Skalowalne trwałe kontenery dla obiektów
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.11.3
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/BTrees/
Source0:	https://files.pythonhosted.org/packages/source/B/BTrees/%{module}-%{version}.tar.gz
# Source0-md5:	626347f5d1f9bce09765f58e55b51285
URL:		https://pypi.org/project/BTrees/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-persistent-devel >= 4.1.0
BuildRequires:	python-setuptools
%if %{with tests}
#BuildRequires:	python-ZODB
BuildRequires:	python-persistent >= 4.4.3
BuildRequires:	python-transaction
BuildRequires:	python-zope.interface >= 5.0.0
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-persistent-devel >= 4.1.0
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-ZODB
BuildRequires:	python3-persistent >= 4.4.3
BuildRequires:	python3-transaction
BuildRequires:	python3-zope.interface >= 5.0.0
BuildRequires:	python3-zope.testrunner
%endif
%endif
%if %{with doc}
# already installed package
BuildRequires:	python3-BTrees
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.8
%endif
Requires:	python-modules >= 1:2.7
%requires_eq	python-persistent
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a set of persistent object containers built
around a modified BTree data structure. The trees are optimized for
use inside ZODB's "optimistic concurrency" paradigm, and include
explicit resolution of conflicts detected by that mechanism.

%description -l pl.UTF-8
Ten pakiet zawiera zbiór trwałych kontenerów dla obiektów, zbudowanych
w oparciu o zmodyfikowane struktury danych B-drzewa. Drzewa są
zoptymalizowane pod kątem użycia wewnątrz paradygmatu "optymistycznej
współbieżności" ZODB i zawierają jawne rozwiązywanie konfliktów
wykrytych przez ten mechanizm.

%package -n python3-%{module}
Summary:	Scalable persistent object containers
Summary(pl.UTF-8):	Skalowalne trwałe kontenery dla obiektów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
%requires_eq	python3-persistent

%description -n python3-%{module}
This package contains a set of persistent object containers built
around a modified BTree data structure. The trees are optimized for
use inside ZODB's "optimistic concurrency" paradigm, and include
explicit resolution of conflicts detected by that mechanism.

%description -n python3-%{module} -l pl.UTF-8
Ten pakiet zawiera zbiór trwałych kontenerów dla obiektów, zbudowanych
w oparciu o zmodyfikowane struktury danych B-drzewa. Drzewa są
zoptymalizowane pod kątem użycia wewnątrz paradygmatu "optymistycznej
współbieżności" ZODB i zawierają jawne rozwiązywanie konfliktów
wykrytych przez ten mechanizm.

%package apidocs
Summary:	API documentation for Python BTrees module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona BTrees
Group:		Documentation

%description apidocs
API documentation for Python BTrees module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona BTrees.

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
PYTHONPATH=$(pwd):$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
