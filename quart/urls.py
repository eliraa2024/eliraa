from .views import (LiraBoletim, liraboletim_detail, BairroListView, BairroCreateView, BairroUpdateView, BairroDeleteView,LiraBoletimListView,
    LiraBoletimCreateView,
    LiraBoletimUpdateView,
    LiraBoletimDeleteView,
    LiraBoletimDadoListView,
    LiraBoletimDadoCreateView,
    LiraBoletimDadoUpdateView,
    LiraBoletimDadoDeleteView,
    lira_boletim_dado_detail,
     indice, mapa_dengue_caico, CicloList)

from django.urls import path

urlpatterns = [
    path('index', LiraBoletim.as_view(), name='index'),
     ################# Bairro
    path('bairro', BairroListView.as_view(), name='bairro_list'),
    path('bairro/create/', BairroCreateView.as_view(), name='bairro_create'),
    path('bairro/<int:pk>/update/',
         BairroUpdateView.as_view(), name='bairro_update'),
    path('bairro/<int:pk>/delete/',
         BairroDeleteView.as_view(), name='bairro_delete'),
     ################### Lira boetim
    path('lira-boletim/', LiraBoletimListView.as_view(), name='lira_boletim_list'),
    path('lira-boletim/create/', LiraBoletimCreateView.as_view(),
         name='lira_boletim_create'),
    path('lira-boletim/<str:pk>/update/',
         LiraBoletimUpdateView.as_view(), name='lira_boletim_update'),
    path('lira-boletim/<str:pk>/delete/',
         LiraBoletimDeleteView.as_view(), name='lira_boletim_delete'),
    path('lira-boletim/<str:pk>', liraboletim_detail,
         name='liraboletim_detail'),
     ######### Lira boletim dados
    path('lira-boletim-dados/<str:pk>', LiraBoletimDadoListView,
         name='lira_boletim_dado_list'),
    path('lira-boletim-dado/create/<str:pk>', LiraBoletimDadoCreateView,
         name='lira_boletim_dado_create'),
    path('lira-boletim-dado/<str:pk>/update/',
         LiraBoletimDadoUpdateView.as_view(), name='lira_boletim_dado_update'),
    path('lira-boletim-dado/<str:pk>/delete/',
         LiraBoletimDadoDeleteView.as_view(), name='lira_boletim_dado_delete'),
    path('lira-boletim-dado/<str:pk>/', lira_boletim_dado_detail,
         name='lira_boletim_dado_detail'),
     ########## Indice
     path('indice/<str:ciclo>/', indice, name='indice'),
     ########## Ciclo
     path('ciclos/', CicloList.as_view(), name='ciclo'),
     ########### Mapa
     path('mapa/<str:ciclo>', mapa_dengue_caico, name='mapa'),
]
