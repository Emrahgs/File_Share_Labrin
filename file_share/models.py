from django.db import models


class User(models.Model):
    #information's
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    
class Post(models.Model):
    #information's
    title = models.CharField(max_length=200)
    desc = models.TextField()
    file_field = models.FileField(upload_to='uploads/')

    #relation's
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # moderation's
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    #information's
    content = models.TextField()

    #relation's
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_index=True, related_name='comments')

    def __str__(self):
        return self.content