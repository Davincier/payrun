from distutils.core import setup
import py2exe

setup(
    windows=['app.py'],
    options={
        'py2exe': {
            'packages': [
                'controllers',
                'models',
                'views',
                'pyvista',
                'stylesheets'
            ]
        }
    },
    requires=['PyQt5']
)