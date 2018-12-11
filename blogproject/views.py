from common.response import render
from .settings import STATIC_URL


def index_page(request):
    return render(request, 'index.html')
