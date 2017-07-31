
from form.validate import ValidatorMap


if __name__ == '__main__':
    from argparse import ArgumentParser
    import os
    from form.backends.hdf5 import HDF5IO
    from . import validate, load_namespaces, get_build_manager

    ep = """
    use --nspath to validate against an extension. If --ns is not specified,
    validate against all namespaces in namespace file.
    """

    def print_errors(errors):
        if len(errors) > 0:
            print(' - found the following errors:')
            for err in errors:
                print('%s - %s' % (err.name, err.reason))
        else:
            print(' - no errors found.')

    parser = ArgumentParser(description="Validate an NWB file")
    parser.add_argument("path", type=str, help="the path to the NWB file")
    parser.add_argument('-p', '--nspath', type=str, help="the path to the namespace file")
    parser.add_argument("-n", "--ns", type=str, help="the namespace to validate against")

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print('%s not found' % path, file=sys.stderr)
        sys.exit(1)

    io = HDF5IO(args.path, get_build_manager())

    if args.nspath is not None:
        namespaces = load_namespaces(args.nspath)
        if args.ns is not None:
            print('Validating against %s from %s.' % (args.ns, args.ns_path), end='')
        else:
            print('Validating using namespaces in %s.' % args.nspath)
            for ns in namespaces:
                print('Validating against %s' % ns, end='')
                errors = validate(io, ns)
                print_errors(errors)
    else:
        errors = validate(io)
        print('Validating against core namespace' % ns, end='')
        print_errors(errors)
