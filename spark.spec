%define debug_package %{nil}
# define _unpackaged_files_terminate_build 0
# disable repacking jars
%define __os_install_post %{nil}
%global initd_dir %{_sysconfdir}/rc.d/init.d

Name:       spark
Version:    %{VERSION}
Release:    1%{?dist}
Summary:    Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.
Group:      Applications/Internet
License:    Apache 2.0
URL:        https://spark.apache.org/
Source0:    %{name}-%{version}-bin-hadoop3.2.tgz
BuildRoot:  %{_tmppath}/apache-%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:   Shuaipeng Lee <lishuaipeng651@gmail.com>

AutoReqProv: no

%description
Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.


%prep
%setup -q -n %{name}-%{version}-bin-hadoop3.2

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 0755 %{buildroot}
%{__install} -d -m 0755 %{buildroot}/usr/lib/%{name}3
%{__install} -d -m 0755 %{buildroot}/var/lib/%{name}3
%{__install} -d -m 0755 %{buildroot}/var/log/%{name}3
%{__install} -d -m 0755 %{buildroot}/var/run/%{name}3
%{__install} -d -m 0755 %{buildroot}/etc/%{name}3

%{__cp} -rp ./* %{buildroot}/usr/lib/%{name}3

%{__rm} %{buildroot}/usr/lib/%{name}3/jars/hadoop-client-api-3.3.1.jar

%{__cp} %{_sourcedir}/hadoop-client-api-3.3.1.jar %{buildroot}/usr/lib/%{name}3/jars/

ln -s -r %{buildroot}/usr/lib/%{name}3/conf  %{buildroot}/etc/%{name}3/


%pre
if ! /usr/bin/id spark &>/dev/null; then
    /usr/sbin/useradd -r -d /var/lib/spark -s /bin/sh -c "spark" spark || \
        %logmsg "Unexpected error adding user \"spark\". Aborting installation."
    # /sbin/usermod -a -G hadoop dolphinscheduler
fi

%post
systemctl daemon-reload

%preun

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel spark || %logmsg "User \"spark\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-,root,root,755)
/usr/lib/%{name}3
/var/lib/%{name}3
/var/log/%{name}3
/var/run/%{name}3
/etc/%{name}3