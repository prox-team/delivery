from setuptools import setup
import pkg_resources


def get_requires():
    path = 'delivery/requirements.txt'  # always use slash
    filepath = pkg_resources.resource_filename(__name__, path)
    with open(filepath) as file:
        packages = [name.rstrip() for name in file.readlines()]
    return packages


setup(
    name='delivery',
    version='0.2.0',
    packages=['delivery'],
    url='https://github.com/ponomarevkonst/delivery',
    license='MIT',
    author='Konstantin Ponomarev',
    author_email='ponomarevkonst@gmail.com',
    description='Сервис доставки еды',
    include_package_data=True,
    install_requires=get_requires()
)
