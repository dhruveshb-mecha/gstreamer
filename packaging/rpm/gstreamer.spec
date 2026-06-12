%{!?project_version:%global project_version 1.26.0}
%{!?snapshot_release:%global snapshot_release 79.git1eb6cfc}
%{!?commit:%global commit 1eb6cfc1ea793f1f62e95202204a5e53fe68d3ff}
%{!?shortcommit:%global shortcommit 1eb6cfc}

Name:           gstreamer
Version:        %{project_version}
Release:        %{snapshot_release}%{?dist}
Summary:        GStreamer multimedia framework with h264 stateless encoder support
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
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  libgudev-devel

Requires:       glib2 >= 2.62

%description
GStreamer %{version} built from the h264-stateless-encoder source tree at
commit %{commit}. The package is installed under /opt/gstreamer so it can be
shipped to Comet devices without replacing the OS GStreamer packages.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and linker symlinks for building software against
the Comet GStreamer package installed under /opt/gstreamer.

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
  -Dugly=disabled \
  -Ddoc=disabled \
  -Dexamples=disabled \
  -Dtests=disabled \
  -Dtools=enabled \
  -Dgst-plugins-base:videoconvertscale=enabled \
  -Dgst-plugins-base:typefind=enabled \
  -Dgst-plugins-good:jpeg=enabled \
  -Dgst-plugins-good:matroska=enabled \
  -Dgst-plugins-bad:v4l2codecs=enabled \
  -Dgst-plugins-bad:videoparsers=enabled

meson compile -C builddir %{?_smp_mflags}

%install
DESTDIR=%{buildroot} meson install -C builddir

install -d %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/gstreamer.sh <<'EOF'
if [ -z "${_COMET_GSTREAMER_SETUP_DONE:-}" ]; then
  export PATH=/opt/gstreamer/bin${PATH:+:$PATH}
  export PKG_CONFIG_PATH=/opt/gstreamer/lib64/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
  export GST_PLUGIN_PATH=/opt/gstreamer/lib64/gstreamer-1.0${GST_PLUGIN_PATH:+:$GST_PLUGIN_PATH}
  export GST_PLUGIN_PATH_1_0=/opt/gstreamer/lib64/gstreamer-1.0${GST_PLUGIN_PATH_1_0:+:$GST_PLUGIN_PATH_1_0}
  export GST_PLUGIN_SYSTEM_PATH=
  export GST_PLUGIN_SCANNER=/opt/gstreamer/libexec/gstreamer-1.0/gst-plugin-scanner
  export GST_PLUGIN_SCANNER_1_0=/opt/gstreamer/libexec/gstreamer-1.0/gst-plugin-scanner
  export _COMET_GSTREAMER_SETUP_DONE=1
fi
EOF

install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/gstreamer.conf <<'EOF'
/opt/gstreamer/lib64
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
%{_sysconfdir}/ld.so.conf.d/gstreamer.conf

%files devel
/opt/gstreamer/include/
/opt/gstreamer/lib64/pkgconfig/
/opt/gstreamer/lib64/*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Mon May 25 2026 Mecha Camera Build <build@mecha.local> - %{version}-%{release}
- Package h264-stateless-encoder build from commit %{commit}.
