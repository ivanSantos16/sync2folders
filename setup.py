from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sync2folders',
      version='0.1.0',
      description='Synchronizes source and replica folders',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='sync folder',
      url='http://github.com/ivanSantos16/sync2folders',
      author='Ivan Santos',
      author_email='ivan.rafa.16@gmail.com',
      license='MIT',
      packages=['sync2folders'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)