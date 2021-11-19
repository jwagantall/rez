# dumb script to update copyright notice in a py sourcefile
#
from __future__ import print_function
import argparse
import sys


new_copyright = \
"""
# Copyright Contributors to the Rez project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

lines = []
NO_COPYRIGHT = "NO_COPYRIGHT"
OTHER_COPYRIGHT = "OTHER_COPYRIGHT"


def find_existing_copyright():
    i_start = None

    for i, line in enumerate(lines):
        if line.startswith('#') and "Copyright" in line:
            if "Allan" in line or "Rez" in line:
                i_start = i
                break
            else:
                return OTHER_COPYRIGHT

    if i_start is None:
        return NO_COPYRIGHT

    i_end = i_start

    while True:
        if (i_end + 1) >= len(lines):
            break

        if lines[i_end + 1].startswith('#'):
            i_end += 1
        else:
            break

    return (i_start, i_end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE")
    parser.add_argument("-s", "--strip-copyright", action="store_true")
    parser.add_argument("-o", "--overwrite-file", action="store_true")
    parser.add_argument("-p", "--print-existing", action="store_true")
    parser.add_argument("-P", "--print-status", action="store_true")
    opts = parser.parse_args()

    with open(opts.FILE) as f:
        txt = f.read()
    lines = txt.split('\n')

    result = find_existing_copyright()

    if opts.print_status:
        if isinstance(result, tuple):
            print("COPYRIGHT")
        else:
            print(result)
        sys.exit(0)

    if not isinstance(result, tuple):
        print("No/other copyright", file=sys.stderr)
        sys.exit(1)
    i_start, i_end = result

    if opts.print_existing:
        copyright_lines = lines[i_start:i_end + 1]
        print('\n'.join(copyright_lines))
        sys.exit(0)

    # strip existing copyright
    lines = lines[:i_start] + lines[i_end + 1:]

    # strip trailing empty lines
    while lines and not lines[-1]:
        lines = lines[:-1]

    # add new copyright at top of file
    if not opts.strip_copyright:
        copyright_lines = new_copyright.strip().split('\n')
        lines = copyright_lines + [''] + lines

    # output
    new_txt = '\n'.join(lines)

    if not opts.overwrite_file:
        print(new_txt)
    else:
        with open(opts.FILE, 'w') as f:
            f.write(new_txt)

        print("Replaced %s" % opts.FILE, file=sys.stderr)
