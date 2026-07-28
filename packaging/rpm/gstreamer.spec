
%{!?project_version:%global project_version 1.26.0}
%{!?snapshot_release:%global snapshot_release 79.git1eb6cfc}
%{!?commit:%global commit 1eb6cfc1ea793f1f62e95202204a5e53fe68d3ff}
%{!?shortcommit:%global shortcommit 1eb6cfc}

Name:           gstreamer
Version:        %{project_version}
Release:        %{snapshot_release}%{?dist}
Summary:        GStreamer multimedia framework with camera preview support
License:        LGPL-2.0-or-later
URL:            https://gitlab.freedesktop.org/gstreamer/gstreamer
Source0:        %{name}-%{commit}.tar.gz

BuildRequires:  meson >= 1.4
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel >= 2.62
BuildRequires:  alsa-lib-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  libgudev-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  gtk3-devel

# Additional codec support
BuildRequires:  ffmpeg-free-devel
BuildRequires:  mpg123-devel
BuildRequires:  flac-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  opus-devel

Requires:       glib2 >= 2.62

%description
GStreamer %{version} built from the h264-stateless-encoder source tree at
commit %{commit}. Installed under /opt/gstreamer for validation.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config files.

%prep
%autosetup -n %{name}-%{commit}

%build
export CCACHE_DISABLE=1

meson setup builddir \
  --prefix=/opt/gstreamer \
  --libdir=lib64 \
  --buildtype=release \
  -Dauto_features=disabled \
  -Dbase=enabled \
  -Dgood=enabled \
  -Dbad=enabled \
  -Dlibav=enabled \
  -Dugly=disabled \
  -Ddoc=disabled \
  -Dtests=disabled \
  -Dtools=enabled \
  -Dexamples=disabled \
  -Dintrospection=disabled \
  -Dgstreamer:dbghelp=disabled \
  -Dgobject-introspection:doctool=disabled \
  \
  -Dgst-plugins-base:encoding=enabled \
  -Dgst-plugins-base:playback=enabled \
  -Dgst-plugins-base:alsa=enabled \
  -Dgst-plugins-base:app=enabled \
  -Dgst-plugins-base:audioconvert=enabled \
  -Dgst-plugins-base:audioresample=enabled \
  -Dgst-plugins-base:audiorate=enabled \
  -Dgst-plugins-base:videorate=enabled \
  -Dgst-plugins-base:videoconvertscale=enabled \
  -Dgst-plugins-base:typefind=enabled \
  -Dgst-plugins-base:ogg=enabled \
  -Dgst-plugins-base:vorbis=enabled \
  -Dgst-plugins-base:opus=enabled \
  -Dgst-plugins-base:gl=enabled \
  -Dgst-plugins-base:drm=enabled \
  -Dgst-plugins-base:volume=enabled \
  \
  -Dgst-plugins-good:autodetect=enabled \
  -Dgst-plugins-good:v4l2=enabled \
  -Dgst-plugins-good:gtk3=enabled \
  -Dgst-plugins-good:jpeg=enabled \
  -Dgst-plugins-good:png=enabled \
  -Dgst-plugins-good:matroska=enabled \
  -Dgst-plugins-good:avi=enabled \
  -Dgst-plugins-good:isomp4=enabled \
  -Dgst-plugins-good:rtp=enabled \
  -Dgst-plugins-good:udp=enabled \
  -Dgst-plugins-good:id3demux=enabled \
  -Dgst-plugins-good:mpg123=enabled \
  -Dgst-plugins-good:wavparse=enabled \
  -Dgst-plugins-good:flac=enabled \
  -Dgst-plugins-good:audioparsers=enabled \
  -Dgst-plugins-good:multifile=enabled \
  -Dgst-plugins-good:videocrop=enabled \
  \
  -Dgst-plugins-bad:wayland=enabled \
  -Dgst-plugins-bad:kms=enabled \
  -Dgst-plugins-bad:gtk3=enabled \
  -Dgst-plugins-bad:drm=enabled \
  -Dgst-plugins-bad:v4l2codecs=enabled \
  -Dgst-plugins-bad:camerabin2=enabled \
  -Dgst-plugins-bad:videoparsers=enabled

meson compile -C builddir %{?_smp_mflags}

%install
DESTDIR=%{buildroot} meson install -C builddir

required_plugins="
libgstplayback.so
libgstalsa.so
libgstapp.so
libgstaudioconvert.so
libgstaudioresample.so
libgstaudiorate.so
libgstvolume.so
libgstvideoconvertscale.so
libgstvideorate.so
libgsttypefindfunctions.so

libgstogg.so
libgstvorbis.so
libgstopus.so

libgstwavparse.so
libgstflac.so
libgstmpg123.so
libgstaudioparsers.so
libgstid3demux.so

libgstjpeg.so
libgstpng.so
libgstmatroska.so
libgstavi.so
libgstisomp4.so

libgstvideo4linux2.so
libgstv4l2codecs.so
libgstcamerabin.so
libgstvideoparsersbad.so

libgstwaylandsink.so
libgstkms.so
libgstgtk.so
libgstgtkwayland.so

libgstlibav.so
"

for plugin in $required_plugins; do
    test -f %{buildroot}/opt/gstreamer/lib64/gstreamer-1.0/$plugin || {
        echo "FATAL: Missing plugin: $plugin"
        exit 1
    }
done

install -d %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/gstreamer.sh <<'EOF'
export PATH=/opt/gstreamer/bin${PATH:+:$PATH}
export PKG_CONFIG_PATH=/opt/gstreamer/lib64/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
export GST_PLUGIN_PATH=/opt/gstreamer/lib64/gstreamer-1.0${GST_PLUGIN_PATH:+:$GST_PLUGIN_PATH}
EOF

%files
%license LICENSE
/opt/gstreamer/
%exclude /opt/gstreamer/include
%exclude /opt/gstreamer/include/*
%exclude /opt/gstreamer/lib64/pkgconfig
%exclude /opt/gstreamer/lib64/pkgconfig/*
%exclude /opt/gstreamer/lib64/*.so
%{_sysconfdir}/profile.d/gstreamer.sh

%files devel
/opt/gstreamer/include/
/opt/gstreamer/lib64/pkgconfig/
/opt/gstreamer/lib64/*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Tue Jul 21 2026 Dhruvesh <dhruvesh@mecha.so>
- Enable libav plugin
- Enable Vorbis, Opus, FLAC, WAV and mpg123 plugins
- Enable audio parser and container plugins
- Enable V4L2, CameraBin and video parser plugins
- Enable Wayland, KMS and GTK sinks
- Add required multimedia BuildRequires
- Add plugin installation validation
- Fix validation for video4linux2 and waylandsink plugins