from django.shortcuts import render


def hello(request):
    print(request)
    x = 1
    y = 2
    # assert x + y == 4

    return render(request, "hello.html", {"result": x + y})
