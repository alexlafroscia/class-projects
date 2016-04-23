"""A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop

requirements = [
    'nltk>=2.0.4',
]


def _post_install():
    from importlib import reload
    import site
    reload(site)

    import nltk
    nltk.download('punkt')


class my_install(install):
    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg='Running post install task')


class my_develop(develop):
    def run(self):
        develop.run(self)
        self.execute(_post_install, [], msg='Running post develop task')

setup(
    name='ngram',

    version='0.0.1',

    description='NGram Model Builder',

    # Author details
    author='Alex LaFroscia',
    author_email='alex@lafroscia.com',

    license='MIT',

    packages=find_packages('.'),
    package_dir={'': '.'},

    install_requires=requirements,
    cmdclass={
        'install': my_install,  # override install
        'develop': my_develop   # develop is used for pip install -e .
    }
)
