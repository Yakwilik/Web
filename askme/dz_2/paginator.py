from django.core.paginator import Paginator


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

