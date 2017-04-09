from setuptools import setup, find_packages

setup(name='multiclip',
      version='1.0',
      description='System tray application - Creates nested context menu of given directory, Copies file contents to clipboard',
      author='Sahil Agarwal, Steen Catchpole',
      author_email='sahil.agarwal94@gmail.com, steen.catchpole@gmail.com',
      keywords='system tray application nested context menu directory copy file contents clipboard',
      # url='',
      license='MIT',
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Logging Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5'
      ],

      packages=find_packages(),
      )

