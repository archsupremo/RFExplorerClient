# -*- coding: utf-8 -*-
import sys
from distutils.core import setup

kwargs = {}
if 'py2exe' in sys.argv:
    import py2exe
    kwargs = {
        'console' : [{
            'script'         : 'init.py',
            'description'    : 'Programa base para leer y enviar informacion.',
            #'icon_resources' : [(0, 'icon.ico')]
            }],
        'zipfile' : None,
        'options' : { 'py2exe' : {
            'dll_excludes'   : ["MSVCP90.dll"],
            'bundle_files'   : 1,
            'compressed'     : True,
            'optimize'       : 2
            }},
         }

setup(
    name='RFExplorerClient',
    author='Guillermo Lopez Garcia',
    author_email='guillermolopezgarcia96@gmail.com',
    **kwargs
    )
