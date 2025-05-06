# TODO: optional ZODB for tests (circular dependency)

# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	BTrees

Summary:	Scalable persistent object containers
Summary(pl.UTF-8):	Skalowalne trwałe kontenery dla obiektów
Name:		python3-%{module}
Version:	6.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/btrees/
Source0:	https://files.pythonhosted.org/packages/source/B/BTrees/btrees-%{version}.tar.gz
# Source0-md5:	ab57ba07f73fc5b977421719218649f6
URL:		https://pypi.org/project/BTrees/
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-persistent-devel >= 4.1.0
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-ZODB
BuildRequires:	python3-persistent >= 4.4.3
BuildRequires:	python3-transaction
BuildRequires:	python3-zope.interface >= 5.0.0
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
# already installed package
BuildRequires:	python3-BTrees
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.8
%endif
Requires:	python3-modules >= 1:3.8
%requires_eq	python3-persistent
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

%package apidocs
Summary:	API documentation for Python BTrees module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona BTrees
Group:		Documentation

%description apidocs
API documentation for Python BTrees module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona BTrees.

%prep
%setup -q -n btrees-%{version}

%build
%py3_build %{?with_tests:test}

%if %{with doc}
PYTHONPATH=$(pwd):$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
