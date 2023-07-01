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
%{__install} -d -m 0755 %{buildroot}/usr/bin
%{__install} -d -m 0755 %{buildroot}/usr/lib/%{name}3
%{__install} -d -m 0755 %{buildroot}/usr/lib/%{name}3/standalone-metastore
%{__install} -d -m 0755 %{buildroot}/var/lib/%{name}3
%{__install} -d -m 0755 %{buildroot}/var/log/%{name}3
%{__install} -d -m 0755 %{buildroot}/var/run/%{name}3
%{__install} -d -m 0755 %{buildroot}/etc/%{name}3

%{__cp} -rp ./* %{buildroot}/usr/lib/%{name}3

%{__rm} -rf %{buildroot}/usr/lib/%{name}3/conf
%{__rm} -rf %{buildroot}/usr/lib/%{name}3/python/docs

%{__rm} %{buildroot}/usr/lib/%{name}3/jars/hadoop-client-api-3.3.1.jar
%{__rm} %{buildroot}/usr/lib/%{name}3/jars/spark-hive_2.12-3.2.2.jar

%{__install} -m 0755 %{_sourcedir}/hadoop-client-api-3.3.1.jar %{buildroot}/usr/lib/%{name}3/jars/
%{__install} -m 0755 %{_sourcedir}/spark-hive_2.12-3.2.2.jar %{buildroot}/usr/lib/%{name}3/jars/
%{__install} -m 0755 %{_sourcedir}/standalone-metastore-1.21.2.3.1.0.0-78-hive3.jar %{buildroot}/usr/lib/%{name}3/standalone-metastore

# ln -s -r %{buildroot}/usr/lib/%{name}3/conf  %{buildroot}/etc/%{name}3/
%{__install} -m 0755 %{_sourcedir}/spark3-script-wrapper.sh %{buildroot}/usr/bin 
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/pyspark3
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/spark3-class
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/spark3R
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/spark3-shell
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/spark3-sql
%{__install} -m 0755 %{_sourcedir}/spark3-service %{buildroot}/usr/bin/spark3-submit

%pre
if ! /usr/bin/id spark &>/dev/null; then
    /usr/sbin/useradd -r -d /var/lib/spark -s /bin/sh -c "spark" spark || \
        %logmsg "Unexpected error adding user \"spark\". Aborting installation."
    # /sbin/usermod -a -G hadoop spark
fi

%post

HDP_VERSIONS=`hdp-select versions`
ln -s /etc/spark2/${HDP_VERSIONS}/0 /usr/lib/%{name}3/conf

%preun

%postun

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-,root,root,755)
/usr/bin/pyspark3
/usr/bin/spark3-class
/usr/bin/spark3R
/usr/bin/spark3-shell
/usr/bin/spark3-sql
/usr/bin/spark3-submit
/usr/bin/spark3-script-wrapper.sh
/usr/lib/%{name}3
/var/lib/%{name}3
/var/log/%{name}3
/var/run/%{name}3
/etc/%{name}3