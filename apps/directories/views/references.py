from django.shortcuts import render


def reference_list(request):
    return render(
        request,
        "directories/references/list.html"
    )