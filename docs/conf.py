# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2013)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

import sys
import inspect
import os.path
import re
import glob
import shutil
import subprocess
import warnings
from string import Template

from six.moves.configparser import (ConfigParser, NoOptionError)

from matplotlib import use
use('agg')

from sphinx.util import logging

import sphinx_bootstrap_theme

from numpydoc import docscrape_sphinx

import gwpy
from gwpy import _version as gwpy_version
from gwpy.plot.rc import DEFAULT_PARAMS as GWPY_PLOT_PARAMS
from gwpy.utils.sphinx import zenodo

GWPY_VERSION = gwpy_version.get_versions()

SPHINX_DIR = os.path.abspath(os.path.dirname(__file__))

# ignore warnings that aren't useful for documentation
warnings.filterwarnings('ignore', message=".*non-GUI backend.*",
                        category=UserWarning)
warnings.filterwarnings('ignore', message='.*gwpy.plot.*',
                        category=DeprecationWarning)

# -- General configuration ------------------------------------------------

#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# extension modules
# DEVNOTE: please make sure and add 3rd-party dependencies to
#          setup.py and requirements-dev.txt
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.linkcode',
    'sphinx.ext.ifconfig',
    'sphinx_automodapi.automodapi',
    'sphinxcontrib.programoutput',
    'numpydoc',
    'matplotlib.sphinxext.plot_directive',
    #'sphinxcontrib.doxylink',
    'gwpy.utils.sphinx.epydoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'GWpy'
copyright = u'2013, Duncan Macleod'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = GWPY_VERSION['version'].split('+')[0]
# The full version, including alpha/beta/rc tags.
release = GWPY_VERSION['version']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_templates', '_generated', 'references.rst']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# Epilog
rst_epilog = "\n.. include:: /references.rst"

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'monokai'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# -- Extensions ---------------------------------------------------------------

# -- autodoc ------------------------------------

autoclass_content = 'class'
autodoc_default_flags = ['show-inheritance', 'members', 'inherited-members']

# -- autosummary --------------------------------

autosummary_generate = True

# -- plot_directive -----------------------------

plot_rcparams = GWPY_PLOT_PARAMS
plot_rcparams.update({
    'backend': 'agg',
})
plot_apply_rcparams = True
plot_formats = ['png']
plot_include_source = True
plot_html_show_source_link = False

# -- numpydoc -----------------------------------

# fix numpydoc autosummary
numpydoc_show_class_members = False

# use blockquotes (numpydoc>=0.8 only)
numpydoc_use_blockquotes = True

# auto-insert plot directive in examples
numpydoc_use_plots = True

# update the plot detection to include .show() calls
parts = re.split('[\(\)|]', docscrape_sphinx.IMPORT_MATPLOTLIB_RE)[1:-1]
parts.extend(('fig.show()', 'plot.show()'))
docscrape_sphinx.IMPORT_MATPLOTLIB_RE = r'\b({})\b'.format('|'.join(parts))

# -- inhertiance_diagram ------------------------

# configure inheritance diagram
inheritance_graph_attrs = dict(rankdir='TB')

# -- epydoc -------------------------------------

# epydoc extension config for GLUE
epydoc_mapping = {
    'http://software.ligo.org/docs/glue/': [r'glue(\.|$)'],
}

# -- epydoc -------------------------------------

LALSUITE_DOCS = 'http://software.ligo.org/docs/lalsuite'

doxylink = {
    'lal': ('lal.tag', '%s/lal/' % LALSUITE_DOCS),
    'lalframe': ('lalframe.tag', '%s/lalframe/' % LALSUITE_DOCS),
}

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'bootstrap'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'source_link_position': None,
    'navbar_site_name': "Contents",
    'navbar_links': [("Examples", "examples/index")],
    'navbar_sidebarrel': True,
    'navbar_pagenav': False,
    'bootswatch_theme': 'flatly',
    'bootstrap_version': '3',
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = 'gwpy_white_24.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = os.path.join('_static', 'favicon.png')

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'**': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'GWpydoc'

# -- Intersphinx --------------------------------------------------------------

# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'matplotlib': ('http://matplotlib.org/', None),
    'astropy': ('http://docs.astropy.org/en/stable/', None),
    'pycbc': ('http://pycbc.org/pycbc/latest/html/', None),
    'root_numpy': ('http://scikit-hep.org/root_numpy/', None),
    'h5py': ('http://docs.h5py.org/en/latest/', None),
    'dateutil': ('https://dateutil.readthedocs.io/en/stable/', None),
}


# -- linkcode -----------------------------------------------------------------

def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object

    This code is stolen with thanks from the scipy team.
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except:
            return None
    # try and sneak past a decorator
    try:
        obj = obj.im_func.func_closure[0].cell_contents
    except (AttributeError, TypeError):
        pass

    try:
        fn = inspect.getsourcefile(obj)
    except:
        fn = None
    if not fn:
        try:
            fn = inspect.getsourcefile(sys.modules[obj.__module__])
        except:
            fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.findsource(obj)
    except:
        lineno = None

    if lineno:
        linespec = "#L%d" % (lineno + 1)
    else:
        linespec = ""

    fn = os.path.relpath(fn, start=os.path.dirname(gwpy.__file__))
    if fn.startswith(os.path.pardir):
        return None

    return ("http://github.com/gwpy/gwpy/tree/%s/gwpy/%s%s"
            % (GWPY_VERSION['full-revisionid'], fn, linespec))


