from setuptools import setup

setup(
    name='dx1-qa-framework',
    version='2.0.0',
    packages=['framework', 'framework.forms', 'framework.pages', 'framework.utils', 'framework.waits',
              'framework.browser', 'framework.scripts', 'framework.elements', 'framework.elements.base',
              'framework.constants', 'framework.configuration'],
    package_data={
        # If any package contains *.txt or *.json files, include them:
        '': ['*.txt', '*.json']
    },
    install_requires=[
        'pytest==3.8.1',
        'pytest-allure-adaptor==1.7.10',
        'allure-python-commons==2.5.2',
        'webdriver-manager==1.7',
        'selenium==3.14.1',
        'PyHamcrest==1.9.0',
        'dpath==1.4.2',
        'Pillow==5.3.0',
        'axe-selenium-python==2.1.2'
    ],
    url='https://gitlab.digitalx1.io/TAMM/quality-assurance/ui-automation-framework',
    license='MIT',
    author='[John Doe, Mark Lee]',
    author_email='[john@test.com, lee@test.com]',
    description='UI Testing Framework',
    zip_safe=False
)
