%define name funguloids
%define version 1.06.4
# pre release from http://www.ogre3d.org/phpBB2/viewtopic.php?t=29147&postdays=0&postorder=asc&start=75 (with autotools and OpenAL support)
#%define pre 0
%define distname %{name}-linux-src-1.06-4
%define release %mkrel 2

Summary: Those Funny Funguloids! arcade game
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.newbyteorder.net/%{distname}.tar.bz2
Source1: funguloids-linux-1.06-4.tar.bz2
Patch0:	 funguloids-1.06-0-noCg.patch
# rediffed from http://www.ogre3d.org/phpBB2/viewtopic.php?p=218467#218467
#Patch1:	 funguloids-1.06-0-root.patch
License: Zlib/libpng
Group: Games/Arcade
Url: http://funguloids.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: automake1.8
BuildRequires: lua5.1-devel ogre-devel ois-devel
BuildRequires: freealut-devel mad-devel oggvorbis-devel openal-devel
Requires: ogre

%description
Never before has collecting mushrooms been this mildly
entertaining. At least not in outer space. It's more of a lifestyle
than a game, really. Now with graphics and sound, too!

%prep
%setup -q -n %{name} -a 1
%patch0 -p1 -b .noCg
#%patch1 -p1 -b .root
perl -pi -e 's/-llua5\.1/-llua/' configure*
autoreconf
%configure2_5x --bindir=%{_gamesbindir}

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install %{name}/bin/*.mpk %{buildroot}%{_gamesdatadir}/%{name}
install bin/icon/*.png %{buildroot}%{_gamesdatadir}/%{name}/music

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/docs/%{name}/*
