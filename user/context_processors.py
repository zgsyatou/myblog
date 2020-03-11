from .forms import LoginForm

# 定义返回的公用模板
def login_modal_form(request):
    return {'login_modal_form': LoginForm()}  # 字典值为实例化的对象