from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Add
from django.contrib import messages

from match.models import Human, Subject, Matched, Wantmatch, Profile, Tutor, Student, Review, Chatroomname

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from match.forms import SignUpForm, ProfileForm, ProfileUpdateForm


def home(request):
    count = User.objects.count()
    username = None

    if request.user.is_authenticated:
        username = request.user.username
        if not Human.objects.filter(name=username).exists():
            user1 = Human(name=username)
            user1.save()
        currentu = Human.objects.get(name=request.user.username)
        wantmatchcount = currentu.wantmatch.all().count
        return render(request, 'home.html', {
            'new_subject': request.POST.get('item_subject', ''), 'wantmatchcount': wantmatchcount, "count": count
        })
    else:
        return redirect('login')


# Sign Up View
# class SignUpView(CreateView):
# form_class = SignUpForm
# success_url = reverse_lazy('login')
# template_name = 'registration/signup.html'
def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username_signup = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username_signup}!')

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# Edit Profile View
def profile_view(request):
    if request.method == 'POST':
        form_class = ProfileForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if form_class.is_valid() and p_form.is_valid():
            form_class.save()
            p_form.save()
            messages.success(request, f'You account has been Updated!')
            return redirect('ProfileView')
    else:
        form_class = ProfileForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    user1 = Human.objects.get(name=request.user.username)
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()
    context = {'form_class': form_class, 'p_form': p_form, 'usercomall': usercommall, 'meanstar': meanstar}
    return render(request, 'registration/profile.html', context)


# class ProfileView(UpdateView):
# model = User
# form_class = ProfileForm
# p_form = ProfileUpdateForm
# success_url = reverse_lazy('home')
# template_name = 'registration/profile.html'

def about_app(request):
    return render(request, 'aboutus/about_app.html')


def about_group(request):
    return render(request, 'aboutus/about_group.html')


def request_match(request):
    Nosent = "No one sent you a matching"
    user1 = Human.objects.get(name=request.user.username)
    if user1.wantmatch.all():
        allwantmatch = user1.wantmatch.all()
        return render(request, "recievematch.html", {'allwantmatch': allwantmatch, 'count': allwantmatch.count()})
    return render(request, "recievematch.html", {'Nosent': Nosent})


# เข้าหน้า My tutor$student
def friend_matched(request):
    nomatched = "You didn't match anyone"
    user1 = Human.objects.get(name=request.user.username)
    if user1.tutor.all() or user1.student.all():
        alltutor = user1.tutor.all()
        allstudent = user1.student.all()

        countall = alltutor.count() + allstudent.count()
        return render(request, "Friend_matched.html",
                      {'alltutor': alltutor, 'allstudent': allstudent, 'count': countall})
    return render(request, "Friend_matched.html", {'Nomatched': nomatched})


def friend_profile(request, name):
    selecteduser = User.objects.get_by_natural_key(name)
    username = selecteduser.username

    user1 = Human.objects.get(name=name)
    sorted = [str(selecteduser.username), str(request.user.username)]
    sorted.sort()
    print(sorted[0])
    print(sorted[1])
    if not Chatroomname.objects.filter(name=sorted[0] + sorted[1]).exists():
        chatname = Chatroomname.objects.create(name=sorted[0] + sorted[1])
        chatname.save()
        chatnamer = Chatroomname.objects.get(name=sorted[0] + sorted[1])
        Human.objects.get(name=sorted[0]).chatroomname.add(chatnamer)
        Human.objects.get(name=sorted[1]).chatroomname.add(chatnamer)
    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (name in i.name):
            user2 = i.name
    # rating
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()

    # Profile
    user = User.objects.filter(username=username).first()
    user_profile = user.profile.image.url

    return render(request, 'Friend_profile.html', {'username': username, 'firstname': selecteduser.first_name
        , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username, 'usercomall': usercommall,
                                                   'user_profile': user_profile, 'id': user2, 'meanstar': meanstar})


