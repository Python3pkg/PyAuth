# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
# To use a consistent encoding
from codecs import open
from os import path
from glob import glob
import pkg_resources
import pyauth

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Icon files to add to system
icon_files = []
# Large program icons plus icon bundles
files = glob( 'pyauth/images/*.png' )
entry = ( 'share/icons/hicolor/512x512/apps', files )
icon_files.append( entry )
# Specific sizes of icons
for s in [ 16, 24, 32, 48, 64, 128, 256 ]:
    files = glob( 'pyauth/images/{0}x{0}/*.png'.format( str(s) ) )
    entry = ( 'share/icons/hicolor/{0}x{0}/apps'.format( str(s) ), files )
    icon_files.append( entry )


# Post-installation script
def _post_install( data_path, script_path ):
    # Read in the desktop shortcut template and substitute final paths into it to create
    # the real shortcut file
    template_filename = data_path + '/share/doc/' + pyauth.__program_name__ + '/PyAuth.desktop.in'
    shortcut_filename = data_path + '/share/doc/' + pyauth.__program_name__ + '/PyAuth.desktop'
    ## TODO This isn't working, need some sort of fix at some point
    ## if path.exists( template_filename ):
    ##     with open( template_filename, 'r' ) as template:
    ##         with open( shortcut_filename, 'w' ) as shortcut:
    ##             for line in template:
    ##                 l = line.format( program_name = pyauth.__program_name__,
    ##                                 script_path = script_path,
    ##                                 data_path = data_path )
    ##                 shortcut.write( l )
    ##     os.chmod( shortcut_filename, 0755 )


# Classes to add post-install behavior to standard install and develop commands

class my_install( _install ):
    def run( self ):
        _install.run( self )
        self.execute( _post_install, [ self.install_data, self.install_scripts ],
                      msg = "Running post install task" )

class my_develop( _develop ):
    def run( self ):
        _develop.run( self )
        self.execute( _post_install, [ self.install_data, self.install_scripts ],
                      msg = "Running post develop task" )


setup(
    name = pyauth.__program_name__,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = pyauth.__version__ + pyauth.__version_tag__,

    description = 'Google Authenticator (TOTP) desktop client',
    long_description = long_description,

    # The project's main homepage.
    url = 'https://github.com/tknarr/PyAuth',

    # Author details
    author = 'Todd Knarr',
    author_email = 'tknarr@silverglass.org',

    # Choose your license
    license = 'GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Security',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',

        # Other classifiers
        'Environment :: X11 Applications',
        'Operating System :: Unix',
    ],

    keywords = 'authentication totp hotp 2fa',

    packages = find_packages( exclude = ['contrib', 'docs', 'tests*'] ),

    install_requires = [
        'pyotp>=2.0.1'
        ],

    package_data = {
        'pyauth': [ 'LICENSE.html',
                    'images/*.ico',
                    'images/PyAuth-systray*.png'
                    ]
        },

    data_files = icon_files + [
        ( 'share/doc/' + pyauth.__program_name__,
          [ 'README.rst',
            'pyauth/LICENSE.html',
            'TODO.md',
            'VERSIONS.md',
            'PyAuth.desktop.in'
          ] )
        ],

    entry_points = {
        'gui_scripts': [
            'PyAuth=pyauth.__main__:main',
        ],
    },

    cmdclass = {
        'install': my_install,  # override install
        'develop': my_develop   # develop is used for pip install -e .
        }
)
