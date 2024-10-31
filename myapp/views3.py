#Hung
from django.shortcuts import render, redirect
from .forms import NguoidungForm
from .models import Nguoidung
from .views2 import list_thong_bao
from .views import get_nguoidung, checklogin
# Create your views here.

def index(request):
	return render(request, 'index.html')

def registerPage(request):
    if request.method == 'POST':
        form = NguoidungForm(request.POST)
        ten = request.POST['ten']
        mk = request.POST['matkhau']
        nhaplaimk = request.POST['nhaplaimk']
        nguoiDungList = Nguoidung.objects.values_list('ten', flat = True)
        
        if form.is_valid() and mk == nhaplaimk and ten not in nguoiDungList:
            form.save()
            return redirect('login')  # Chuyển hướng về login sau khi đăng ký thành công

    else:
        form = NguoidungForm()
    return render(request, 'register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        form = NguoidungForm(request.POST)
            # Lấy dữ liệu từ form
        ten = request.POST['ten']
        matkhau = request.POST['matkhau']
        nguoiDungList = Nguoidung.objects.values_list('ten', 'matkhau')
        # Lưu tên người dùng vào session để theo dõi trạng thái đăng nhập
        if (ten, matkhau) in nguoiDungList:
            request.session['nguoidung'] = ten
            
            return redirect('home')  # Chuyển hướng về trang chủ sau khi đăng nhập thành công
    else:
        form = NguoidungForm()

    return render(request, 'login.html', {'form': form})

def dang_xuat(request):
    request.session.flush()  # Xóa tất cả session
    return redirect('home')

def get_truyen_yeuthich(request):
    # Lấy tên người dùng từ session
    ten_nguoidung = request.session.get('nguoidung', None)  # Kiểm tra session có chứa 'nguoidung'
    if ten_nguoidung:
        try:
            # Tìm đối tượng người dùng dựa trên tên
            nguoidung = Nguoidung.objects.get(ten=ten_nguoidung)
            # Lấy danh sách truyện yêu thích
            truyen_yeuthich = nguoidung.yeuthich.all()
            # Trả về kết quả hiển thị
            list_thong_baos = list_thong_bao(request)
            context = {
                'truyen_yeuthich': truyen_yeuthich,
                'list_thong_baos': list_thong_baos,
            }
            return render(request, 'theodoi.html', context)
        
        except Nguoidung.DoesNotExist:
            return redirect('login')  
    else:
        return redirect('login')

def get_lichsu(request):
    if checklogin(request) == False:
        return redirect('login')
    else:
        nguoidung = get_nguoidung(request)
        alllichsu = nguoidung.lichsu.all().order_by('-thoigiandoc')
        dates = list() #luu tat ca ngay doc
        for x in alllichsu:
            if x.thoigiandoc.date() not in dates:
                dates.append(x.thoigiandoc.date())

        lichsu_theo_ngays = list() #luu tat ca cac truyen cua tung ngay
        for i in dates:
            history = []
            for lsu in alllichsu:
                if lsu.thoigiandoc.date() == i:
                    history.append(lsu)
            lichsu_theo_ngays.append(history)
        for x in lichsu_theo_ngays:
            for i in x:
                print(i.tentruyen, end = ' ')
            print()
        context = {
            'lichsu_theo_ngay' : lichsu_theo_ngays,
        }
        return render(request, 'lichsu.html', context)
        

