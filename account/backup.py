def login(request):
    if request.method == 'POST':
        print('sudah sampai masuk')
        form = LoginForm(request.POST)
        if form.is_valid():
            print('masuk is valid')
            initial = form.cleaned_data['initial']
            print(initial)
            password = form.cleaned_data['password']
            print(password)
            user = User.objects.filter(initial=initial, password=password)
            if user.exists():
                if user.is_user or user.is_manager == True:
                    return redirect('index')
                
                else:
                    context = {
                        'form' : form,
                        'messages' : 
                        [
                            {
                                'message':'Akun sudah ada',
                                'category' : 'info'
                            }
                        ]
                    }
                    return render(request, 'account/login.html', context)
            else:
                context = {
                    'form' : form,
                    'messages' : 
                    [
                        {
                            'message':'Salah',
                            'category' : 'info'
                        }
                    ]
                }
                return render(request, 'account/login.html', context)
    elif request.method == 'GET':
        form_class = LoginForm()
        context = {
            'form' : form_class
        }
        return render(request, 'account/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(initial=form.cleaned_data['initial']).exists():
                context = {
                    'form' : form,
                    'messages' : 
                    [
                        {
                            'message':'Akun sudah ada',
                            'category' : 'info'
                        }
                    ]
                }
                return render(request, 'account/register.html', context)
            else:
                user = User()
                user.full_name = form.cleaned_data["full_name"]
                # print(request.POST.get("namalengkap"))
                user.initial = form.cleaned_data["initial"]
                user.password = make_password(form.cleaned_data["password"], salt=None, hasher='default')
                user.save()
                context = {
                    'messages' : 
                    [
                        {
                            'message':'Registrasi berhasil, saat ini sedang diproses oleh Admin.',
                            'category' : 'primary'
                        }
                    ]
                }
                return render(request, 'account/login.html', context)

    elif request.method == 'GET':
        form_class = RegisterForm()
        context = {
            'form' : form_class
        }
        return render(request, 'account/register.html', context)



                    <div class="form-group">
                        <label for="{{ form.full_name.id_for_label }}">Nama Lengkap</label>
                        {{ form.full_name }}
                    </div>
                    <div class="form-group">
                        <label for="{{ form.initial.id_for_label }}">Inisial</label>
                        {{ form.initial }}
                    </div>
                    <div class="form-group">
                        <label for="{{ form.password.id_for_label }}">Password</label>
                        {{ form.password }}
                    </div>


    # context = {
    #     'messages' : 
    #     [
    #         {
    #             'message':'Berhasil tambah data',
    #             'category' :'success',
    #             'full_name' : request.session['full_name']
    #         }
    #     ]
    # }

            context = {
            'messages' : 
            [
                {
                    'message':'Berhasil ubah data',
                    'category' :'success',
                }
            ],
            'full_name' : request.session['full_name'],
            'data' : attendance,
        }


  <style>
    #slideup {
      position:fixed;
      bottom:0;
      background:#0243c9;
      color:#fafefa;
      width:100%;
      display:none;
      padding: 20px;
      z-index: 2;
    }
  </style>
  <button onclick="jQuery('#slideup').slideDown(1500);">"Slideup"</button>
  <button onclick="jQuery('#slideup').slideUp(1500);">"Slideup"</button>
  <div id="slideup">Could be a bottom cookie warning bar</div>

  # class RegisterForm(forms.Form):
#     full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nama Lengkap', 'required': True}))
#     initial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Inisial', 'required': True}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password', 'required': True}))

# class LoginForm(forms.Form):
#     initial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Inisial', 'required': True}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password', 'required': True}))

/* .jumbotron .icon {
    margin-left: auto;
    margin-right: auto;
    display: block;
} */


let kehadiran = document.getElementById('myCharts').getContext('2d');
let myPieCharts  = new Chart(kehadiran, {
  type: 'pie',
  data: {
        labels: ['Hadir', 'Tidak Hadir'],
        datasets: [{
            backgroundColor: ['#007bff','#f8f9fa'],
            data: {{ attend }}
        }]
    },
  options: {}
  });

