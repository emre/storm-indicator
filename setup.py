from distutils.core import setup

setup(
    name='storm-indicator',
    version='0.2',
    packages=['storm_indicator'],
    url='https://github.com/emre/storm-indicator',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='A unity indicator for connecting to your SSH connections easily.',
    scripts=[
        'storm_indicator/bin/ssh_list_indicator'
    ],
    install_requires=["stormssh", ],
)
