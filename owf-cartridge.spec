%global cartridgedir %{_libexecdir}/openshift/cartridges/v2/owf/

Summary:       Provides OWF support for OpenShift
Name:          owf-cartridge
Version: 0.8.19
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://www.shadow-soft.com
Source0:       https://github.com/Shadow-Soft/owf-cartridge
Requires:      rubygem(openshift-origin-node)
Requires:      openshift-origin-cartridge-jbossews
Requires:      openshift-origin-cartridge-postgresql
%if 0%{?rhel}
Requires:      maven3
%endif
%if 0%{?fedora}
Requires:      maven
%endif
BuildRequires: jpackage-utils
BuildArch:     noarch

%description
Provides the Ozone Widget Framework on  OpenShift. (Cartridge Format V2)

%prep
%setup -q

%build
%__rm %{name}.spec

%install
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}

%post
# To modify an alternative you should:
# - remove the previous version if it's no longer valid
# - install the new version with an increased priority
# - set the new version as the default to be safe

%if 0%{?rhel}
alternatives --install /etc/alternatives/maven-3.0 maven-3.0 /usr/share/java/apache-maven-3.0.3 100
alternatives --set maven-3.0 /usr/share/java/apache-maven-3.0.3
%endif

%if 0%{?fedora}
alternatives --remove maven-3.0 /usr/share/java/apache-maven-3.0.3
alternatives --install /etc/alternatives/maven-3.0 maven-3.0 /usr/share/maven 102
alternatives --set maven-3.0 /usr/share/maven
%endif

/usr/sbin/oo-admin-cartridge --action install -R -s %{cartridgedir}../
if [ -f /usr/sbin/oo-admin-broker-cache ]
then
    echo "clearing broker cache"
    /usr/sbin/oo-admin-broker-cache --clear --console
fi

%postun
/usr/sbin/oo-admin-cartridge --action erase --name owf --version 7.0 --cartridge_version 0.0.1
if [ -f /usr/sbin/oo-admin-broker-cache ]
then
    echo "clearing broker cache"
    /usr/sbin/oo-admin-broker-cache --clear --console
fi

%files
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%attr(0755,-,-) %{cartridgedir}/hooks/
%{cartridgedir}
%doc %{cartridgedir}/README.md
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Fri Feb 14 2014 Bret Frederick <bret.frederick@patvmackinc.com> 0.8.19-1
- add owf.war back in (bret.frederick@patvmackinc.com)
- changed manifest source url to point to the owf-cartridge location (was owf-
  widget-cartridge location) (bret.frederick@patvmackinc.com)

* Fri Feb 14 2014 Bret Frederick <bret.frederick@patvmackinc.com> 0.8.18-1
- put owf.war back in.  changed manifest source url to point to the owf-
  cartridge location (was owf-widget-cartridge location)
  (bret.frederick@patvmackinc.com)
- Update (matt@intelligentgeek.com)
- Re-initialize repository (matt@intelligentgeek.com)


