#Phuc
from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung, Theloai
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
from .views import get_nguoidung, checklogin
import base64

def list_thong_bao(request): # trả về list thông báo
    if checklogin(request):
        nguoidung = get_nguoidung(request)
        print(nguoidung)
        return nguoidung.thongbao.all()

def dangtruyen(request): # chức năng đang truyện của nhóm dịch
    nguoidung = get_nguoidung(request)
    if checklogin(request) :
        if request.method == 'POST':
            if 'btn-dangtruyen' in request.POST:
                theloais = request.POST.getlist('theloais')
                theloai = ""
                for x in theloais:
                    theloai += x + ","
                truyen = Truyen(
                    ten = request.POST['ten'],
                    theloai= theloai,
                    mota = request.POST['mota'],
                    tacgia = request.POST['tacgia'],
                    luotthich=0,
                    anhbia = request.FILES['anhbia'],
                    anhnen = request.FILES['anhnen'],
                )
                try:
                    truyen.save()
                except:
                    redirect('/dangtruyen/') 
                nguoidung.truyendang.add(truyen)

        context = {
            'checklogin': checklogin(request),
            'nguoidung': get_nguoidung(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
        }
        return render(request, 'dangtruyen.html', context)
    else:
        return redirect('/login/')
        
def truyencuaban(request): # trang quản lý truyện đã đăng
    nhomdich = get_nguoidung(request)
    list_truyencuaban = list(nhomdich.truyendang.all().order_by('ten'))
    if request.method == 'POST':
        if 'btn-delete' in request.POST:
            id_theodoi_xoa = request.POST['id_theodoi_xoa']
            truyen_xoa = Truyen.objects.get(id=id_theodoi_xoa)
            truyen_xoa.delete()
        return redirect('/truyencuaban/')
    context = {
        'list_truyencuaban': list_truyencuaban,
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
        'list_the_loais': Theloai.objects.all().order_by('theloai'),
    }
    return render(request, 'truyencuaban.html', context)

def top_view(time): 
	if time == 'tuan': # lọc theo tuần
		today = datetime.today()
		start_of_week = today - timedelta(days=today.weekday())
		end_of_week = start_of_week + timedelta(days=6)
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem', filter=Q(chap__thoigiandang__gte=start_of_week) & Q(chap__thoigiandang__lte=end_of_week)),Value(0)))
			.order_by('-total_views')[:10]  # Lấy 9 truyện có lượt xem cao nhất trong tuần
		)
		return top_view
	elif time == 'thang': # lọc theo tháng
		this_month = datetime.today().month
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem', filter=Q(chap__thoigiandang__month=this_month)),Value(0)))
			.order_by('-total_views')[:10] # Lấy 9 truyện có lượt xem cao nhất trong tháng
		)
		return top_view
	elif time == 'moiluc':
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem'),Value(0)))
			.order_by('-total_views')[:10]
		)
		return top_view

def suatruyen(request, id): #trang sửa thông tin truyện
    nhomdich = get_nguoidung(request)
    # list_truyencuaban = list(nhomdich.truyendang.all().order_by('ten'))
    truyensua = Truyen.objects.get(id=id)
    if request.method == 'POST':
        if 'btn-save-sua' in request.POST:
            try:
                truyensua.anhnen = request.FILES['anhnen']
            except:
                pass
            try:
                truyensua.anhbia = request.FILES['anhbia']
            except:
                pass
            truyensua.tacgia = request.POST['tacgia']
            truyensua.ten = request.POST['ten']
            truyensua.theloai = ""
            for x in request.POST.getlist('theloais'):
                truyensua.theloai += x + ','
            truyensua.mota = request.POST['mota']
            truyensua.save()
            return redirect(f'/truyen_id={truyensua.id}/')
    if truyensua in nhomdich.truyendang.all(): #check xem bạn có phải nhóm dịch truyện này ko?
        sochuong = 0
        allchuong = list(truyensua.chap.all().order_by('stt'))
        for x in truyensua.chap.all():
            sochuong+=1
        truyen_cung_nhom_dich = nhomdich.truyendang.all()[:3]
        truyen_de_xuat = top_view('tuan')[:3]
        list_the_loai = truyensua.theloai.split(",")
        list_thong_baos = list_thong_bao(request)
        context = {
            "truyen" : truyensua,
            'nhomdich' : nhomdich,
            'sochuong' : sochuong,
            'allchuong' : allchuong,
            'truyen_cung_nhom_dich': truyen_cung_nhom_dich,
            'truyen_de_xuat' : truyen_de_xuat,
            'list_the_loai' : list_the_loai,
            'list_thong_baos' : list_thong_baos,
            # thanh nav
            'checklogin': checklogin(request),
            'nguoidung': get_nguoidung(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
        }
        return render(request, 'suatruyen.html', context)
    else:
        return redirect('/login/')

def themchap(request, id): # thêm chap mới
    nguoidung = get_nguoidung(request)
    truyen = Truyen.objects.get(id=id)
    if truyen in nguoidung.truyendang.all():
        context = {
            'truyen': truyen,
            # thanh nav
            'nguoidung': get_nguoidung(request),
            'checklogin': checklogin(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
        }
        return render(request, 'themchap.html', context)
    else:
        return redirect('/login/')

def previewchap(request, id):
    if request.method == 'POST':
            if 'btn-dangtruyen' in request.POST:
                truyen = Truyen.objects.get(id=id)
                stt = request.POST['stt']
                ten = request.POST['ten']
                chap = Chap(stt = stt, ten=ten, truyen = truyen)
                alltrang_files = request.FILES.getlist('alltrang')
                alltrang_files.sort(key=lambda x: x.name) 
                # Lưu các file ảnh vào một danh sách để hiển thị
                alltrang = list()
                for x in alltrang_files:
                    anh = base64.b64encode(x.read()).decode('utf-8')
                    alltrang.append(anh)
                context = {
                    'alltrang' : alltrang,
                    'chap': chap,
                    'truyen': truyen,
                                # thanh nav
                    'nguoidung': get_nguoidung(request),
                    'checklogin': checklogin(request),
                    'list_the_loais': Theloai.objects.all().order_by('theloai'),
                }
                return render(request, 'previewchap.html', context)
            if 'btn-savechap' in request.POST:
                truyen = Truyen.objects.get(id=id)
                stt = request.POST['stt']
                ten = request.POST['ten']
                chap = Chap(stt = stt, ten=ten, truyen = truyen)
                chap.save()
                alltrang_files = request.FILES.getlist('alltrang')
                alltrang_files.sort(key=lambda x: x.name) 
                for x in alltrang_files:
                    Trang.objects.create(chap=chap, anh = x)
                return redirect(f'/truyen_id={truyen.id}/chuong={chap.id}/')
    else:
        return redirect('/home/')
