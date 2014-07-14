#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_musicindex
%define mod_conf B31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	1.4.0
Release:	3
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
%_post_service httpd

%preun
%_preun_service httpd

%files -f %{mod_name}.lang
%doc AUTHORS COPYING ChangeLog README README.Handlers
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_datadir}/%{mod_name}



