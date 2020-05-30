"""
class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'cms/user_update.html'
    def get_success_url(self,request):
        #return resolve_url('cms:user_detail', pk=self.kwargs['pk'])
        form=UserUpdateForm(request.POST)
        if form.is_valid():
            User=AbstractUser()
            print(request)
            User.username=request.POST['username']
            User.twitter=request.POST['twitter']
            User.profile_picture=request.FILES['profile_picture']
            User.save()
            return redirect('cms:user_detail',pk=User.pk)
        else:
            form=UserUpdateForm()
        return render(request,'cms:user_detail',{'form':form})
"""