# -- build CLI examples -------------------------------------------------------

CLI_TEMPLATE = Template("""
.. _gwpy-cli-example-${tag}:

${titleunderline}
${title}
${titleunderline}

${description}

.. code:: sh

   $$ ${command}

.. image:: ${png}
   :align: center
   :alt: ${title}
""")


def _build_cli_example(config, section, outdir, logger):
    raw = config.get(section, 'command')
    try:
        title = config.get(section, 'title')
    except NoOptionError:
        title = ' '.join(map(str.title, section.split('-')))
    try:
        desc = config.get(section, 'description')
    except NoOptionError:
        desc = ''

    outf = os.path.join(outdir, '{0}.png'.format(section))

    # build command-line strings for display and subprocess call
    cmd = 'gwpy-plot {0}'.format(raw)  # exclude --out for display
    cmds = (cmd + ' --interactive').replace(
        ' --', ' \\\n       --')  # split onto multiple lines
    cmdo = '{0} --out {1}'.format(cmd, outf)  # include --out for actual run

    rst = CLI_TEMPLATE.substitute(
        title=title, titleunderline='#'*len(title), description=desc,
        tag=section, png=outf[len(SPHINX_DIR):], command=cmds)

    # only write RST if new or changed
    rstfile = outf.replace('.png', '.rst')
    new = (not os.path.isfile(rstfile) or
           not os.path.isfile(outf) or
           open(rstfile, 'r').read() != rst)
    if new:
        with open(rstfile, 'w') as f:
            f.write(rst)
        logger.debug('[cli] wrote {0}'.format(rstfile))
        return rstfile, cmdo
    return rstfile, None


def build_cli_examples(_):
    logger = logging.getLogger('cli-examples')

    clidir = os.path.join(SPHINX_DIR, 'cli')
    exini = os.path.join(clidir, 'examples.ini')
    exdir = os.path.join(clidir, 'examples')
    if not os.path.isdir(exdir):
        os.makedirs(exdir)

    config = ConfigParser()
    config.read(exini)

    rsts = []
    for sect in config.sections():
        rst, cmd = _build_cli_example(config, sect, exdir, logger)
        if cmd:
            logger.info('[cli] running example {0!r}'.format(sect))
            logger.debug('[cli] $ {0}'.format(cmd))
            subprocess.check_call(cmd, shell=True)
            logger.debug('[cli] wrote {0}'.format(cmd.split()[-1]))
        rsts.append(rst)

    with open(os.path.join(exdir, 'examples.rst'), 'w') as f:
        f.write('.. toctree::\n   :glob:\n\n')
        for rst in rsts:
            f.write('   {0}\n'.format(rst[len(SPHINX_DIR):]))


# -- examples -----------------------------------------------------------------

def build_examples(_):
    logger = logging.getLogger('examples')
    logger.info('[examples] converting examples to RST...')

    srcdir = os.path.join(SPHINX_DIR, os.pardir, 'examples')
    outdir = os.path.join(SPHINX_DIR, 'examples')
    ex2rst = os.path.join(SPHINX_DIR, 'ex2rst.py')

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        logger.debug('[examples] created {0}'.format(outdir))

    for exdir in next(os.walk(srcdir))[1]:
        subdir = os.path.join(outdir, exdir)
        if not os.path.isdir(subdir):
            os.makedirs(subdir)
        # copy index
        index = os.path.join(subdir, 'index.rst')
        shutil.copyfile(os.path.join(srcdir, exdir, 'index.rst'), index)
        logger.debug('[examples] copied {0}'.format(index))
        # render python script as RST
        for expy in glob.glob(os.path.join(srcdir, exdir, '*.py')):
            target = os.path.join(
                subdir, os.path.basename(expy).replace('.py', '.rst'))
            subprocess.Popen([sys.executable, ex2rst, expy, target])
            logger.debug('[examples] wrote {0}'.format(target))
        logger.info('[examples] converted all in examples/{0}'.format(exdir))


# -- create citation file -----------------------------------------------------

def write_citing_rst(_):
    logger = logging.getLogger('zenodo')
    here = os.path.dirname(__file__)
    with open(os.path.join(here, 'citing.rst.in'), 'r') as fobj:
        citing = fobj.read()
    citing += '\n' + zenodo.format_citations(597016)
    out = os.path.join(here, 'citing.rst')
    with open(out, 'w') as f:
        f.write(citing)
    logger.info('[zenodo] wrote {0}'.format(out))


# -- add css and js files -----------------------------------------------------

CSS_DIR = os.path.join(html_static_path[0], 'css')
JS_DIR = os.path.join(html_static_path[0], 'js')

def setup_static_content(app):
    # add stylesheets
    for cssf in glob.glob(os.path.join(CSS_DIR, '*.css')):
        app.add_stylesheet(cssf.split(os.path.sep, 1)[1])

    # add custom javascript
    for jsf in glob.glob(os.path.join(JS_DIR, '*.js')):
        app.add_javascript(jsf.split(os.path.sep, 1)[1])


# -- setup --------------------------------------------------------------------

def setup(app):
    setup_static_content(app)
    app.connect('builder-inited', write_citing_rst)
    app.connect('builder-inited', build_examples)
    app.connect('builder-inited', build_cli_examples)
