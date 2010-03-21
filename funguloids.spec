%define name funguloids
%define version 1.06.4
# pre release from http://www.ogre3d.org/phpBB2/viewtopic.php?t=29147&postdays=0&postorder=asc&start=75 (with autotools and OpenAL support)
##%define pre 0
%define distname %{name}-linux-src-1.06-4
%define release %mkrel 9

Summary:	Those Funny Funguloids! arcade game
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.newbyteorder.net/%{distname}.tar.bz2
Source1:	funguloids-linux-1.06-4.tar.bz2
# (ahmad) fix segmenation fault on selecting "start game", due to change in ogre
# using mpak.py, from upstream author, to unpack modify the scritps and repack
# c.f. http://www.mail-archive.com/packman@links2linux.de/msg02703.html
Source2:	mpak.py
Patch0:		funguloids-1.06-0-noCg.patch
Patch1:		 funguloids-1.06-4-gcc43.patch
Patch2:	 	funguloids-size_chunks_reverse.patch
# (misc) new ogre engine no longer have setnormaliseNormals 
# and requires the archive class to return the modification date
# of the file. I choosed to return 0 since this information is missing
Patch3:		funguloids-1.06-fix_new_ogre.diff
# add upstream patch to make it work with openal, because it defaults to openal-soft
Patch4:		funguloids-1.06.4-alc_error.patch

License:	Zlib/libpng
Group:		Games/Arcade
Url:		http://funguloids.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake1.8
BuildRequires:	lua5.1-devel ogre-devel ois-devel
BuildRequires:	freealut-devel mad-devel oggvorbis-devel openal-devel
Requires:	ogre

%description
Never before has collecting mushrooms been this mildly
entertaining. At least not in outer space. It's more of a lifestyle
than a game, really. Now with graphics and sound, too!

%prep
%setup -q -n %{name} -a 1
%patch0 -p1 -b .noCg
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
perl -pi -e 's/-llua5\.1/-llua/' configure*
autoreconf -fi

# fix scritps using mpak.py from upstream
cp %{SOURCE2} .
python mpak.py -e -f funguloids/bin/bootstrap.mpk -p _bootstrap
python mpak.py -e -f funguloids/bin/funguloids.mpk -p _gamedata
sed -ri '/^[A-Z]/ s/(.*)/overlay \1/' _bootstrap/*.overlay _gamedata/*.overlay
sed -ri '/^[A-Z]/ s/(.*)/particle_system \1/' _gamedata/*.particle
# This last one looks like a bug in ogre, should be removed when fixed
# The problem is that green and blue mushrooms have a square instead of a glow
sed -ri 's/^(\t\t\t)(texture_unit) 1/\1\2\n\1{\n\1}\n\1\2/' _gamedata/materials.material
python mpak.py -c -f funguloids/bin/bootstrap.mpk _bootstrap/*
python mpak.py -c -f funguloids/bin/funguloids.mpk _gamedata/*
rm -rf mpak.py _bootstrap _gamedata

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install %{name}/bin/*.mpk %{buildroot}%{_gamesdatadir}/%{name}
install bin/icon/*.png %{buildroot}%{_gamesdatadir}/%{name}/music

install -m 755 -d %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Those Funny Funguloids!
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/docs/%{name}/*
