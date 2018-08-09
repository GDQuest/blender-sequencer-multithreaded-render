from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='bpsrender',
    version='0.1.2',
    description='Blender Power Sequencer Renderer',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ],
    url='https://gitlab.com/razcore/BPSRender',
    keywords='blender render parallel multiprocess speedup utility'
    ' productivty',
    author='Razvan C. Radulescu',
    author_email='razcore.art@gmail.com',
    license='GPLv3',
    packages=['bpsrender'],
    install_requires=['tqdm'],
    zip_safe=False,
    entry_points={'console_scripts': ['bpsrender=bpsrender.__main__:main']},
    include_package_data=True)

