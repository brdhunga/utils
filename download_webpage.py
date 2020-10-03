import argparse

from pywebcopy import save_webpage


parser = argparse.ArgumentParser(description='Download a given website.')
parser.add_argument('-n', type=str, 
    help='Name of the project aka the directory')
parser.add_argument('-d', type=str, 
    help='Directory to save the project')
parser.add_argument('-w', type=str, 
    help='Website to download')

args = parser.parse_args()


kwargs = {'project_name': args.n}

save_webpage(
    url=args.w,
    project_folder=args.d,
    **kwargs
)