let ctxx = document.getElementById('myChartss').getContext('2d');
let myPieChart  = new Chart(ctxx, {
  type: 'pie',
  data: {
        labels: ['Sehat', 'Sakit'],
        datasets: [{
            backgroundColor: ['#007bff','#f8f9fa'],
            data: {{ condition }}
        }]
    },
  options: {}
  });

$(document).ready(function(){
  $("#flip").click(function(){
    $("#panel").slideToggle("slow");
  });
});

<div id="slideupadd" class="panel">
<div class="container">
  <div class="modal-header">
    <h5 class="modal-title">TAMBAH DATA</h5>
    <button onclick="slideHideAdd()" type="button" class="close" data-dismiss="modal" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <form action="/add-edit-attend/" method="POST" style="height: 400px; overflow: auto;">
    {% csrf_token %}
    <div class="form-group" onchange="handleSelect()">
      <label for="name">Apakah kamu hari ini hadir?</label>
      <select class="form-control" id="attend" name="attend" required>
          <option name="attend">{{ data.attend }}</option>
          <optgroup label="Pilihan">
          <option value="Hadir">Hadir</option>
          <option value="Tidak Hadir">Tidak Hadir</option>
      </select>
    </div>

    <div class="form-group" id="reasonAttend" style="display: none;" onchange="handleSelect()">
      <label for="name">Mengapa kamu tidak hadir?</label>
      <select class="form-control" id="reasonAttends" name="reasonAttends" required>
          <option name="attend">{{ data.reasonAttends }}</option>
          <optgroup label="Pilihan">
          <option>Cuti</option>
          <option>Training</option>
      </select>
    </div>

    <div class="form-group" id="otherAttend" style="display: none;" onchange="handleSelect()">
      <label for="initial">Alasan tidak hadir</label>
      <input type="form" class="form-control" id="otherAttend" value="{{ data.otherAttend }}"  name="otherAttend" placeholder="Alasan tidak hadir" required>
    </div>
    
    <div class="form-group" onchange="handleSelectSick()">
      <label for="name">Kondisimu saat ini apa?</label>
      <select class="form-control" id="condition" name="condition" required>
          <option name="attend">{{ data.condition }}</option>
          <optgroup label="Pilihan">
          <option value="Sehat">Sehat</option>
          <option value="Sakit">Sakit</option>
      </select>
    </div>
    
    <div class="form-group" id="sickChoice" style="display: none;" onchange="handleSelectSick()">
      <label for="name">Kamu sakit apa?</label>
      <select class="form-control" id="sickChoices" name="sickChoices" required>
          <option name="attend">{{ data.sickChoices }}</option>
          <optgroup label="Pilihan">
          <option>Batuk</option>
          <option>Pilek</option>
      </select>
    </div>
    
    <div class="form-group" id="otherSick" style="display: none;" onchange="handleSelectSick()">
      <label for="initial">Alasan sakit lainnya</label>
      <input type="form" class="form-control" id="sick" value="{{ data.otherSicks }}" name="otherSicks" placeholder="Alasan sakit lainnya" required>
    </div>
    

    <div class="form-group" id="work_statuss" onchange="handleSelectWFO()">
      <label for="name">Kamu WFH / WFO?</label>
      <select class="form-control" id="work_status" name="work_status" required>
          <option name="attend">{{ data.work_status }}</option>
          <optgroup label="Pilihan">
          <option value="WFH">WFH</option>
          <option value="WFO">WFO</option>
      </select>
    </div>

    <div class="form-group" id="wfoStatus" style="display: none;" onchange="handleSelectWFO()">
      <label for="initial">Jadwal WFO jam berapa?</label>
      <select class="form-control" id="work_description" name="work_description" required>
          <option name="attend">{{ data.work_description }}</option>
          <optgroup label="Pilihan">
          <option>07.30 - 16.30</option>
          <option>08.30 - 17.30</option>
          <option>09.30 - 18.30</option>
      </select>
    </div>
    <button type="submit" class="btn btn-primary btn-block">Tambah Data</button>
  </form>
