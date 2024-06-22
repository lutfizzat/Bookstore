from django.urls import path
from django.views.generic.base import TemplateView


from .views import ( 
    CheckoutView,
    BookDetail,
    HomePageView,
    CartView,
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart,
    book_collection_view,
    account_delete_view,
    payment_complete_view,
    
)

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),             #slug
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-from-cart/<slug:slug>/', remove_single_from_cart, name='remove_single_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart-summary/', CartView.as_view(), name='cart_summary'),
    path('bookprofile/<slug:slug>/', BookDetail.as_view(), name='booklist'),        #slug
    path('book_collection/', book_collection_view, name="book_collection"),
    path('account_delete/', account_delete_view, name="account_delete"),
    path('payment_complete/', payment_complete_view, name="payment_complete"),
    

]