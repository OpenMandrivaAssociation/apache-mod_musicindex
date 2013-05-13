#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_musicindex
%define mod_conf B31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	1.4.0
Release:	2
Group:		System/Servers
License:	LGPLv2.1
URL:		http://hacks.slashdirt.org/musicindex/
Source0:	http://hacks.slashdirt.org/musicindex/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_musicindex-libdir.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRequires:	pkgconfig(flac)
BuildRequires:	id3tag-devel
BuildRequires:	mad-devel
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	libmp4v2-devel
BuildRequires:	mysql-devel

%description
mod_musicindex is an Apache module aimed at being a C alternative to the Perl
module Apache::MP3. It allows nice displaying of directories containing MP3,
Ogg Vorbis, FLAC, or MP4/AAC files, including sorting them on various fields,
streaming/downloading them, constructing playlists, and searching. It also
provides features such as RSS and Podcast feeds, multiple CSS support, and
archive downloads.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

%build
rm -f configure
autoreconf -fi

%configure2_5x --localstatedir=/var/lib \
    --libdir=%{_libdir}

%make 

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

%makeinstall_std 

mv %{buildroot}%{_libdir}/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/

install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%find_lang %{mod_name}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files -f %{mod_name}.lang
%doc AUTHORS COPYING ChangeLog README README.Handlers
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_datadir}/%{mod_name}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-6mdv2012.0
+ Revision: 772692
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-5
+ Revision: 678353
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-4
+ Revision: 645769
- relink against libmysqlclient.so.18

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.3.5-3mdv2011.0
+ Revision: 605223
- Rebuild with apr with workaround to issue with gcc type based

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-2mdv2011.0
+ Revision: 588037
- rebuild

* Sun Oct 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-1mdv2011.0
+ Revision: 584669
- 1.3.5

* Mon Aug 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.4-1mdv2011.0
+ Revision: 568082
- 1.3.4

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-3mdv2010.1
+ Revision: 516154
- rebuilt for apache-2.2.15

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2010.1
+ Revision: 507473
- rebuild

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2010.1
+ Revision: 506519
- 1.3.1

* Thu Jan 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-1mdv2010.1
+ Revision: 491462
- 1.3.0

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-2mdv2010.0
+ Revision: 406625
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-1mdv2010.0
+ Revision: 387754
- fix build
- 1.2.5
- rediffed patches

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-4mdv2009.1
+ Revision: 326166
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-3mdv2009.0
+ Revision: 235060
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2mdv2009.0
+ Revision: 215612
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Mon Mar 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1mdv2009.0
+ Revision: 191188
- import apache-mod_musicindex


* Mon Mar 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1mdv2008.1
- initial Mandriva package
