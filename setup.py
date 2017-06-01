from setuptools import setup

setup(name='bookbot',
      version='0.1',
      description='Discord bot for HE-Arc/livre-python',
      url='https://github.com/greut/bookbot',
      author='Yoan Blanc',
      author_email='yoan@dosimple.ch',
      license='MIT',
      packages=['bookbot'],
      install_requires=['Discord.py', 'graphql-core'],
      entry_points={'console_scripts': [
          'bookbot = bookbot:main'
      ]},
      zip_safe=False)
