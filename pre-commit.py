#!/bin/env python
" Example Subversion pre-commit hook. "


def command_output(cmd):
    " Capture a command's standard output. "
    import subprocess
    return subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE).communicate()[0]


def files_added(look_cmd):
    """ List the files added or updated by this transaction.

  "svnlook changed" gives output like:
    U   trunk/file1.cpp
    A   trunk/file2.cpp
    """
    def filename(line):
        return line[4:]

    def added_or_updated(line):
        return line and line[0] == "A"
    return [
        filename(line)
        for line in command_output(look_cmd % "changed").split("\n")
        if added_or_updated(line)]


def valid_file_name(filename):
    " Return True if the file name is not UpperCaseCamel. "
    import os
    file_name_without_path = os.path.split(filename)[1]
    if "entitydef" in filename or "servicedef" in filename:
        is_valid_file_name = file_name_without_path.islower()
        if not is_valid_file_name:
            sys.stderr.write("File name should follow standard lower_snake_case.xml:\n%s\n"
                             % filename)
    else:
        is_valid_file_name = file_name_without_path[0].isupper()
        if not is_valid_file_name:
            sys.stderr.write("File name should follow standard UpperCamelCase:\n%s\n"
                             % filename)
    return not is_valid_file_name


def check_file_name(look_cmd):
    " Check file name. "
    def file_ext_to_check(fname):
        import os
        return os.path.splitext(fname)[1] in ".java .ftl .groovy .xml".split()
    file_with_invalid_name = [
        ff for ff in files_added(look_cmd)
        if file_ext_to_check(ff) and valid_file_name(ff)]
    return len(file_with_invalid_name)

def main():
    usage = """usage: %prog REPOS TXN

Run pre-commit options on a repository transaction."""
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--revision",
                      help="Test mode. TXN actually refers to a revision.",
                      action="store_true", default=False)
    errors = 0
    try:
        (opts, (repos, txn_or_rvn)) = parser.parse_args()
        look_opt = ("--transaction", "--revision")[opts.revision]
        look_cmd = "svnlook %s %s %s %s" % (
            "%s", repos, look_opt, txn_or_rvn)
        errors += check_file_name(look_cmd)
    except:
        parser.print_help()
        errors += 1
    return errors


if __name__ == "__main__":
    import sys
    sys.exit(main())

