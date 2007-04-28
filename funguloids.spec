%define name funguloids
%define version 1.06
# pre release from http://www.ogre3d.org/phpBB2/viewtopic.php?t=29147&postdays=0&postorder=asc&start=75 (with autotools and OpenAL support)
%define pre 0
%define distname %{name}-%{version}-%{pre}
%define release %mkrel 1

Summary: Those Funny Funguloids! arcade game
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.newbyteorder.net/%{distname}.tar.bz2
License: Zlib/libpng
Group: Games/Arcade
Url: http://funguloids.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: automake1.8 ogre-devel lua5.1-devel

%description
Never before has collecting mushrooms been this mildly
entertaining. At least not in outer space. It's more of a lifestyle
than a game, really. Now with graphics and sound, too!

%prep
%setup -q -n %{distname}
perl -pi -e 's/-llua5\.1/-llua/' configure*
autoreconf
%configure2_5x --prefix=%{_datadir} --bindir=%{_gamesbindir}

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}.sh
%{_gamesdatadir}/%{name}
