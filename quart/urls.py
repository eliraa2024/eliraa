from .views import (liraboletim_detail, BairroListView, BairroCreateView, BairroUpdateView, BairroDeleteView, LiraBoletimListView,
                    LiraBoletimCreateView,
                    LiraBoletimUpdateView,
                    LiraBoletimDeleteView,
                    lira_boletim_dado_list_view,
                    lira_boletim_dado_create_view,
                    LiraBoletimDadoUpdateView,
                    LiraBoletimDadoDeleteView,
                    lira_boletim_dado_detail,
                    indice,
                    indice_create_view,
                    mapa_dengue_caico,
                    CicloList)

from django.urls import path

urlpatterns = [
    # Bairro
    path('bairro', BairroListView.as_view(), name='bairro_list'),
    path('bairro/create/', BairroCreateView.as_view(), name='bairro_create'),
    path('bairro/<int:pk>/update/',
         BairroUpdateView.as_view(), name='bairro_update'),
    path('bairro/<int:pk>/delete/',
         BairroDeleteView.as_view(), name='bairro_delete'),
    # Lira boetim
    path('lira-boletim/', LiraBoletimListView.as_view(), name='lira_boletim_list'),
    path('lira-boletim/create/', LiraBoletimCreateView.as_view(),
         name='lira_boletim_create'),
    path('lira-boletim/<str:pk>/update/',
         LiraBoletimUpdateView.as_view(), name='lira_boletim_update'),
    path('lira-boletim/<str:pk>/delete/',
         LiraBoletimDeleteView.as_view(), name='lira_boletim_delete'),
    path('lira-boletim/<str:pk>', liraboletim_detail,
         name='liraboletim_detail'),
    # Lira boletim dados
    path('lira-boletim-dados/<str:pk>', lira_boletim_dado_list_view,
         name='lira_boletim_dado_list'),
    path('lira-boletim-dado/create/<str:pk>', lira_boletim_dado_create_view,
         name='lira_boletim_dado_create'),
    path('lira-boletim-dado/<str:pk>/update/',
         LiraBoletimDadoUpdateView.as_view(), name='lira_boletim_dado_update'),
    path('lira-boletim-dado/<str:pk>/delete/',
         LiraBoletimDadoDeleteView.as_view(), name='lira_boletim_dado_delete'),
    path('lira-boletim-dado/<str:pk>/', lira_boletim_dado_detail,
         name='lira_boletim_dado_detail'),
    # Indice
    path('indice/<str:ciclo>/', indice, name='indice'),
    path('indice/create/<str:pk>/', indice_create_view, name='indice_create'),
    # Ciclo
    path('ciclos/', CicloList.as_view(), name='ciclo'),
    # Mapa
    path('mapa/<str:ciclo>', mapa_dengue_caico, name='mapa'),
]
