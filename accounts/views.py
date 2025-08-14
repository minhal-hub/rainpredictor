from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SignUpForm

class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
