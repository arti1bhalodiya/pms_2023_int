# from django.contrib.auth.decorators import user_passes_test

# def manager_required(function):
#     decorated_view_func = user_passes_test(
#         lambda user: user.is_authenticated and user.is_manager1,
#         login_url='/login/'
#     )(function)
#     return decorated_view_func