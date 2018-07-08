from distutils.core import setup
setup(
  name='teampy',
  packages=['teampy'],
  version='0.1.1',
  description='Tools for Team-Based Learning',
  author='Frank Alexander Kraemer',
  author_email='kraemer.frank@gmail.com',
  license='GPL',
  url='https://github.com/falkr/teampy',
  download_url='https://github.com/falkr/teampy/archive/0.2.tar.gz',
  keywords=['education'],
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],
  entry_points = {'console_scripts': ['teampy=teampy.command_line_setup:teampy', 'rat=teampy.command_line_rat:rat']}
)
