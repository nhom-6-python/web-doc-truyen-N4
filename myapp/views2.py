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
            'list_the_loai': Theloai.objects.all().order_by('theloai'),
        }
        return render(request, 'dangtruyen.html', context)
    else:
        return redirect('/login/')
        
def truyencuaban(request):
    nhomdich = get_nguoidung(request)
    list_truyencuaban = list(nhomdich.truyendang.all().order_by('ten'))
    if request.method == 'POST':
        if 'btn-delete' in request.POST:
            id_theodoi_xoa = request.POST['id_theodoi_xoa']
            truyen_xoa = Truyen.objects.get(id=id_theodoi_xoa)
            nhomdich.truyendang.remove(truyen_xoa)
        return redirect('/truyencuaban/')
    context = {
        'list_truyencuaban': list_truyencuaban,
    }
    return render(request, 'truyencuaban.html', context)