#Hai
from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung, Theloai
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
from .views2 import list_thong_bao,xoa_thong_bao
from .views import get_nguoidung, checklogin
from .views3 import add_chap_to_lichsu
# Create your views here.

# chức năng trang home

def top3_by_like(): # top 3 truyện có lượt yêu thích cao nhất( slider trang home)
	top3 = Truyen.objects.all().order_by('-luotthich')[:3] #lấy ra theo lượt thích
	return top3

def new_update(): # top truyện mới tải lên chap mới
	chaps = Chap.objects.all().order_by('-thoigiandang')
	new_update = list()
	for x in chaps:
		if x.truyen not in new_update:
			new_update.append(x.truyen)
	new_update = new_update[:12]
	return new_update

# lọc ra truyện nhiều view nhất trong tuần/tháng/all
def top_view(time): 
	if time == 'tuan': # lọc theo tuần
		today = datetime.today() 
		start_of_week = today - timedelta(days=today.weekday())
		end_of_week = start_of_week + timedelta(days=6)
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem', filter=Q(chap__thoigiandang__gte=start_of_week) 
			& Q(chap__thoigiandang__lte=end_of_week)),Value(0)))
			.order_by('-total_views')[:9]  # Lấy 9 truyện có lượt xem cao nhất trong tuần
		)
		return top_view
	elif time == 'thang': # lọc theo tháng
		this_month = datetime.today().month
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem', filter=Q(chap__thoigiandang__month=this_month)),Value(0)))
			.order_by('-total_views')[:9] # Lấy 9 truyện có lượt xem cao nhất trong tháng
		)
		return top_view
	elif time == 'moiluc': # lọc theo mọi lúc
		top_view = (
			Truyen.objects
			.annotate(total_views=Coalesce(Sum('chap__luotxem'),Value(0)))
			.order_by('-total_views')[:9]  # Lấy 9 truyện có lượt xem cao nhất trong mọi lúc
		)
		return top_view

# top nhóm dịch có lượt xem nhiều nhất
def top_nhomdich(time):
	if time == 'tuan': # lọc theo tuần
		today = datetime.today()
		start_of_week = today - timedelta(days=today.weekday())
		end_of_week = start_of_week + timedelta(days=6)
		top_nhomdich = (
			Nguoidung.objects.filter(vaitro='nhomdich')
			.annotate(total_views=Coalesce(Sum('truyendang__chap__luotxem', filter=Q(truyendang__chap__thoigiandang__gte=start_of_week) 
			& Q(truyendang__chap__thoigiandang__lte=end_of_week)),Value(0)))
			.order_by('-total_views')[:5]  # Lấy 5 người dùng có lượt xem cao nhất
		)
		return top_nhomdich
	elif time == 'thang': # lọc theo tháng
		this_month = datetime.today().month
		top_nhomdich = (
			Nguoidung.objects.filter(vaitro='nhomdich')
			.annotate(total_views=Coalesce(Sum('truyendang__chap__luotxem', filter=Q(truyendang__chap__thoigiandang__month=this_month)),Value(0)))
			.order_by('-total_views')[:5] # Lấy 9 truyện có lượt xem cao nhất trong tháng
		)
		return top_nhomdich
	elif time == 'moiluc': # lọc theo mọi lúc
		top_nhomdich = (
			Nguoidung.objects.filter(vaitro='nhomdich')
			.annotate(total_views=Coalesce(Sum('truyendang__chap__luotxem'),Value(0)))
			.order_by('-total_views')[:5]
		)
		return top_nhomdich
	
def theloai(request, theloai): # view tìm truyện theo thể loại
	xoa_thong_bao(request)
	truyens = Truyen.objects.all()
	truyens_theo_the_loai = list()
	for x in truyens:
		if theloai in x.theloai: # kiểm tra xem thể loại từ request có nằm trong truyện
			truyens_theo_the_loai.append(x)
	list_thong_baos = list_thong_bao(request)
	context={
		'theloai': theloai,
		'truyens_theo_the_loai': truyens_theo_the_loai,
		'list_thong_baos' : list_thong_baos,
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
	}
	return render(request, 'theloai.html', context)

def home(request): # view trang home
	xoa_thong_bao(request)
	context = { # truyền vào html
		'top3' : top3_by_like(), # lấy ra 3 truyện có lượt thích cao nhất
		'list_new_update' : new_update(), # lấy ra các truyện có thời gian cập nhật gần đây
		'list_top_view_tuan' : top_view('tuan'), # truyện view theo tuần, tháng, mọi lúc
		'list_top_view_thang' : top_view('thang'), 
		'list_top_view_moiluc' : top_view('moiluc'), 
		'list_top_nhomdich_tuan' : top_nhomdich('tuan'), # nhóm dịch có tổng số view cao nhất theo tuần, tháng, mọi lúc
		'list_top_nhomdich_thang' : top_nhomdich('thang'),
		'list_top_nhomdich_moiluc' : top_nhomdich('moiluc'),
		'list_thong_baos' : list_thong_bao(request),
		# thanh nav
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
	}
	return render(request, 'home.html', context)

