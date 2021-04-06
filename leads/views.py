from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LeadForm, LeadModelForm, CustomCreateUserForm, AssignAgentForm, LeadCategoryUpdateForm, \
    CategoryModelForm
from .models import Lead, Agent, Category
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from agents.mixin import OrganizerAndLoginRequiredMixin


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomCreateUserForm

    def get_success_url(self):
        return reverse("login")


class LandingView(TemplateView):
    template_name = "landing.html"


def landing(request):
    return render(request, 'landing.html', )


class ListLeadsView(LoginRequiredMixin, ListView):
    template_name = 'leads/leads_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListLeadsView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


def list_leads(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/leads_list.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {"lead": lead}
    return render(request, 'leads/lead_detail.html', context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/create_lead.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # TODO SEND EMAIL
        send_mail(
            subject="A Lead has Been Created",
            message="Go to the Site To see The New Lead",
            from_email="test@test.com",
            recipient_list=['khaledbebo722@yahoo.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = form.cleaned_data['agent']
            # lead = Lead(
            #     first_name=first_name,
            #     last_name=last_name,
            #     age=age,
            #     agent=agent
            # )
            # lead.save()
            return redirect('/leads')
    context = {
        'form': form
    }
    return render(request, 'leads/create_lead.html', context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    # queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user
        # initial queryset for lead of the entir organization
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(instance=lead, data=request.POST)
        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # lead.first_name = first_name
            # lead.last_name = last_name
            # lead.age = age
            # lead.save()
            return redirect(f'/leads/{lead.pk}/')
    context = {
        "lead": lead,
        "form": form
    }
    return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    # queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user
        # initial queryset for lead of the entir organization
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


def delete_lead(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-list")


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
        return queryset


class CatgeoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(CatgeoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #
    #     context.update({
    #         "leads": leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
        return queryset


class CategoryCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/create_category.html'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/update_category.html'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
        return queryset
    # def form_valid(self, form):
    #     category = form.save(commit=False)
    #     category.organization = self.request.user.userprofile
    #     category.save()
    #     return super(CategoryUpdateView, self).form_valid(form)


class LeadCategoryUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    # queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={'pk': self.get_object().id})


class CategoryDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/category_delete.html'

    # queryset = Lead.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            # initial queryset for lead of the entir organization
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
        return queryset

    def get_success_url(self):
        return reverse("leads:category-list")
