# pre release from http://www.ogre3d.org/phpBB2/viewtopic.php?t=29147&postdays=0&postorder=asc&start=75 (with autotools and OpenAL support)
##%define pre 0
%define distname %{name}-linux-src-1.06-4

Summary:	Those Funny Funguloids! arcade game
Name:		funguloids
Version:	1.06.4
Release:	15
License:	Zlib/libpng
Group:		Games/Arcade
Url:		http://funguloids.sourceforge.net/
Source0:	http://www.newbyteorder.net/%{distname}.tar.bz2
Source1:	funguloids-linux-1.06-4.tar.bz2
# (ahmad) fix segmenation fault on selecting "start game", due to change in ogre
# using mpak.py, from upstream author, to unpack, modify the scritps and repack
# c.f. http://www.mail-archive.com/packman@links2linux.de/msg02703.html
Source2:	mpak.py
Patch0:		funguloids-1.06-0-noCg.patch
Patch1:		funguloids-1.06-4-gcc43.patch
Patch2:		funguloids-size_chunks_reverse.patch
# add upstream patch to make it work with openal, because it defaults to openal-soft
Patch3:		funguloids-1.06-more-ogre.patch
Patch4:		funguloids-1.06.4-alc_error.patch
# fix doc location
Patch5:		funguloids-1.06-fix-doc-location.patch
Patch6:		funguloids-ogre-1.7.0.patch
Patch7:		funguloids-1.06-gcc4.7.patch
Patch8:		funguloids-1.06-linkage.patch
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
%patch3 -p1
%patch4 -p0
%patch5 -p0 -b .doc
%patch6 -p1
%patch7 -p1
%patch8 -p1
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
Comment=%{summary}
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
%{_datadir}/doc/%{name}


%changelog
* Sun Feb 06 2011 Funda Wang <fwang@mandriva.org> 1.06.4-13mdv2011.0
+ Revision: 636431
- update opal patch from archlinux
- add archlinux patch to build with ogre 1.7

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.06.4-12mdv2011.0
+ Revision: 610777
- rebuild

* Sun May 02 2010 Funda Wang <fwang@mandriva.org> 1.06.4-11mdv2010.1
+ Revision: 541523
- rebuild
- fix desktop file

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - add patch to install docs to %%_docdir
    - clean spec

* Sun Mar 21 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.06.4-9mdv2010.1
+ Revision: 526273
- clean spec
- add upstream patch to make it work with openal
- use upstream mpak.py to fix the scripts to make it work with new ogre changes

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 1.06.4-8mdv2010.0
+ Revision: 437608
- rebuild

* Sun Mar 29 2009 Michael Scherer <misc@mandriva.org> 1.06.4-7mdv2009.1
+ Revision: 362175
- fix build by porting to the new ogre library, to fix  bug #49268

  + Emmanuel Andry <eandry@mandriva.org>
    - add missing menu entry
    - add support for ogre 1.4.6 and later with P2
    - really requires ogre

* Tue Aug 26 2008 Emmanuel Andry <eandry@mandriva.org> 1.06.4-4mdv2009.0
+ Revision: 276162
- fix typo
- drop ogre requires
- add P1 from Pardus to fix gcc43 build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Mar 11 2008 Erwan Velu <erwan@mandriva.org> 1.06.4-2mdv2008.1
+ Revision: 186975
- Fixing requires

* Fri Feb 22 2008 Emmanuel Andry <eandry@mandriva.org> 1.06.4-1mdv2008.1
+ Revision: 173918
- New version
- drop patch1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed May 02 2007 Olivier Blin <oblin@mandriva.com> 1.06-0.pre0.4mdv2008.0
+ Revision: 20528
- write ogre config and log files in home directory (patch from upstream forum, #30583)

* Tue May 01 2007 Olivier Blin <oblin@mandriva.com> 1.06-0.pre0.3mdv2008.0
+ Revision: 19976
- really disable Cg (by patching .in file...)

* Mon Apr 30 2007 Olivier Blin <oblin@mandriva.com> 1.06-0.pre0.2mdv2008.0
+ Revision: 19529
- disable Cg plugin

* Sun Apr 29 2007 Olivier Blin <oblin@mandriva.com> 1.06-0.pre0.1mdv2008.0
+ Revision: 19090
- buildrequire mad-devel
- buildrequire oggvorbis-devel
- buildrequire ois-devel
- buildrequire freaalut-devel
- buildrequire openal-devel
- add mpk data files from src+data tarball
- initial funguloids package (from pre 1.06 release with autotools and OpenAL support)
- Create funguloids

