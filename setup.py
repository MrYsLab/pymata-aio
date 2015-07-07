from distutils.core import setup

setup(
    name='pymata-aio',
    version='1.00',
    packages=['pymata_aio'],
    install_requires=['pyserial == 2.7', 'autobahn[asyncio,accelerate,compress'],
    url='',
    license='',
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    description='A Python Protocol Abstraction Library For Arduino Firmata using Python asyncio'
)
