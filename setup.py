from setuptools import setup, find_packages
import os

version_path = os.path.join("younglives", "publication", "version.txt")

version = open(version_path).read().strip()

long_description = open(os.path.join("docs", "README.txt")).read()
long_description += "\n" + open(os.path.join("docs", "INSTALL.txt")).read()
long_description += "\n" + open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='younglives.publication',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='Publication content type for Young Lives website',
      author='Michael Davis',
      author_email='M.R.Davis@me.com',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['younglives'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={
          'test': ['plone.app.testing', ]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
