from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):       #inheriting the BaseUserManager class
    def create_user(self, email, password = None, **extra_fields):      
        if not email:       #if email is not set i.e our primary key is not set then we need to raise exception
            raise ValueError('The email should be set')
        email = self.normalize_email(email)         #this sets the email to a standard form irrespective to how it was typed (caps or no caps)    
        user = self.model(email = email, **extra_fields)        #create a new user instance
        user.set_password(password)         #this is used to hash the password and store it in the user instance
        user.save(using=self.db)        #saves the user instance to the database and using=self.db specifies the database alias
        return user

    def create_superuser(self, email, password = None, **extra_fields):
        #super user will have additional permission which are set true in addition to the normal user
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)