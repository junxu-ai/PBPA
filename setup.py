# -*- coding: utf-8 -*-
"""

@author: junxu
"""

from distutils.core import setup
setup(
    name = 'PBPA',
    version = '0.1.0',
    packages = ['PBPA'],
    include_package_data=True,
    package_data = {'PBPA':['Data/*.txt','Data/*.mat','Data/*.pptx',
                            'Figures/*.eps','Figures/*.jpg','Figures/*.png',
                            'Sample/*.pptx','Sample/*.png']},
    author = 'Jun Xu',
    author_email = 'jun.xu99@gmail.com',
    url = 'TBD',
    description = 'A simple block level trace parser, analyzer and reporter',
    )
