


from rest_framework import permissions 




class IsStafforReadOnly(permissions.IsAdminUser):#staff ise CRUD işlemleri yoksa sadece get işlemi yapsın diye 
# bir overread methodu yazıyoruz. Bunu IsAdmınUser dan inherit ediyoruz.
    #permission lar True/False dönerler
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: #kullanıcı yetlili değilse get dönsün
            return True
        return bool(request.user and request.user.is_staff) #kullanıcı login ve staffsa CRUD yapabilir.