from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/<int:event_id>/', views.BookingCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<int:pk>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
    
    # Novo fluxo de inscrição
    path('register/', views.AdventureSelectionView.as_view(), name='adventure_selection'),
    path('event/<int:event_id>/register/', views.EventRegistrationStartView.as_view(), name='registration_start'),
    path('event/<int:event_id>/debug/', views.EventRegistrationDebugView.as_view(), name='registration_debug'),
    path('event/<int:event_id>/check-cpf/', views.CheckCPFView.as_view(), name='check_cpf'),
    path('event/<int:event_id>/pre-registration/', views.PreRegistrationView.as_view(), name='pre_registration'),
    path('event/<int:event_id>/direct-registration/', views.DirectRegistrationView.as_view(), name='direct_registration'),
    
    path('pre-registration/<int:pre_registration_id>/success/', views.PreRegistrationSuccessView.as_view(), name='pre_registration_success'),
    
    path('booking/<int:booking_id>/payment-options/', views.PaymentOptionsView.as_view(), name='payment_options'),
    path('booking/<int:booking_id>/pix-payment/', views.PIXPaymentView.as_view(), name='pix_payment'),
    path('booking/<int:booking_id>/credit-card-payment/', views.CreditCardPaymentView.as_view(), name='credit_card_payment'),
    path('booking/<int:booking_id>/payment-success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    
    path('payment/check-status/', views.CheckPaymentStatusView.as_view(), name='check_payment_status'),
] 