</div>
</div>

  <div class="d-flex justify-content-center">
    <li style="display: inline;"><a class="btn btn-outline-primary" style="width:150px" href="/my-attend-list/{{ data.id }}" role="button">Kembali</a></li>&nbsp;
    &nbsp;<li style="display: inline;"><button type="submit" class="btn btn-primary" style="width:150px">Ubah</button></li>
  </div>

      <div class="d-flex justify-content-center buttonisikehadiran">
      <a class="btn btn-outline-primary" href="/add-edit-attend" role="button">Berbeda</a></li>&nbsp;
      &nbsp;<a class="btn btn-primary" href="/add-same-attend" role="button">Sama</a></li>
    </div>

      <!-- <td><h5><a value="{{ data.id }}" onclick="getStuff(elem)" class="badge badge-primary">Detail</a></h5></td> -->
      <!-- <td><button onclick="getStuff({{ data.id }})">Get Stuff</button></td> -->

        <div class="d-flex justify-content-center">
            <li style="display: inline;">
                <a class="btn btn-primary btn-block" style="width:120px" href="" role="button">Mingguan</a>
            </li>
            &nbsp;
            &nbsp;
            <li style="display: inline;">
                <a class="btn btn-primary btn-block" style="width:120px" href="" role="button">Bulanan</a>
            </li>
            &nbsp;
            &nbsp;
            <li style="display: inline;">
                <a class="btn btn-primary btn-block" style="width:120px" href="" role="button">Semua Data</a>
            </li>
          </div>

                      <div class="container">
                  <div class="form-group row">
                      <label for="example-date-input" class="col-2">Tanggal</label>
                        <form href="/show-all-attend?date=date">
                          <div class="form-group " >
                            <input type="date" class="form-control col-7" name="date" id="sick">
                          </div>
                          <button type="submit" class="btn btn-info btn-block col-7">Cari</button>
                        </form>
                        <!-- <a class="col-3 btn btn-primary btn-block" href="" role="button">Terapkan</a> -->
                </div>
            </div>


                <nav class="navbar navbar-expand-lg navbar-dark bg-primary nav-top">
      <div class="container">
        <a class="navbar-brand" href="#"><b>HEI-ASYST</b></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ml-auto">
            <a class="nav-item nav-link" href="#">Data Kehadiran</a>
            <a class="nav-item nav-link" href="#">Data Akun</a>
            <a class="nav-item nav-link" href="#">Nama Session</a>
            <a class="nav-item nav-link" href="#">Keluar</a>
          </div>
        </div>
      </div>
    </nav>

        /* box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19); */
    /* box-shadow: 0 0 7px rgba(0, 0, 0, 0.2); */
    /* box-shadow: 0px -5px 5px rgba(0, 0, 0, 0.2); */
    /* border-radius: 20px; */
    /* height: 455px; */

    function slideShow(){
  jQuery('#slideup').slideDown(600);
  document.getElementById("backdrop").style.width = "100%";
  document.getElementById("backdrop").style.opacity = "0.5";    
}

function slideHide(){
  jQuery('#slideup').slideUp(600);
  document.getElementById("backdrop").style.width = "0";
  document.getElementById("backdrop").style.opacity = "0";
}

function slideShows(){
  jQuery('#slideups').slideDown(600);
  document.getElementById("backdrop").style.width = "100%";
  document.getElementById("backdrop").style.opacity = "0.5";    
}

function slideHides(){
  jQuery('#slideups').slideUp(600);
  document.getElementById("backdrop").style.width = "0";
  document.getElementById("backdrop").style.opacity = "0";
}
