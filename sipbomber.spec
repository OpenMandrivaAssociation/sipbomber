%define	Summary	A tool for testing SIP-protocol implementation (RFC3261)

Summary:	%{Summary}
Name:		sipbomber
Version:	0.8
Release:	%mkrel 1
License:	GPL
Group:		Networking/Other
URL:		http://www.metalinkltd.com/downloads.php
Source0:	http://metalinkltd.com/wp-content/uploads/%{name}_%{version}.tar.bz2
Patch1:		sipbomber_0.7-testcases_dir.diff
BuildRequires:	libqt-devel

%description
Sipbomber is invaluable tool for SIP developers intended for
testing SIP-protocol implementation against rfc3261. Current
version can check only server implementations - (proxies, user
agent servers, redirect servers, and registrars).

%prep

%setup -q -n %{name}
%patch1 -p0

# lib64 fix
find -type f -name "Makefile" | xargs perl -pi -e "s|/lib\b|/%{_lib}|g"

%build

# Set QTDIR for Bash shell
if [ -z "$QTDIR" ]; then
    export QTDIR="/usr/lib/qt3/"
fi
   
PATH=$PATH:$QTDIR/bin
export PATH
   
%make OPT="%{optflags}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}

install -m0755 sipb_main %{buildroot}%{_bindir}/%{name}
install -m0644 testcases/* %{buildroot}%{_datadir}/%{name}/


install -d %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=SipBomber
Comment=%{Summary}
Exec=%{name}
Icon=development_tools_section
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Development-Tools;
EOF

%post
%update_menus

%postun
%clean_menus

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop


