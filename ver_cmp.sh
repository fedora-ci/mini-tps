#!/usr/bin/bash -efu

DEBUG="${DEBUG:-}"

# ➜  ~ echo -e "10\naa" |  sort -V
# 10
# aa
# ➜  ~ rpmdev-vercmp "aa" '10'
# aa < 10

debug() {
    if [ -n "${DEBUG:-}" ]; then
        echo "$*" >&2
    fi
}

from_nevra() {
    # Input: foo-1.0-1.i386 or foo-1:1.0-1.i386
    local nevra="$1" && shift
    # One of: name, ver, rel, epoch, arch
    local req_info="$1" && shift
    # Arch
    local arch="${nevra##*.}"
    debug "$nevra arch: $arch"
    [[ $req_info == 'arch' ]] && echo "$arch" && return
    # Release
    local rel="${nevra##*-}"
    rel="${rel%.*}"
    debug "$nevra rel: $rel"
    [[ $req_info == 'rel' ]] && echo "$rel" && return
    # Version
    local epoch_ver="${nevra%-${rel}.${arch}}"
    epoch_ver="${epoch_ver##*-}"
    local ver="${epoch_ver##*:}"
    debug "$nevra ver: $ver"
    [[ $req_info == 'ver' ]] && echo "$ver" && return
    # Epoch
    local epoch="${epoch_ver%${ver}}"
    epoch="${epoch//:/}"
    epoch="${epoch:-0}"
    debug "$nevra epoch: ${epoch}"
    [[ $req_info == 'epoch' ]] && echo "$epoch" && return
    # Name
    local name="${nevra%-${epoch_ver}-${rel}.${arch}}"
    debug "$nevra name: $name"
    [[ $req_info == 'name' ]] && echo "$name" && return
}

nevra_older_then() {
    # Verify with: rpmdev-vercmp
    # How rpm compares two package versions:
    # rpmUtils.miscutils.compareEVR(), which massages data types and then calls
    # rpm.labelCompare(), found in rpm.git/python/header-py.c, which
    # sets epoch to 0 if null, then compares epoch, then ver, then rel
    # using compare_values() and returns the first non-0 result, else 0.
    # This function combines the logic of compareEVR() and labelCompare().
    local nevra1="$1" && shift
    local nevra2="$1" && shift
    local name1="$(from_nevra "$nevra1" "name")"
    local name2="$(from_nevra "$nevra2" "name")"
    local epoch1="$(from_nevra "$nevra1" "epoch")"
    local epoch2="$(from_nevra "$nevra2" "epoch")"
    local version1="$(from_nevra "$nevra1" "ver")"
    local version2="$(from_nevra "$nevra2" "ver")"
    local release1="$(from_nevra "$nevra1" "rel")"
    local release2="$(from_nevra "$nevra2" "rel")"
    local arch1="$(from_nevra "$nevra1" "arch")"
    local arch2="$(from_nevra "$nevra2" "arch")"
    nevra1="${name1}-${epoch1}:${version1}-${release1}"
    nevra2="${name2}-${epoch2}:${version2}-${release2}"
    if [ "$nevra1" = "$nevra2" ]; then
        # False
        debug "$nevra1 == $nevra2"
        return 1
    fi
    local older="$(echo -e "$nevra1\n$nevra2" | sed -e 's/\([[:alnum:]]\+\)/0\1/g' | sed -e 's/\./ /g;' -e 's/_/\t/g' |  sort -V | sed -n -e '1p' | sed -e 's/ /./g;' -e 's/\t/_/g' | sed -e 's/0\([[:alnum:]]\+\)/\1/g')"
    # Special '~' case when rules doesn't apply:
    # 1. epoch1-version1-release1(before ~) == epoch2-version2-release2
    # 2. Only one of release1 or release2 has ~ in release.
    # Then result is reversed. Example:
    # rpmdev-vercmp 'grilo-plugins-0.3.5-3.el8+7~nogmime30' 'grilo-plugins-0.3.5-3.el8+7'
    # grilo-plugins-0.3.5-3.el8+7~nogmime30 < grilo-plugins-0.3.5-3.el8+7
    if [ "$nevra1" = "$older" ]; then
        newer="$nevra2"
    else
        newer="$nevra1"
    fi
    echo -n "$older < $newer "
    if [ "$older" != "$nevra1" ]; then
        # False
        debug "Not older"
        return 1
    fi
    # True
    return 0
}

echo 1
nevra_older_then "grilo-plugins-0:0.3.5-3.el8+7.noarch" "grilo-plugins-0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 2
nevra_older_then "grilo-plugins-0.3.5-3.el8+7.noarch" "grilo-plugins-0:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 3
nevra_older_then "grilo-plugins-0.3.5-3.el8+7.noarch" "grilo-plugins-0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 4
nevra_older_then "grilo-plugins-0.3.5-3.el8+7.noarch" "grilo-plugins-0.3.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 5
nevra_older_then "grilo-plugins-0:0.3.5-3.el8+7.noarch" "grilo-plugins-0:0.3.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 6
nevra_older_then "grilo-plugins-0.3.50-3.el8+8.noarch" "grilo-plugins-0.3.50-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 7
nevra_older_then "grilo-plugins-0:0.3.5-3.el8+8.noarch" "grilo-plugins-0:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 8
nevra_older_then "grilo-plugins-1:0.3.5-3.el8+8.noarch" "grilo-plugins-0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 9
nevra_older_then "grilo-plugins-1:0.3.5-3.el8+8.noarch" "grilo-plugins-0:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 10
nevra_older_then "grilo-plugins-0.3.5-3.el8+7.noarch" "grilo-plugins-1:0.3.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 11
nevra_older_then "grilo-plugins-0:0.3.5-3.el8+7.noarch" "grilo-plugins-1:0.3.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 12
nevra_older_then "grilo-plugins-10:0.3.5-3.el8+8.noarch" "grilo-plugins-9:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 13
nevra_older_then "grilo-plugins-9:0.3.5-3.el8+7.noarch" "grilo-plugins-10:0.3.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 14
nevra_older_then "grilo-plugins-10:0.3.5-3.el8+7.noarch" "grilo-plugins-9:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 15
nevra_older_then "grilo-plugins-9:0.3.5-3.el8+7.noarch" "grilo-plugins-10:0.3.5-3.el8+7.noarch" && echo "OK" || echo "FAIL"
echo 16
nevra_older_then "grilo-plugins-9:0.3.5-3.el8+7~nogmime30+7.noarch" "grilo-plugins-1:0.3.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 17
nevra_older_then "grilo-plugins-1:0.3.5-3.el8+7.noarch" "grilo-plugins-9:0.3.5-3.el8+7~nogmime30+7.noarch" && echo "OK" || echo "FAIL"
echo 18
nevra_older_then "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" "grilo-plugins-0.3.5-3.el8+7.noarch" && echo "OK" || echo "FAIL"
echo 19
nevra_older_then "grilo-plugins-0.3.5-3.el8+7.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" && echo "FAIL" || echo "OK"
echo 20
nevra_older_then "grilo-plugins-0.11.5-3.el8+7.noarch" "grilo-plugins-0.9.5-3.el8+7.noarch" && echo "FAIL" || echo "OK"
echo 21
nevra_older_then "grilo-plugins-0.9.5-3.el8+7.noarch" "grilo-plugins-0.11.5-3.el8+8.noarch" && echo "OK" || echo "FAIL"
echo 22
nevra_older_then "grilo-plugins-0.11.5-3.el8+7.noarch" "grilo-plugins-5:0.9.5-3.el8+7.noarch" && echo "OK" || echo "FAIL"
echo 23
nevra_older_then "grilo-plugins-5:0.9.5-3.el8+7.noarch" "grilo-plugins-0.11.5-3.el8+8.noarch" && echo "FAIL" || echo "OK"
echo 24
nevra_older_then "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime31+7.noarch" && echo "OK" || echo "FAIL"
echo 25
nevra_older_then "grilo-plugins-0.3.5-3.el8+7~nogmime31+7.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" && echo "FAIL" || echo "OK"
echo 26
nevra_older_then "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime30+8.noarch" && echo "OK" || echo "FAIL"
echo 27
nevra_older_then "grilo-plugins-0.3.5-3.el8+7~nogmime30+8.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime30+7.noarch" && echo "FAIL" || echo "OK"
echo 28
nevra_older_then "grilo-plugins-1:0.3.5-3.el8+7~nogmime30+7.noarch" "grilo-plugins-0.3.5-3.el8+7~nogmime31+7.noarch" && echo "FAIL" || echo "OK"
echo 29
nevra_older_then "java-11-openjdk-demo-1:11.0.ea.22-5.el8.x86_64" "java-11-openjdk-demo-1:11.0.1.13-4.el8.x86_64" && echo "OK" || echo "FAIL"
echo 30
nevra_older_then "java-11-openjdk-demo-1:11.0.0.22-5.el8.x86_64" "java-11-openjdk-demo-1:11.0.1.13-4.el8.x86_64" && echo "OK" || echo "FAIL"
echo 31
nevra_older_then "java-11-openjdk-demo-1:11.0.ea.22-5.el8.x86_64" "java-11-openjdk-demo-1:11.0.0.13-4.el8.x86_64" && echo "OK" || echo "FAIL"
echo 32
nevra_older_then "a2a10-1:11.0.ea.22-5.el8.x86_64" "a10a10-1:11.0.0.13-4.el8.x86_64" && echo "OK" || echo "FAIL"
echo 33
nevra_older_then "a10a22a-1:11.0.ea.22-5.el8.x86_64" "a10a222a-1:11.0.0.13-4.el8.x86_64" && echo "OK" || echo "FAIL"
echo 34
nevra_older_then "kmod-25-11.el8_0.1.x86_64" "kmod-25-11.el8.1.x86_64" && echo "OK" || echo "FAIL"
echo 35
nevra_older_then "kmod-25-11.el8.x86_64" "kmod-25-11.el8_0.1.x86_64" && echo "OK" || echo "FAIL"
