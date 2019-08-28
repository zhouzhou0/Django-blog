from django.contrib.auth.decorators import login_required


class LoginrequiredMixin(object):
    @classmethod
    # 调用父类的as_view
    def as_view(cls,**initkwargs):
        view=super(LoginrequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)