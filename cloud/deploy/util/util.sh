
###########
#
# getting location of where this script is run from
#
###########

get_curr_subdir() {
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    relative_subdir="${script_dir/#$PWD\//}"
    echo "relative_subdir: ${relative_subdir}"
}

get_curr_subdir