def write_review_matched(request, profilename):
    user = User.objects.filter(username=profilename).first()
    user_profile = user.profile.image.url
    selecteduser = User.objects.get_by_natural_key(profilename)
    username = selecteduser.username
    user1 = Human.objects.get(name=profilename)
    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (profilename in i.name):
            user2 = i.name
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()
    if request.POST.get('item_review', ''):
        getrating = request.POST.getlist('star', '')
        if getrating:
            starrating = getrating[0]
        else:
            starrating = 0
        Review.objects.create(post=user1, realname=request.user.username, star=starrating,
                              message=request.POST.get('item_review', ''))

        usercommall = Review.objects.filter(post=user1)
        return render(request, 'Friend_profile.html', {'username': username, 'firstname': selecteduser.first_name
            , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                       'usercomall': usercommall, 'id': user2, 'meanstar': meanstar,
                                                       'user_profile': user_profile})
    else:
        nomessage = 'Please type your message before Review'
        usercommall = Review.objects.filter(post=user1)
        return render(request, 'Friend_profile.html', {'username': username, 'firstname': selecteduser.first_name
            , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'nomessage': nomessage, 'name': username,
                                                       'usercomall': usercommall, 'id': user2, 'meanstar': meanstar,
                                                       'user_profile': user_profile})


def view_r_profile(request, name):
    selecteduser = User.objects.get_by_natural_key(name)
    username = selecteduser.username

    # Profile
    user = User.objects.filter(username=username).first()
    user_profile = user.profile.image.url
    sorted = [str(selecteduser.username), str(request.user.username)]
    sorted.sort()
    print(sorted[0])
    print(sorted[1])
    if not Chatroomname.objects.filter(name=sorted[0] + sorted[1]).exists():
        chatname = Chatroomname.objects.create(name=sorted[0] + sorted[1])
        chatname.save()
        chatnamer = Chatroomname.objects.get(name=sorted[0] + sorted[1])
        Human.objects.get(name=sorted[0]).chatroomname.add(chatnamer)
        Human.objects.get(name=sorted[1]).chatroomname.add(chatnamer)
    user1 = Human.objects.get(name=name)
    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (name in i.name):
            user2 = i.name

    # rating
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()

    if usercommall.count() > 0:
        return render(request, 'recieve_profile.html', {'username': username, 'firstname': selecteduser.first_name
            , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                        'usercomall': usercommall, 'user_profile': user_profile,
                                                        'id': user2, 'meanstar': meanstar})
    else:
        Nocomment = "โนคอมเม้นเน้นคอมโบ"
        return render(request, 'recieve_profile.html', {'username': username, 'firstname': selecteduser.first_name
            , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                        'Nocomment': Nocomment, 'user_profile': user_profile,
                                                        'id': user2, 'meanstar': meanstar})


### other_perofile.html

def view_other_profile(request, name):
    selecteduser = User.objects.get_by_natural_key(name)
    username = selecteduser.username

    # Profile
    user = User.objects.filter(username=username).first()
    user_profile = user.profile.image.url
    sorted = [str(selecteduser.username), str(request.user.username)]
    sorted.sort()
    print(sorted[0])
    print(sorted[1])
    if not Chatroomname.objects.filter(name=sorted[0] + sorted[1]).exists():
        chatname = Chatroomname.objects.create(name=sorted[0] + sorted[1])
        chatname.save()
        chatnamer = Chatroomname.objects.get(name=sorted[0] + sorted[1])
        Human.objects.get(name=sorted[0]).chatroomname.add(chatnamer)
        Human.objects.get(name=sorted[1]).chatroomname.add(chatnamer)
    user1 = Human.objects.get(name=name)
    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (name in i.name):
            user2 = i.name

    # rating
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()
    if user1.wantmatch.filter(name=request.user.username):
        checked = 1
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
    else:
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username
                , 'usercomall': usercommall, 'id': user2, 'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})


