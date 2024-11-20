#Hung
from django.shortcuts import render, redirect
from .forms import NguoidungForm
from .models import Nguoidung, Truyen, Chap, Lichsu, Theloai
from .views2 import list_thong_bao, xoa_thong_bao
from .views import get_nguoidung, checklogin
from django.utils import timezone


# Create your views here.

def index(request):
	return render(request, 'index.html')

def registerPage(request):
    xoa_thong_bao(request)
    if request.method == 'POST': # nhận vào form đăng ký 
        form = NguoidungForm(request.POST)
        ten = request.POST['ten']
        mk = request.POST['matkhau']
        nhaplaimk = request.POST['nhaplaimk']
        nguoiDungList = Nguoidung.objects.values_list('ten', flat = True)
        if form.is_valid() and mk == nhaplaimk and ten not in nguoiDungList: # kiểm tra mật khẩu có đung ko?
            form.save()
            return redirect('/login/')  # Chuyển hướng về login sau khi đăng ký thành công
        else: 
            context = {
                'register_failed': True,
            }
            return render(request, 'register.html', context)
    else:
        form = NguoidungForm()
    context = {
        # thanh nav
        'checklogin': checklogin(request),
        'nguoidung': get_nguoidung(request),
        'list_the_loais': Theloai.objects.all().order_by('theloai'),
    }    
    return render(request, 'register.html', context)
 
def loginPage(request):
    xoa_thong_bao(request)
    if request.method == 'POST': # nhận form đăng nhập
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
            context = {
                'login_failed': True,
                # thanh nav
                'checklogin': checklogin(request),
                'nguoidung': get_nguoidung(request),
                'list_the_loais': Theloai.objects.all().order_by('theloai'),
            }
            return render(request, 'login.html', context)
    else:
        form = NguoidungForm()
    context = {
                # thanh nav
                'checklogin': checklogin(request),
                'nguoidung': get_nguoidung(request),
                'list_the_loais': Theloai.objects.all().order_by('theloai'),
            }
    return render(request, 'login.html', context)

def dang_xuat(request):
    request.session.flush()  # Xóa tất cả session
    return redirect('home')

def get_truyen_yeuthich(request):
    xoa_thong_bao(request)
    # Lấy tên người dùng từ session
    ten_nguoidung = request.session.get('nguoidung', None)  # Kiểm tra session có chứa 'nguoidung'
    if ten_nguoidung:
        try:
            # Tìm đối tượng người dùng dựa trên tên
            nguoidung = Nguoidung.objects.get(ten=ten_nguoidung)
            # Lấy danh sách truyện yêu thích
            truyen_yeuthich = nguoidung.yeuthich.all()
            # Trả về kết quả hiển thị
            if request.method == 'POST':
                if 'btn-delete' in request.POST:
                    id_theodoi_xoa = request.POST['id_theodoi_xoa']
                    for x in truyen_yeuthich:
                        if str(x.id) == id_theodoi_xoa:
                            nguoidung.yeuthich.remove(x)
                    truyen = Truyen.objects.get(id=id_theodoi_xoa)
                    truyen.luotthich = truyen.yeuthich.count()
                    truyen.save()
                return redirect('/theodoi/')
            list_thong_baos = list_thong_bao(request)
            context = {
                'truyen_yeuthich': truyen_yeuthich,
                'list_thong_baos': list_thong_baos,
                'nguoidung': get_nguoidung(request),
                'list_the_loai': Theloai.objects.all().order_by('theloai'),
            }
            return render(request, 'theodoi.html', context)
        
        except Nguoidung.DoesNotExist:
            return redirect('login')  
    else:
        return redirect('login')

def get_lichsu(request):
    xoa_thong_bao(request)
    #kiểm tra xem đã đăng nhập chưa
    if checklogin(request) == False:
        return redirect('login')
    else: # hiển thị trang lịch sử
        nguoidung = get_nguoidung(request)
        alllichsu = nguoidung.lichsu.all().order_by('-thoigiandoc')
        dates = list() #luu tat ca ngay doc
        # xử lý theo lọc hoặc ko lọc
        if request.method == 'POST':
            if 'btn-delete' in request.POST:
                id_ls_xoa = request.POST['id_ls_xoa']
                for x in alllichsu:
                    if str(x.id) == id_ls_xoa:
                        x.delete()
                    elif x.thoigiandoc.date() not in dates:
                        dates.append(x.thoigiandoc.date())
                return redirect('/lichsu/')
            if 'btn-loc-ngay' in request.POST: # nút lọc
                for x in alllichsu:
                    if x.thoigiandoc.date() not in dates and str(x.thoigiandoc.date()) >= request.POST['start-date'] and str(x.thoigiandoc.date()) <= request.POST['end-date']:
                        dates.append(x.thoigiandoc.date())
        else:
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
        context = {
            'lichsu_theo_ngay' : lichsu_theo_ngays,
            #thanh nav
            'nguoidung': get_nguoidung(request),
            'checklogin': checklogin(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
            'list_thong_baos' : list_thong_bao(request),
        }
        return render(request, 'lichsu.html', context)
        
def add_chap_to_lichsu(request, id_truyen, id_chap):
    if checklogin(request): # thêm lịch sử chap khi đọc chap đó
        idchap = id_chap
        idtruyen = id_truyen
        truyen = Truyen.objects.get(id=id_truyen)  
        chap = Chap.objects.get(id=id_chap)
        stt = chap.stt
        tentruyen = truyen.ten
        anhbia = truyen.anhbia
        nguoidoc = get_nguoidung(request)
        lichsu = Lichsu(
            idchap = idchap,
            idtruyen = idtruyen,
            stt = stt,
            tentruyen = tentruyen,
            anhbia = anhbia,
            nguoidoc = nguoidoc,
        )
        for x in Lichsu.objects.filter(idtruyen=idtruyen, idchap=idchap):
            if x.thoigiandoc.date() == timezone.now().date():
                x.delete()
        lichsu.save()                   

def get_truyen_cua_nhomdich(request, ten):
    xoa_thong_bao(request)
    nhomdich = Nguoidung.objects.get(ten = ten)
    truyen_da_dang = nhomdich.truyendang.all()
    context = {
        'truyen_da_dang' : truyen_da_dang,
        'nhomdich': nhomdich,
		#thanh nav
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
		'list_thong_baos' : list_thong_bao(request),
    }
    return render(request, 'truyencuanhomdich.html', context)