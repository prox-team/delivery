"""
Сервис доставки еды из вымышленного ресторана.
"""
__author__ = 'Konstantin Ponomarev'
__maintainer__ = __author__

__email__ = 'ponomarevkonst@gmail.com'
__license__ = 'MIT'
__version__ = '0.2.0'


__all__ = (
    '__author__',
    '__email__',
    '__license__',
    '__maintainer__',
    '__version__',
)

from flask import Flask
from delivery.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from delivery.views import *

if __name__ == '__main__':
    app.run()
