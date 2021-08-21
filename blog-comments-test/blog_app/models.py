from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    num_comments = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    num_replies = models.IntegerField(default=0, null=True, blank=True)
    path_id = models.TextField(default=None, null=True, blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(default=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        #update num_comments and path_id only for the first time its initialised
        if(self.path_id not in [None, '']):
            # print("path was already set")
            super().save(*args, **kwargs)
            return

        # print(self.parent_comment)
        if self.parent_comment is None:
            post = self.post
            num_comments = post.num_comments
            num_comments = num_comments + 1
            
            post.num_comments = num_comments
            post.save()

            self.path_id = str(num_comments)
            super().save(*args, **kwargs)
        else:
            parent = self.parent_comment
            num_rep = parent.num_replies
            num_rep = num_rep + 1

            parent.num_replies = num_rep
            parent.save()
            
            path = parent.path_id
            path = path+'-'+str(num_rep)
            self.path_id = path
            self.level = parent.level + 1
            super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)+' - '+self.content