# from django.shortcuts import render
# from operator import attrgetter
# from account.models import Product


# def home_screen_view(request):
#     context = {}

#     query = ""
#     if request.GET:
#         query = request.GET.get('q', '')
#         context['query'] = str(query)

#     book_products = sorted(Product.objects.all(), key=attrgetter('price'), reverse=True)
#     context['book_products'] = book_products


   



#     return render(request, 'personal/home.html', context)

