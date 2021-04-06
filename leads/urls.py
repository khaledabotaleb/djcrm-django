from django.urls import path
from .views import (
    list_leads, lead_detail, lead_create, lead_update, delete_lead,
    ListLeadsView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView, CategoryListView,
    CatgeoryDetailView, LeadCategoryUpdateView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
)
app_name = 'leads'

urlpatterns = [

    path('', ListLeadsView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign_agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CatgeoryDetailView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete')
]