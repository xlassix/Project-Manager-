from django.db.models import Q,Manager


class ProjectManager(Manager):
    use_in_migrations = True
    def create(self,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        print(extra_fields)
        data = self.model(**extra_fields)
        data.save(using=self._db)
    def update_user(self,username,data):
        Model=self.model()
        try:
            obj = Model.objects.get(Q(username__iexact=username))
            print(obj)
            for i,j in data.items():
                print(i,j)
            #obj.field = new_value
            #obj.save()
        except Model.DoesNotExist:
            raise ValueError("nice try")