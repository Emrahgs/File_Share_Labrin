from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import User, Post, Comment
from django.http import HttpResponse
from django.contrib import messages


class HomePageView(ListView):
    def get(self, request):
        all_post = Post.objects.all().order_by('-id')
        param = {'posts': all_post}
        return render(request, 'main/home.html', param)

    def post(self, request):
        """
        Create account system
        """
        user_name = request.POST['uname']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']

        if pwd1 == pwd2:
            add_user = User(username=user_name, password=pwd1)
            add_user.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('home')
        else:
            messages.warning(request, 'Passwords are not same.')
            return redirect('home')

        
class UploadView(ListView):
    def get(self, request, user_name):
        return render(request, 'main/upload_file.html')

    def post(self, request, user_name):
        filename = request.FILES['filename']
        title = request.POST['title']
        desc = request.POST['desc']

        user_obj = User.objects.get(username=user_name)
        upload_post = Post(user=user_obj, title=title, file_field=filename, desc=desc)
        upload_post.save()
        messages.success(request, 'Your post has been uploaded successfully')
        return render(request, 'main/upload_file.html')


class DeleteView(ListView):
    model = Post
    def get(self, request, post_id):
        user = request.session['user']
        delete_post = self.model.objects.get(id=post_id)
        delete_post.delete()
        messages.success(request, 'Your post has been deleted successfully')
        return redirect(f'/profile/{user}')


class SearchView(ListView):
    def get(self, request):
        query = request.GET['query']
        search_users = User.objects.filter(username__icontains=query)
        search_title = Post.objects.filter(title__icontains=query)
        search_desc = Post.objects.filter(desc__icontains=query)
        search_result = search_title.union(search_desc)
        param = {'query': query, 'search_result': search_result, 'search_users': search_users}
        return render(request, 'main/search.html', param)


class ProfileView(ListView):
    def get(self, request, user_name):
        user_obj = User.objects.get(username=user_name)
        user_posts = user_obj.post_set.all().order_by('-id')
        param = {'user_data': user_obj, 'user_posts': user_posts}
        return render(request, 'main/profile.html', param)


class LoginView(ListView):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        user_name = request.POST['uname']
        pwd = request.POST['pwd']
        user_exists = User.objects.filter(username=user_name, password=pwd).exists()
        if user_exists:
            request.session['user'] = user_name
            messages.success(request, 'You are logged in successfully')
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('home')


class LogoutView(ListView):
    def get(self, request):
        try:
            del request.session['user']
        except:
            return redirect('home')
        return redirect('home')