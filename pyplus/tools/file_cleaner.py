
import os
import time
import fnmatch


def match(paths, atimeout=None, ctimeout=None, mtimeout=None, seed=None, patterns=None, verbose=False):
    '''
    :param paths:  path for clean
    :param atimeout: file will be deleted after access timeout
    :param ctimeout: file will be deleted after creation timeout
    :param mtimeout: file will be deleted after modification timeout
    :param seed: base line of current time
    :param patterns: includes and excludes patterns with format [('i', pattern), ('e', pattern), ...]
    :return: file list
    '''

    # args check
    if isinstance(paths, str): paths = [paths]
    assert isinstance(paths, (tuple, list))
    if seed is None: seed = time.time()
    if patterns is None: patterns = ['i', '*']

    # match function
    def check_include(f):
        # check patterns
        for t, p in patterns:
            m = fnmatch.fnmatch(file_path, p)
            if t == 'i':
                if not m: continue
                break

            else:
                if not m: continue
                return False

        # check
        at, ct, mt = os.path.getatime(f), os.path.getctime(f), os.path.getmtime(f)
        if atimeout is not None and seed - at < atimeout: return False
        if ctimeout is not None and seed - ct < ctimeout: return False
        if mtimeout is not None and seed - mt < mtimeout: return False

        return True


    # scan all paths
    include_files = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            for f in files:
                file_path = os.path.join(root, f)
                if not check_include(file_path): continue
                include_files.append(file_path)
                if verbose: print(file_path)

    return include_files




def remove_empty_dirs(paths):
    def _do(path):
        empty = True
        for f in os.listdir(path):
            f = os.path.join(path, f)
            if os.path.isfile(f):
                empty = False
                break

            if not _do(f):
                empty = False
                break
        return empty


    for p in paths:
        _do(p)




def clean(paths, atimeout=None, ctimeout=None, mtimeout=None, seed=None, patterns=None, remove_empty_dir=True, verbose=False):
    '''
    :params: see test method
    :return: None
    '''

    # find all deleted files
    files = match(paths, atimeout, ctimeout, mtimeout, seed, patterns, False)

    # remove files
    for f in files:
        try:
            os.remove(f)
        except: pass
        if verbose: print(f)


    # clear empty directories
    if remove_empty_dir: remove_empty_dirs(paths)








def main():
    import argparse

    class PatternAction(argparse.Action):
        def __init__(self, *args, **kwargs):
            super(PatternAction, self).__init__(*args, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            if not 'patterns' in namespace:
                setattr(namespace, 'patterns', [])
            tag = 'i' if self.dest == 'include' else 'e'
            namespace.patterns.append((tag, values))

    parser = argparse.ArgumentParser(prog='fclean', description="A clean tool for remove timeout files and path")
    parser.add_argument('-p', '--path', type=str, required=True, action='append', help='Path for clean')
    parser.add_argument('-t', '--timeout', type=int, help='File will be deleted after timeout')
    parser.add_argument('-at', '--access-timeout', type=int, help='File will be deleted after last access timeout')
    parser.add_argument('-ct', '--creation-timeout', type=int, help='File will be deleted after creation timeout')
    parser.add_argument('-mt', '--modification-timeout', type=int, help='File will be deleted after modification timeout')
    parser.add_argument('-s', '--seed', type=float, default=None, help='Base line of current time')
    parser.add_argument('-i', '--include', type=str, action=PatternAction, help='Include files matching PATTERN')
    parser.add_argument('-e', '--exclude', type=str, action=PatternAction, help='Exclude files matching PATTERN')
    parser.add_argument('-m', '--match', action='store_true', default=False, help='Only execute match instead of remove files')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase verbosity')
    parser.add_argument('-k', '--keep', action='store_true', default=False, help='Keep empty directories')
    args = parser.parse_args()

    # parse timeout
    if args.timeout is not None and args.access_timeout is None:
        args.access_timeout = args.timeout

    if args.match:
        match(args.path, args.access_timeout, args.creation_timeout, args.modification_timeout,
              args.seed, args.patterns, args.verbose)
    else:
        clean(args.path, args.access_timeout, args.creation_timeout, args.modification_timeout,
              args.seed, args.patterns, not args.keep, args.verbose)



if __name__ == '__main__':
    main()


