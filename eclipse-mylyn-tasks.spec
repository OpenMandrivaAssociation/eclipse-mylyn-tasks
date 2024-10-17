%global eclipse_base        %{_libdir}/eclipse
%global install_loc         %{_datadir}/eclipse/dropins
# Taken from update site so we match upstream
#  http://download.eclipse.org/mylyn/archive/3.5.1/v20110422-0200/
%global qualifier           v20110422-0200

Name: eclipse-mylyn-tasks
Summary: Mylyn Bugzilla/Trac Tasks Connectors
Version: 3.5.1
Group:	Development/Java
Release: 4
License: EPL
URL: https://www.eclipse.org/mylyn/tasks

# bash fetch-eclipse-mylyn-tasks.sh
Source0: eclipse-mylyn-tasks-R_3_5_1-fetched-src.tar.bz2
Source1: fetch-eclipse-mylyn-tasks.sh
# Red Hat bugzilla's custom transition file
Source2: redhat-bugzilla-custom-transitions.txt

# These patches are probably not suitable for upstream.
# They switch Import-Package for Bundle-Require in
# bugzilla.core and trac.core MANIFEST.MF
Patch0: %{name}-bugzilla-core-xmlrpc-import-package-manifest-fix.patch
Patch1: %{name}-trac-core-xmlrpc-import-package-manifest-fix.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.5.0
BuildRequires: eclipse-platform >= 0:3.4.0
BuildRequires: eclipse-pde >= 0:3.4.0
BuildRequires: eclipse-mylyn >= 3.5.0
BuildRequires: eclipse-mylyn-commons >= 3.5.0
BuildRequires: eclipse-mylyn-context >= 3.5.0
# The following two are required for webtasks
BuildRequires: rome
BuildRequires: jdom

%description
Mylyn Tasks Connectors


# eclips-mylyn-tasks-bugzilla

%package bugzilla
Summary: Mylyn Tasks Connector: Bugzilla
Requires: eclipse-platform >= 0:3.4.0
Requires: eclipse-mylyn >= 3.5.0
Requires: eclipse-mylyn-commons >= 3.5.0
Provides: eclipse-mylyn-bugzilla = %{version}-%{release}
Obsoletes: eclipse-mylyn-bugzilla < %{version}-%{release}
Group: Development/Java

%description bugzilla
Provides Task List integration, offline support and rich editing for the
open source Bugzilla bug tracker.


# eclips-mylyn-tasks-trac

%package  trac
Summary: Mylyn Tasks Connector: Trac
Requires: eclipse-platform >= 0:3.4.0
Requires: eclipse-mylyn >= 3.5.0
Requires: eclipse-mylyn-commons >= 3.5.0
Requires: eclipse-mylyn-context >= 3.5.0
Group: Development/Java
Provides: eclipse-mylyn-trac = %{version}-%{release}
Obsoletes: eclipse-mylyn-trac < %{version}-%{release}

%description trac
Provides Task List integration, offline support and rich editing
for the open source Trac issue tracker.


# eclips-mylyn-tasks-web

%package  web
Summary: Mylyn Tasks Connector: Web Templates (Advanced) (Incubation)
Requires: eclipse-platform >= 0:3.4.0
Requires: eclipse-mylyn >= 3.5.0
Requires: eclipse-mylyn-commons >= 3.5.0
Requires: rome
Requires: jdom
Group: Development/Java
Provides: eclipse-mylyn-webtasks = %{version}-%{release}
Obsoletes: eclipse-mylyn-webtasks < %{version}-%{release}

%description web
Provides Task List integration for web-based issue trackers
and templates for example projects.


%prep
%setup -q -c
pushd org.eclipse.mylyn.tasks
%patch0
%patch1
popd
pushd org.eclipse.mylyn.incubator
rm -rf orbitDeps
mkdir orbitDeps
pushd orbitDeps
ln -s %{_javadir}/rome-0.9.jar
ln -s %{_javadir}/jdom.jar
popd
popd


%build
pushd org.eclipse.mylyn.tasks
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.bugzilla_feature \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -d "mylyn mylyn-commons"
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.trac_feature \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -d "mylyn mylyn-commons mylyn-context"
popd
pushd org.eclipse.mylyn.incubator
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.mylyn.web.tasks_feature \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier} -DmylynQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \
 -d "mylyn mylyn-commons" -o `pwd`/orbitDeps
popd

%install
install -d -m 755 %{buildroot}%{_datadir}/eclipse
install -d -m 755 %{buildroot}%{install_loc}/mylyn-bugzilla
install -d -m 755 %{buildroot}%{install_loc}/mylyn-trac
install -d -m 755 %{buildroot}%{install_loc}/mylyn-webtasks
install %{SOURCE2} %{buildroot}%{install_loc}/mylyn-bugzilla/redhat-bugzilla-custom-transitions.txt

pushd org.eclipse.mylyn.tasks
unzip -q -o -d %{buildroot}%{install_loc}/mylyn-bugzilla \
 build/rpmBuild/org.eclipse.mylyn.bugzilla_feature.zip
unzip -q -o -d %{buildroot}%{install_loc}/mylyn-trac \
 build/rpmBuild/org.eclipse.mylyn.trac_feature.zip
popd
pushd org.eclipse.mylyn.incubator
unzip -q -o -d %{buildroot}%{install_loc}/mylyn-webtasks \
 build/rpmBuild/org.eclipse.mylyn.web.tasks_feature.zip
popd
pushd %{buildroot}%{install_loc}/mylyn-webtasks/eclipse/plugins
# rome
rm -rf com.sun.syndication*
# jdom
rm -rf org.jdom*
# link to system files instead
ln -s %{_javadir}/rome-0.9.jar
ln -s %{_javadir}/jdom.jar
popd


# eclips-mylyn-tasks-bugzilla

%files bugzilla
%defattr(-,root,root,-)
%{install_loc}/mylyn-bugzilla
%doc org.eclipse.mylyn.tasks/org.eclipse.mylyn.bugzilla-feature/epl-v10.html
%doc org.eclipse.mylyn.tasks/org.eclipse.mylyn.bugzilla-feature/license.html


# eclips-mylyn-tasks-trac

%files trac
%defattr(-,root,root,-)
%{install_loc}/mylyn-trac
%doc org.eclipse.mylyn.tasks/org.eclipse.mylyn.trac-feature/epl-v10.html
%doc org.eclipse.mylyn.tasks/org.eclipse.mylyn.trac-feature/license.html


# eclips-mylyn-tasks-web

%files web
%defattr(-,root,root,-)
%{install_loc}/mylyn-webtasks
%doc org.eclipse.mylyn.incubator/org.eclipse.mylyn.web.tasks-feature/epl-v10.html
%doc org.eclipse.mylyn.incubator/org.eclipse.mylyn.web.tasks-feature/license.html


