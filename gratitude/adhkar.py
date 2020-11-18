from flask import Blueprint

import api

adhkarRoutes = Blueprint('adhkar', __name__,)


@adhkarRoutes.route('/')
def adhkar_route_test():
    return 'Adhkar works!'

#
# @adhkarRoutes.route('/all')
# def all():
#     gratitudeReasons = Adhkarentry.query.all()
#
#     allReasons = [];
#
#     for reason in gratitudeReasons:
#         allReasons.append(reason.data)
#
#     return "<br />".join(allReasons)