def matching(request, name):
    selecteduser = User.objects.get_by_natural_key(name)
    username = selecteduser.username

    # Profile
    user = User.objects.filter(username=username).first()
    user_profile = user.profile.image.url

    if not Wantmatch.objects.filter(name=request.user.username).exists():
        firstwm = Wantmatch(name=request.user.username)
        firstwm.save()
    fwantmatch = Wantmatch.objects.get(name=request.user.username)
    Human.objects.get(name=name).wantmatch.add(fwantmatch)
    user2 = ''
    user1 = Human.objects.get(name=name)
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (name in i.name):
            user2 = i.name

    # rating
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if user1.wantmatch.filter(name=request.user.username):
        checked = 1
        usercommall = Review.objects.filter(post=user1)
        if usercommall.count() > 0:
            for i in usercommall:
                meanstar += i.star
            meanstar = meanstar // usercommall.count()
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
    else:
        usercommall = Review.objects.filter(post=user1)
        if usercommall.count() > 0:
            for i in usercommall:
                meanstar += i.star
            meanstar = meanstar // usercommall.count()
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})


def unmatching(request, name):
    selecteduser = User.objects.get_by_natural_key(name)
    username = selecteduser.username

    # Profile
    user = User.objects.filter(username=username).first()
    user_profile = user.profile.image.url

    user1 = Human.objects.get(name=name)
    # user1= Human.objects.get(pk=1).delete()
    user2 = get_object_or_404(Human, name=name)
    selected_unmatch = user2.wantmatch.get(name=request.user.username)
    user2.wantmatch.remove(selected_unmatch)

    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (name in i.name):
            user2 = i.name
    # rating
    meanstar = 0
    usercommall = Review.objects.filter(post=user1)
    if usercommall.count() > 0:
        for i in usercommall:
            meanstar += i.star
        meanstar = meanstar // usercommall.count()
    if user1.wantmatch.filter(name=request.user.username):
        checked = 1
        usercommall = Review.objects.filter(post=user1)
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'checked': checked, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
    else:
        usercommall = Review.objects.filter(post=user1)
        if usercommall.count() > 0:
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'Nocomment': Nocomment, 'id': user2,
                                                          'user_profile': user_profile, 'meanstar': meanstar})


def write_review(request, profilename):
    user = User.objects.filter(username=profilename).first()
    user_profile = user.profile.image.url
    selecteduser = User.objects.get_by_natural_key(profilename)
    username = selecteduser.username
    user1 = Human.objects.get(name=profilename)
    user2 = ''
    for i in user1.chatroomname.all():
        if (request.user.username in i.name) and (profilename in i.name):
            user2 = i.name
    meanstar = 0
    if user1.wantmatch.filter(name=request.user.username):
        checked = 1
        if request.POST.get('item_review', ''):
            getrating = request.POST.getlist('star', '')
            if getrating:
                starrating = getrating[0]
            else:
                starrating = 0
            Review.objects.create(post=user1, realname=request.user.username, star=starrating,
                                  message=request.POST.get('item_review', ''))

            usercommall = Review.objects.filter(post=user1)
            if usercommall.count() > 0:
                for i in usercommall:
                    meanstar += i.star
                meanstar = int(meanstar // usercommall.count())
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'checked': checked, 'id': user2,
                                                          'meanstar': meanstar, 'user_profile': user_profile})
        else:
            nomessage = 'Please type your message before Review'
            usercommall = Review.objects.filter(post=user1)
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'nomessage': nomessage,
                                                          'name': username, 'usercomall': usercommall,
                                                          'checked': checked, 'id': user2, 'meanstar': meanstar,
                                                          'user_profile': user_profile})

    else:
        if request.POST.get('item_review', ''):
            getrating = request.POST.getlist('star', '')
            if getrating:
                starrating = getrating[0]
            else:
                starrating = 0
            Review.objects.create(post=user1, realname=request.user.username, star=starrating,
                                  message=request.POST.get('item_review', ''))

            usercommall = Review.objects.filter(post=user1)
            if usercommall.count() > 0:
                for i in usercommall:
                    meanstar += i.star
                meanstar = int(meanstar // usercommall.count())
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'name': username,
                                                          'usercomall': usercommall, 'id': user2, 'meanstar': meanstar,
                                                          'user_profile': user_profile})
        else:
            nomessage = 'Please type your message before Review'
            usercommall = Review.objects.filter(post=user1)
            return render(request, 'other_profile.html', {'username': username, 'firstname': selecteduser.first_name
                , 'lastname': selecteduser.last_name, 'email': selecteduser.email, 'nomessage': nomessage,
                                                          'name': username, 'usercomall': usercommall, 'id': user2,
                                                          'meanstar': meanstar, 'user_profile': user_profile})


