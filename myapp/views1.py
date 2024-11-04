#Hai
from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
from .views2 import list_thong_bao
from .views import get_nguoidung, checklogin
from .views3 import add_chap_to_lichsu
# Create your views here.

# chức năng trang home

# top 3 truyện có lượt yêu thích cao nhất( slider trang home)
def top3_by_like():
	top3 = Truyen.objects.all().order_by('-luotthich')[:3]
	return top3

# top truyện mới tải lên chap mới
def new_update():
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

# top nhóm dịch có lượt xem nhiều nhất
def top_nhomdich(time):
	if time == 'tuan': # lọc theo tuần
		today = datetime.today()
		start_of_week = today - timedelta(days=today.weekday())
		end_of_week = start_of_week + timedelta(days=6)
		top_nhomdich = (
			Nguoidung.objects.filter(vaitro='nhomdich')
			.annotate(total_views=Coalesce(Sum('truyendang__chap__luotxem', filter=Q(truyendang__chap__thoigiandang__gte=start_of_week) & Q(truyendang__chap__thoigiandang__lte=end_of_week)),Value(0)))
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
	elif time == 'moiluc':
		top_nhomdich = (
			Nguoidung.objects.filter(vaitro='nhomdich')
			.annotate(total_views=Coalesce(Sum('truyendang__chap__luotxem'),Value(0)))
			.order_by('-total_views')[:5]
		)
		return top_nhomdich
	
def theloai(request, theloai): # view tìm truyện theo thể loại
	truyens = Truyen.objects.all()
	truyens_theo_the_loai = list()
	for x in truyens:
		if theloai in x.theloai:
			truyens_theo_the_loai.append(x)
	list_thong_baos = list_thong_bao(request)
	context={
		'theloai': theloai,
		'truyens_theo_the_loai': truyens_theo_the_loai,
		'list_thong_baos' : list_thong_baos,
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
	}
	return render(request, 'theloai.html', context)

def home(request): # view trang home
	top3 = top3_by_like()
	list_new_update = new_update()
	list_top_view = list()
	list_top_nhomdich = list()
	list_top_view_tuan = top_view('tuan')
	list_top_view_thang = top_view('thang')
	list_top_view_moiluc = top_view('moiluc')
	list_top_nhomdich_tuan = top_nhomdich('tuan')
	list_top_nhomdich_thang = top_nhomdich('thang')
	list_top_nhomdich_moiluc = top_nhomdich('moiluc')
	list_thong_baos = list_thong_bao(request)
	context = {
		'top3' : top3,
		'list_new_update': list_new_update,
		'list_top_view': list_top_view,
		'list_top_nhomdich': list_top_nhomdich,
		'list_top_view_tuan' : list_top_view_tuan,
		'list_top_view_thang' : list_top_view_thang,
		'list_top_view_moiluc' : list_top_view_moiluc,
		'list_top_nhomdich_tuan' : list_top_nhomdich_tuan,
		'list_top_nhomdich_thang' : list_top_nhomdich_thang,
		'list_top_nhomdich_moiluc' : list_top_nhomdich_moiluc,
		'list_thong_baos' : list_thong_baos,
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
	}
	return render(request, 'home.html', context)

def doc_tiep(request, id_truyen): # lấy ra chap đọc gần đây nhất của truyện này
	truyen = Truyen.objects.get(id=id_truyen)
	allchuong = list(truyen.chap.all().order_by('stt'))
	if checklogin(request):
		nguoidung = get_nguoidung(request)
		alllichsu = nguoidung.lichsu.all().order_by('-thoigiandoc')
		for x in alllichsu:
			if id_truyen == x.idtruyen:
				return Chap.objects.get(id = x.idchap)
		return allchuong[0]

def doctruyen(request, id): #view phan mota truyen
	# xử lý view phần doctruyen
	truyen = Truyen.objects.get(id=id)
	nhomdich = Nguoidung.objects.get(truyendang=truyen)
	sochuong = 0
	allchuong = list(truyen.chap.all().order_by('stt'))
	for x in truyen.chap.all():
		sochuong+=1
	truyen_cung_nhom_dich = nhomdich.truyendang.all()[:3]
	truyen_de_xuat = top_view('tuan')[:3]
	list_the_loai = truyen.theloai.split(",")
	list_thong_baos = list_thong_bao(request)
	# xử lý form khi người dùng thêm truyện vào yêu thích
	if request.method == 'POST':
		if 'btn-yeuthich' in request.POST:
			if checklogin(request):
				nguoidung = get_nguoidung(request)
				if truyen not in nguoidung.yeuthich.all():
					nguoidung.yeuthich.add(truyen)
			else:
				return redirect('login')
	chuong_gan_nhat = doc_tiep(request, id)
	context = {
		"truyen" : truyen,
		'nhomdich' : nhomdich,
		'sochuong' : sochuong,
		'allchuong' : allchuong,
		'truyen_cung_nhom_dich': truyen_cung_nhom_dich,
		'truyen_de_xuat' : truyen_de_xuat,
		'list_the_loai' : list_the_loai,
		'list_thong_baos' : list_thong_baos,
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
		'chuongdau': allchuong[0],
		'chuongmoinhat': allchuong[-1],
		'chuong_gan_nhat': chuong_gan_nhat,
	}
	return render(request, 'doctruyen.html', context)

def view_docchuong(request, id_truyen, id_chap): #đọc theo chương
	# hien thi
	truyen = Truyen.objects.get(id=id_truyen)
	chap = Chap.objects.get(id=id_chap)
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
		'nguoidung': get_nguoidung(request),
		'checklogin': checklogin(request)
	}
	return render(request, 'docchuong.html', context)
	
def test(request):
	return render(request, 'lichsu.html')

def timkiem(request):
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
		'checklogin': checklogin(request),
		'nguoidung': get_nguoidung(request),
	}
	return render(request, 'timkiem.html', context)







# def upload(request):
# 	if request.method == 'POST':
# 		if 'upload-truyen' in request.POST:
# 			form = TruyenForm(request.POST, request.FILES)
# 			if form.is_valid():
# 				form.save()
# 				print('save')
# 				return redirect('/admin')
# 			else:
# 				print('save not done')
# 				return render(request, 'home.html', {'form': form})
# 	return render(request, 'home.html')