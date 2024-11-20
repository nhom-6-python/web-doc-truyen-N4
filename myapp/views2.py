#Phuc
from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung, Theloai, Lichsu
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
from .views import get_nguoidung, checklogin
import base64

def post_thongbao(chap): # tạo thông báo
    thongbao = Thongbao()
    thongbao.theloai = "chương mới cập nhật!!"
    thongbao.noidung = f'chương {chap.stt} của truyện {chap.truyen.ten} đã được cập nhật, xem ngay !!!'
    thongbao.chap = chap
    thongbao.save()
    nguoidungs = Nguoidung.objects.all()
    for x in nguoidungs:
        if chap.truyen in x.yeuthich.all():
            x.thongbao.add(thongbao)

def list_thong_bao(request): # trả về list thông báo
    if checklogin(request):
        nguoidung = get_nguoidung(request)
        print(nguoidung)
        return nguoidung.thongbao.all()

def xoa_thong_bao(request):
    if request.method == 'POST': # xóa thông báo
        if 'btn-delete-noti' in request.POST:
            print('xoa thong bao')
            nguoidung = get_nguoidung(request)
            for x in list_thong_bao(request):
                print(x.chap.ten)
                nguoidung.thongbao.remove(x)
    return 0

def dangtruyen(request): # chức năng đang truyện của nhóm dịch
    nguoidung = get_nguoidung(request)
    if nguoidung.vaitro == 'nhomdich':
        if checklogin(request) :
            if request.method == 'POST':
                try:
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
                except:
                    redirect('/dangtruyen/') 
                return redirect(f'/truyen_id={truyen.id}/')
            context = {
                #thanh nav
                'nguoidung': get_nguoidung(request),
                'checklogin': checklogin(request),
                'list_the_loais': Theloai.objects.all().order_by('theloai'),
                'list_thong_baos' : list_thong_bao(request),
            }
            return render(request, 'dangtruyen.html', context)
    else:
        return redirect('/login/')
        
def truyencuaban(request): # trang quản lý truyện đã đăng
    xoa_thong_bao(request)
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
			.order_by('-total_views')[:9]  # Lấy 9 truyện có lượt xem cao nhất trong tuần
		)
		return top_view

def suatruyen(request, id): #trang sửa thông tin truyện
    nhomdich = get_nguoidung(request)
    truyensua = Truyen.objects.get(id=id)
    if truyensua not in nhomdich.truyendang.all():
        return redirect('/login/')
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
            try:
                truyensua.tacgia = request.POST['tacgia']
            except:
                pass
            try:
                truyensua.ten = request.POST['ten']
            except:
                pass
            try:
                truyensua.theloai = ""
            except:
                pass
            for x in request.POST.getlist('theloais'):
                truyensua.theloai += x + ','
            try:
                truyensua.mota = request.POST['mota']
            except:
                pass
            try:
                print('xoatruyen')
                idchapxoas = request.POST.getlist('idchapxoas')
                print(idchapxoas)
                for x in idchapxoas:
                    chap=Chap.objects.get(id=x)
                    chap.delete()
                    Lichsu.objects.filter(idchap=x).delete()
            except:
                pass
            truyensua.save()
            return redirect(f'/truyen_id={truyensua.id}/')
    if truyensua in nhomdich.truyendang.all(): #check xem bạn có phải nhóm dịch truyện này ko?
        xoa_thong_bao(request)
        sochuong = 0
        for x in truyensua.chap.all():
            sochuong+=1
        context = {
            "truyen" : truyensua,
            'nhomdich' : nhomdich,
            'sochuong' : sochuong,
            'allchuong' : list(truyensua.chap.all().order_by('stt')),
            'truyen_cung_nhom_dich': nhomdich.truyendang.all()[:3],
            'truyen_de_xuat' :top_view('tuan')[:3],
            'list_the_loai' : truyensua.theloai.split(","),
            # thanh nav
            'checklogin': checklogin(request),
            'nguoidung': get_nguoidung(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
            'list_thong_baos' : list_thong_bao(request),
        }
        return render(request, 'suatruyen.html', context)
    else:
        return redirect('/login/')

def themchap(request, id): # thêm chap mới
    xoa_thong_bao(request)
    nguoidung = get_nguoidung(request)
    truyen = Truyen.objects.get(id=id)
    try:
        sttchap = truyen.chap.all().order_by('-stt').first().stt
        sttchap = sttchap + 1
    except:
        sttchap = 1
    if truyen in nguoidung.truyendang.all():
        context = {
            'truyen': truyen,
            'sttchap': sttchap,
            # thanh nav
            'nguoidung': get_nguoidung(request),
            'checklogin': checklogin(request),
            'list_the_loais': Theloai.objects.all().order_by('theloai'),
            'list_thong_baos' : list_thong_bao(request),
        }
        return render(request, 'themchap.html', context)
    else:
        return redirect('/login/')

def previewchap(request, id):
    xoa_thong_bao(request)
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
                    #thanh nav
                    'nguoidung': get_nguoidung(request),
                    'checklogin': checklogin(request),
                    'list_the_loais': Theloai.objects.all().order_by('theloai'),
                    'list_thong_baos' : list_thong_bao(request),
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
                post_thongbao(chap)
                return redirect(f'/truyen_id={truyen.id}/chuong={chap.id}/')
    else:
        return redirect('/home/')