def doc_tiep(request, id_truyen): # lấy ra chap đọc gần đây nhất của truyện này
	truyen = Truyen.objects.get(id=id_truyen)
	allchuong = list(truyen.chap.all().order_by('stt'))
	if not allchuong:
		return False
	if checklogin(request):
		nguoidung = get_nguoidung(request)
		alllichsu = nguoidung.lichsu.all().order_by('-thoigiandoc')
		for x in alllichsu:
			if id_truyen == x.idtruyen:
				return Chap.objects.get(id = x.idchap)
		return allchuong[0]

def doctruyen(request, id): #view phan mota truyen
	xoa_thong_bao(request)
	# xử lý view phần doctruyen
	truyen = Truyen.objects.get(id=id)
	nhomdich = Nguoidung.objects.get(truyendang=truyen)
	sochuong = 0
	allchuong = list(truyen.chap.all().order_by('stt'))
	for x in truyen.chap.all():
		sochuong+=1
	# xử lý form khi người dùng thêm truyện vào yêu thích
	if request.method == 'POST':
		if 'btn-yeuthich' in request.POST:
			if checklogin(request):
				nguoidung = get_nguoidung(request)
				if truyen not in nguoidung.yeuthich.all():
					nguoidung.yeuthich.add(truyen)
				truyen.luotthich = truyen.yeuthich.count()
				truyen.save()
			else:
				return redirect('login')
		elif 'btn-huy-yeuthich' in request.POST:
			nguoidung = get_nguoidung(request)
			if truyen in nguoidung.yeuthich.all():
				nguoidung.yeuthich.remove(truyen)
			truyen.luotthich = truyen.yeuthich.count()
			truyen.save()
	if not allchuong:
		chuongdau = chuongmoinhat = False
	else:
		chuongdau = allchuong[0]
		chuongmoinhat = allchuong[-1]
	if checklogin(request):
		list_yeu_thich = get_nguoidung(request).yeuthich.all()
	else:
		list_yeu_thich = list()
	context = {
		"truyen" : truyen,
		'nhomdich' : nhomdich,
		'sochuong' : sochuong,
		'allchuong' : list(truyen.chap.all().order_by('stt')),
		'truyen_cung_nhom_dich': nhomdich.truyendang.all()[:3],
		'truyen_de_xuat' : top_view('tuan')[:3],
		'list_the_loai' : truyen.theloai.split(","),
		'chuongdau': chuongdau,
		'chuongmoinhat': chuongmoinhat,
		'chuong_gan_nhat': doc_tiep(request, id),#đọc chương gần nhất (trong lịch sử)
		'list_yeu_thich': list_yeu_thich,
		# thanh nav
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request),
		'list_thong_baos' : list_thong_bao(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
	}
	return render(request, 'doctruyen.html', context)

def view_docchuong(request, id_truyen, id_chap): #đọc theo chương
	xoa_thong_bao(request)
	# hien thi
	truyen = Truyen.objects.get(id=id_truyen)
	chap = Chap.objects.get(id=id_chap)
	chap.luotxem = chap.luotxem + 1
	chap.save()
	allchap = list(truyen.chap.all().order_by('stt'))
	chap_index = allchap.index(chap)
	try:
		chaptruoc = allchap[chap_index - 1]
	except:
		chaptruoc = 'none'
	try:
		chapsau = allchap[chap_index + 1]
	except:
		chapsau = 'none'
	alltrang = chap.trang.all().order_by('id')
	# thêm vào lịch sử
	add_chap_to_lichsu(request, id_truyen, id_chap)
	context = {
		'truyen': truyen,
		'chap': chap,
		'alltrang': alltrang,
		'chaptruoc': chaptruoc,
		'chapsau': chapsau,
		'allchuong': list(truyen.chap.all().order_by('stt')),
		'nhomdich': Nguoidung.objects.get(truyendang=truyen),
		#thanh nav
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
		'list_thong_baos' : list_thong_bao(request),
	}
	return render(request, 'docchuong.html', context)
	

def timkiem(request):
	xoa_thong_bao(request)
	timkiems = list()
	if request.method == 'POST':
		if 'btn-search' in request.POST:
			search_value = request.POST['search_value']
			for x in Truyen.objects.all().order_by('ten'):
				if search_value.strip().upper().replace(" ", "") in x.ten.upper().replace(" ", "") or x.ten.upper().replace(" ", "") in search_value.strip().upper().replace(" ", ""):
					timkiems.append(x)
	context = {
		'timkiems': timkiems,
		'search_value': request.POST['search_value'],
		#thanh nav
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
		'list_thong_baos' : list_thong_bao(request),
	}
	return render(request, 'timkiem.html', context)

def truyenmoicapnhat(request): # trang truyen moi cap nhat
	xoa_thong_bao(request)
	list_new_update = new_update()
	context = {
		'list_new_update': list_new_update,
				#thanh nav
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request),
		'list_the_loais': Theloai.objects.all().order_by('theloai'),
		'list_thong_baos' : list_thong_bao(request),
	}
	return render(request, 'truyenmoicapnhat.html', context)