##### end other_profile.html

def un_friend_matched(request, name):
    myself = get_object_or_404(Human, name=request.user.username)
    if myself.student.filter(name=name).exists():
        Selunmatched = myself.student.get(name=name)
        myself.student.remove(Selunmatched)
    if myself.tutor.filter(name=name).exists():
        Selunmatched2 = myself.tutor.get(name=name)
        myself.tutor.remove(Selunmatched2)

    user2 = get_object_or_404(Human, name=name)
    if user2.tutor.filter(name=request.user.username).exists():
        Selunmatched3 = user2.tutor.get(name=request.user.username)
        user2.tutor.remove(Selunmatched3)
    if user2.student.filter(name=request.user.username).exists():
        Selunmatched4 = user2.student.get(name=request.user.username)
        user2.student.remove(Selunmatched4)

    myself.tutor.all()
    Nomatched = "You didn't match anyone"
    user1 = Human.objects.get(name=request.user.username)
    if user1.tutor.all() or user1.student.all():
        alltutor = user1.tutor.all()
        allstudent = user1.student.all()
        countall = alltutor.count() + allstudent.count()
        return render(request, "Friend_matched.html",
                      {'alltutor': alltutor, 'allstudent': allstudent, 'count': countall})
    return render(request, "Friend_matched.html", {'Nomatched': Nomatched})


def accept_match(request, name):
    selecteduser = User.objects.get_by_natural_key(request.user.username)
    username = selecteduser.username
    user1 = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    tutorself = get_object_or_404(Human, name=request.user.username)
    studentself = get_object_or_404(Human, name=name)
    selected_unmatch = tutorself.wantmatch.get(name=name)
    tutorself.wantmatch.remove(selected_unmatch)
    if not Student.objects.filter(name=name).exists():
        student = Student(name=name)
        student.save()
    if not Tutor.objects.filter(name=request.user.username).exists():
        tutor = Tutor(name=request.user.username)
        tutor.save()
    fstudent = Student.objects.get(name=name)
    ftutor = Tutor.objects.get(name=request.user.username)
    tutorself.student.add(fstudent)
    studentself.tutor.add(ftutor)
    Nosent = "No one sent you a matching"
    user1 = Human.objects.get(name=request.user.username)
    if user1.wantmatch.all():
        allwantmatch = user1.wantmatch.all()
        return render(request, "recievematch.html", {'allwantmatch': allwantmatch, 'count': allwantmatch.count()})
    return render(request, "recievematch.html", {'Nosent': Nosent})


def de_cline_match(request, name):
    selecteduser = User.objects.get_by_natural_key(request.user.username)
    username = selecteduser.username
    user1 = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    user2 = get_object_or_404(Human, name=request.user.username)
    selected_unmatch = user2.wantmatch.get(name=name)
    user2.wantmatch.remove(selected_unmatch)
    Nosent = "No one sent you a matching"
    user1 = Human.objects.get(name=request.user.username)
    if user1.wantmatch.all():
        allwantmatch = user1.wantmatch.all()
        return render(request, "recievematch.html", {'allwantmatch': allwantmatch, 'count': allwantmatch.count()})
    return render(request, "recievematch.html", {'Nosent': Nosent})


