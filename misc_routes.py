from flask import Blueprint
from datetime import datetime

miscRoutes = Blueprint('misc', __name__,)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#       Inane miscelania
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
@miscRoutes.route('/hi')
def hello_world2():
    return 'Hi, World!'


@miscRoutes.route('/time')
def current_time():
    today = datetime.now()
    result =  today.strftime("%H:%M:%S on %d %B, %Y: ") + "Hello world"
    return result;