def searching(request):
    count = User.objects.count()
    user1 = Human.objects.get(name=request.user.username)
    subjectin = request.POST.get('item_subject2', '')
    subject1 = subjectin.lower().strip().replace(" ", "")
    if not Subject.objects.filter(name=subject1).exclude(
            name=(subject.name for subject in user1.subject.all())).exists():
        Noresult = 'No users were found matching'
        return render(request, 'home.html', {'Noresult': Noresult, 'count': count, 'subjectin': subjectin})
    subinmyself = Subject.objects.filter(name=subject1)
    for subject in user1.subject.all():
        subinmyself = subinmyself.exclude(name=subject.name)
    if not subinmyself.exists():
        Noresult = 'No users were found matching'
        return render(request, 'home.html', {'Noresult': Noresult, 'count': count, 'subjectin': subjectin})
    firstsubject = Subject.objects.get(name=subject1)
    first = firstsubject.human_set.all().exclude(name=request.user.username)
    second = firstsubject.human_set.all().exclude(name=request.user.username)
    for tutor in user1.tutor.all():
        first = first.exclude(name=tutor.name)
    for student in user1.student.all():
        first = first.exclude(name=student.name)
    for human_set in first:
        second = second.exclude(name=human_set.name)
    #    fisubject.add(Subject)
    return render(request, 'home.html',
                  {'usertutorstu': second, 'userins': first, 'count': count, 'subjectin': subjectin})


def profile_add_subject(request):
    user1 = Human.objects.get(name=request.user.username)
    checkremovebutton = 0
    if user1.subject.all().count() > 0:
        checkremovebutton = 1
    return render(request, 'add_subject.html', {
        'User': user1, 'checkremovebutton': checkremovebutton
    })


def add_subject(request):
    subject = request.POST.get('item_subject', '')
    subject = subject.lower().strip().replace(" ", "")
    if subject != '':
        if not Subject.objects.filter(name=subject).exists():
            firstsubject = Subject(name=subject)
            firstsubject.save()
        if not Human.objects.filter(name=request.user.username).exists():
            user1 = Human(name=request.user.username)
            user1.save()
        fsubject = Subject.objects.get(name=subject)
        Human.objects.get(name=request.user.username).subject.add(fsubject)
        user1 = Human.objects.get(name=request.user.username)
        checkremovebutton = 0
        if user1.subject.all().count() > 0:
            checkremovebutton = 1
        return render(request, 'add_subject.html', {
            'User': user1, 'checkremovebutton': checkremovebutton
        })
    else:
        fillyourbox = "Type your expert subject"
        user1 = Human.objects.get(name=request.user.username)
        checkremovebutton = 0
        if user1.subject.all().count() > 0:
            checkremovebutton = 1
        return render(request, 'add_subject.html', {
            'User': user1, 'checkremovebutton': checkremovebutton, 'fillyourbox': fillyourbox
        })


def clean_model(request):
    user1 = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    new_subject_list = request.POST.getlist('new_subject')
    checkremovebutton = 0

    if len(new_subject_list) == 0:
        # Redisplay the question voting form.
        if user1.subject.all().count() > 0:
            checkremovebutton = 1
        return render(request, 'add_subject.html', {
            'User': user1,
            'error_message': "You didn't select a subject.",
            'checkremovebutton': checkremovebutton
        })
    else:
        user2 = get_object_or_404(Human, name=request.user.username)
        for index in new_subject_list:
            print(index)
            selected_subject = user2.subject.get(pk=index)

            user2.subject.remove(selected_subject)
        if user1.subject.all().count() > 0:
            checkremovebutton = 1
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.

        return render(request, 'add_subject.html', {'User': user1, 'checkremovebutton': checkremovebutton})


def change_password_done(request):
    return render(request, 'registration/change_password_done.html')


def help_app(request):
    return render(request, 'help.html')
