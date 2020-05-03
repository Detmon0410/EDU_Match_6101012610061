from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Add
from django.contrib import messages
from match.models import Human, Subject, Matched, WantMatch, Profile, Tutor, Student, Review, ChatRoomName
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from match.forms import SignUpForm, ProfileForm, ProfileUpdateForm
from django.urls import reverse


# rename all functions
# rename all value

def home(request):  # this func will be index page
    count = User.objects.count()
    user_name = None

    if request.user.is_authenticated:
        user_name = request.user.username
        if not Human.objects.filter(name=user_name).exists():
            user1 = Human(name=user_name)
            user1.save()
        current_user = Human.objects.get(name=request.user.username)
        want_match_count = current_user.want_match.all().count
        return render(request, 'home.html', {
            'new_subject': request.POST.get('item_subject', ''), 'wantmatchcount': want_match_count, "count": count
        })
    else:
        return redirect('login')
    # this code will show register user


# Sign Up View
# class SignUpView(CreateView):
# form_class = SignUpForm
# success_url = reverse_lazy('login')
# template_name = 'registration/signup.html'
def sign_up_view(request):
    # will lead user to register page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_name_signup = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user_name_signup}!')

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# Edit Profile View
def profile_view(request):
    # this func will show user profiles
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
    user_a = Human.objects.get(name=request.user.username)
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_comment_all.count() > 0:
        for i in user_comment_all:
            mean_star += i.star
        mean_star = mean_star // user_comment_all.count()
    con_text = {'form_class': form_class, 'p_form': p_form, 'usercomall': user_comment_all, 'meanstar': mean_star}
    return render(request, 'registration/profile.html', con_text)


# class ProfileView(UpdateView):
# model = User
# form_class = ProfileForm
# p_form = ProfileUpdateForm
# success_url = reverse_lazy('home')
# template_name = 'registration/profile.html'

def about_app(request):
    # this func show app info
    return render(request, 'aboutus/about_app.html')


def about_group(request):
    # this func show group info
    return render(request, 'aboutus/about_group.html')


def request_match(request):
    # this func will made you can request match to other user
    no_sent = "No one sent you a matching"
    user_a = Human.objects.get(name=request.user.username)
    if user_a.want_match.all():
        all_want_match = user_a.want_match.all()
        return render(request, "recievematch.html", {'allwantmatch': all_want_match, 'count': all_want_match.count()})
    return render(request, "recievematch.html", {'Nosent': no_sent})


# เข้าหน้า My tutor$student
def friend_matched(request):
    # show tutor and student who got match by user
    no_matched = "You didn't match anyone"
    user_a = Human.objects.get(name=request.user.username)
    if user_a.tutor.all() or user_a.student.all():
        all_tutor = user_a.tutor.all()
        all_student = user_a.student.all()

        count_all = all_tutor.count() + all_student.count()
        return render(request, "Friend_matched.html",
                      {'alltutor': all_tutor, 'allstudent': all_student, 'count': count_all})
    return render(request, "Friend_matched.html", {'Nomatched': no_matched})


def friend_profile(request, name):
    # this func will show match user profiles
    selected_user = User.objects.get_by_natural_key(name)
    user_name = selected_user.username

    user_a = Human.objects.get(name=name)
    sorted_user = [str(selected_user.username), str(request.user.username)]
    sorted_user.sort()
    print(sorted_user[0])
    print(sorted_user[1])
    if not ChatRoomName.objects.filter(name=sorted_user[0] + sorted_user[1]).exists():
        chat_name = ChatRoomName.objects.create(name=sorted_user[0] + sorted_user[1])
        chat_name.save()
        chat_name_result = ChatRoomName.objects.get(name=sorted_user[0] + sorted_user[1])
        Human.objects.get(name=sorted_user[0]).chat_room_name.add(chat_name_result)
        Human.objects.get(name=sorted_user[1]).chat_room_name.add(chat_name_result)
    user_b = ''
    for i in user_a.chat_room_name.all():
        if (request.user.username in i.name) and (name in i.name):
            user_b = i.name
    # rating
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_comment_all.count() > 0:
        for i in user_comment_all:
            mean_star += i.star
        mean_star = mean_star // user_comment_all.count()

    # Profile
    user = User.objects.filter(username=user_name).first()
    user_profile = user.profile.image.url

    return render(request, 'Friend_profile.html', {'username': user_name, 'firstname': selected_user.first_name
        , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                   'usercomall': user_comment_all,
                                                   'user_profile': user_profile, 'id': user_b, 'meanstar': mean_star})


def write_review(request, profile_name):
    # this func will made you can write review and rating to other user
    user_a = Human.objects.get(name=profile_name)
    mean_star = 0
    # set up variable for use in this functions

    if request.POST.get('item_review', ''):
        # when user click send star ratting and comment
        get_rating = request.POST.getlist('star', '')
        if get_rating:
            star_rating = get_rating[0]

        else:
            star_rating = 0

        Review.objects.create(post=user_a, real_name=request.user.username, star=star_rating,
                              message=request.POST.get('item_review', ''))
        # receive star variable and message variable
        user_comment_all = Review.objects.filter(post=user_a)
        if user_comment_all.count() > 0:
            # when have comment
            for i in user_comment_all:
                mean_star += i.star
                # calculate new stars rating
        return redirect(reverse('friendprofile', args=(profile_name,)))
        # set all variable to render on friend profiles functions


def view_r_profile(request, name):
    # this func will show match request from other user
    selected_user = User.objects.get_by_natural_key(name)
    user_name = selected_user.username

    # Profile
    user = User.objects.filter(username=user_name).first()
    user_profile = user.profile.image.url
    sorted_user = [str(selected_user.username), str(request.user.username)]
    sorted_user.sort()
    print(sorted_user[0])
    print(sorted_user[1])
    if not ChatRoomName.objects.filter(name=sorted_user[0] + sorted_user[1]).exists():
        chat_name = ChatRoomName.objects.create(name=sorted_user[0] + sorted_user[1])
        chat_name.save()
        chat_name_result = ChatRoomName.objects.get(name=sorted_user[0] + sorted_user[1])
        Human.objects.get(name=sorted_user[0]).chat_room_name.add(chat_name_result)
        Human.objects.get(name=sorted_user[1]).chat_room_name.add(chat_name_result)
    user_a = Human.objects.get(name=name)
    user_b = ''
    for i in user_a.chat_room_name.all():
        if (request.user.username in i.name) and (name in i.name):
            user_b = i.name

    # rating
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_comment_all.count() > 0:
        for i in user_comment_all:
            mean_star += i.star
        mean_star = mean_star // user_comment_all.count()

    if user_comment_all.count() > 0:
        return render(request, 'recieve_profile.html', {'username': user_name, 'firstname': selected_user.first_name
            , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                        'usercomall': user_comment_all, 'user_profile': user_profile,
                                                        'id': user_b, 'meanstar': mean_star})
    else:
        no_comment = "โนคอมเม้นเน้นคอมโบ"
        return render(request, 'recieve_profile.html', {'username': user_name, 'firstname': selected_user.first_name
            , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                        'Nocomment': no_comment, 'user_profile': user_profile,
                                                        'id': user_b, 'meanstar': mean_star})


### other_perofile.html

def view_other_profile(request, name):
    # this func will show other user profiles
    selected_user = User.objects.get_by_natural_key(name)
    user_name = selected_user.username

    # Profile
    user = User.objects.filter(username=user_name).first()
    user_profile = user.profile.image.url
    sorted_user = [str(selected_user.username), str(request.user.username)]
    sorted_user.sort()
    print(sorted_user[0])
    print(sorted_user[1])
    if not ChatRoomName.objects.filter(name=sorted_user[0] + sorted_user[1]).exists():
        chat_name = ChatRoomName.objects.create(name=sorted_user[0] + sorted_user[1])
        chat_name.save()
        chat_name_result = ChatRoomName.objects.get(name=sorted_user[0] + sorted_user[1])
        Human.objects.get(name=sorted_user[0]).chat_room_name.add(chat_name_result)
        Human.objects.get(name=sorted_user[1]).chat_room_name.add(chat_name_result)
    user_a = Human.objects.get(name=name)
    user_b = ''
    for i in user_a.chat_room_name.all():
        if (request.user.username in i.name) and (name in i.name):
            user_b = i.name

    # rating
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_comment_all.count() > 0:
        for i in user_comment_all:
            mean_star += i.star
        mean_star = mean_star // user_comment_all.count()
    if user_a.want_match.filter(name=request.user.username):
        checked = 1
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'usercomall': user_comment_all, 'checked': checked,
                                                          'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
        else:
            no_comment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': no_comment, 'checked': checked, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
    else:
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name
                , 'usercomall': user_comment_all, 'id': user_b, 'user_profile': user_profile, 'meanstar': mean_star})
        else:
            no_comment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': no_comment, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})


def matching(request, name):
    # this func will made you can request matching to other user
    selected_user = User.objects.get_by_natural_key(name)
    user_name = selected_user.username

    # Profile
    user = User.objects.filter(username=user_name).first()
    user_profile = user.profile.image.url

    if not WantMatch.objects.filter(name=request.user.username).exists():
        first_Want_match = WantMatch(name=request.user.username)
        first_Want_match.save()
    first_time_want_match = WantMatch.objects.get(name=request.user.username)
    Human.objects.get(name=name).want_match.add(first_time_want_match)
    user_b = ''
    user_a = Human.objects.get(name=name)
    for i in user_a.chat_room_name.all():
        if (request.user.username in i.name) and (name in i.name):
            user_b = i.name

    # rating
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_a.want_match.filter(name=request.user.username):
        checked = 1
        user_comment_all = Review.objects.filter(post=user_a)
        if user_comment_all.count() > 0:
            for i in user_comment_all:
                mean_star += i.star
            mean_star = mean_star // user_comment_all.count()
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'usercomall': user_comment_all, 'checked': checked,
                                                          'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
        else:
            no_comment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': no_comment, 'checked': checked, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
    else:
        user_comment_all = Review.objects.filter(post=user_a)
        if user_comment_all.count() > 0:
            for i in user_comment_all:
                mean_star += i.star
            mean_star = mean_star // user_comment_all.count()
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'usercomall': user_comment_all, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
        else:
            no_comment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': no_comment, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})


def un_matching(request, name):
    # this func will made you can unmatch other user
    selected_user = User.objects.get_by_natural_key(name)
    user_name = selected_user.username

    # Profile
    user = User.objects.filter(username=user_name).first()
    user_profile = user.profile.image.url

    user_a = Human.objects.get(name=name)
    # user1= Human.objects.get(pk=1).delete()
    user_b = get_object_or_404(Human, name=name)
    selected_un_match = user_b.want_match.get(name=request.user.username)
    user_b.want_match.remove(selected_un_match)

    user_b = ''
    for i in user_a.chat_room_name.all():
        if (request.user.username in i.name) and (name in i.name):
            user_b = i.name
    # rating
    mean_star = 0
    user_comment_all = Review.objects.filter(post=user_a)
    if user_comment_all.count() > 0:
        for i in user_comment_all:
            mean_star += i.star
        mean_star = mean_star // user_comment_all.count()
    if user_a.want_match.filter(name=request.user.username):
        checked = 1
        user_comment_all = Review.objects.filter(post=user_a)
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'usercomall': user_comment_all, 'checked': checked,
                                                          'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': Nocomment, 'checked': checked, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
    else:
        user_comment_all = Review.objects.filter(post=user_a)
        if user_comment_all.count() > 0:
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'usercomall': user_comment_all, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})
        else:
            Nocomment = "โนคอมเม้นเน้นคอมโบ"
            return render(request, 'other_profile.html', {'username': user_name, 'firstname': selected_user.first_name
                , 'lastname': selected_user.last_name, 'email': selected_user.email, 'name': user_name,
                                                          'Nocomment': Nocomment, 'id': user_b,
                                                          'user_profile': user_profile, 'meanstar': mean_star})


##### end other_profile.html

def un_friend_matched(request, name):
    # this func will made you can unmatch in tutor/student page
    my_self = get_object_or_404(Human, name=request.user.username)
    if my_self.student.filter(name=name).exists():
        self_un_matched = my_self.student.get(name=name)
        my_self.student.remove(self_un_matched)
    if my_self.tutor.filter(name=name).exists():
        self_un_matched_seconds = my_self.tutor.get(name=name)
        my_self.tutor.remove(self_un_matched_seconds)

    user_b = get_object_or_404(Human, name=name)
    if user_b.tutor.filter(name=request.user.username).exists():
        self_un_matched_thirds = user_b.tutor.get(name=request.user.username)
        user_b.tutor.remove(self_un_matched_thirds)
    if user_b.student.filter(name=request.user.username).exists():
        self_un_matched_fourth = user_b.student.get(name=request.user.username)
        user_b.student.remove(self_un_matched_fourth)

    my_self.tutor.all()
    no_matched = "You didn't match anyone"
    user_a = Human.objects.get(name=request.user.username)
    if user_a.tutor.all() or user_a.student.all():
        all_tutor = user_a.tutor.all()
        all_student = user_a.student.all()
        count_all = all_tutor.count() + all_student.count()
        return render(request, "Friend_matched.html",
                      {'alltutor': all_tutor, 'allstudent': all_student, 'count': count_all})
    return render(request, "Friend_matched.html", {'Nomatched': no_matched})


def accept_match(request, name):
    # this func made you can accept match request
    selected_user = User.objects.get_by_natural_key(request.user.username)
    user_name = selected_user.username
    user_a = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    tutor_self = get_object_or_404(Human, name=request.user.username)
    student_self = get_object_or_404(Human, name=name)
    selected_un_match = tutor_self.want_match.get(name=name)
    tutor_self.want_match.remove(selected_un_match)
    if not Student.objects.filter(name=name).exists():
        student = Student(name=name)
        student.save()
    if not Tutor.objects.filter(name=request.user.username).exists():
        tutor = Tutor(name=request.user.username)
        tutor.save()
    first_student = Student.objects.get(name=name)
    first_tutor = Tutor.objects.get(name=request.user.username)
    tutor_self.student.add(first_student)
    student_self.tutor.add(first_tutor)
    no_sent = "No one sent you a matching"
    user_a = Human.objects.get(name=request.user.username)
    if user_a.want_match.all():
        all_want_match = user_a.want_match.all()
        return render(request, "recievematch.html", {'allwantmatch': all_want_match, 'count': all_want_match.count()})
    return render(request, "recievematch.html", {'Nosent': no_sent})


def de_cline_match(request, name):
    # this func will made you can decline match request from other user
    selected_user = User.objects.get_by_natural_key(request.user.username)
    user_name = selected_user.username
    user_a = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    user_b = get_object_or_404(Human, name=request.user.username)
    selected_un_match = user_b.want_match.get(name=name)
    user_b.want_match.remove(selected_un_match)
    no_sent = "No one sent you a matching"
    user_a = Human.objects.get(name=request.user.username)
    if user_a.want_match.all():
        all_want_match = user_a.want_match.all()
        return render(request, "recievematch.html", {'allwantmatch': all_want_match, 'count': all_want_match.count()})
    return render(request, "recievematch.html", {'Nosent': no_sent})


def searching(request):
    # this func make user can search subject
    count = User.objects.count()
    user_a = Human.objects.get(name=request.user.username)
    subject_in = request.POST.get('item_subject2', '')
    subject_start = subject_in.lower().strip().replace(" ", "")
    if not Subject.objects.filter(name=subject_start).exclude(
            name=(subject.name for subject in user_a.subject.all())).exists():
        no_result = 'No users were found matching'
        return render(request, 'home.html', {'Noresult': no_result, 'count': count, 'subjectin': subject_in})
    subject_in_my_self = Subject.objects.filter(name=subject_start)
    for subject in user_a.subject.all():
        subject_in_my_self = subject_in_my_self.exclude(name=subject.name)
    if not subject_in_my_self.exists():
        no_result = 'No users were found matching'
        return render(request, 'home.html', {'Noresult': no_result, 'count': count, 'subjectin': subject_in})
    first_subject = Subject.objects.get(name=subject_start)
    first = first_subject.human_set.all().exclude(name=request.user.username)
    second = first_subject.human_set.all().exclude(name=request.user.username)
    for tutor in user_a.tutor.all():
        first = first.exclude(name=tutor.name)
    for student in user_a.student.all():
        first = first.exclude(name=student.name)
    for human_set in first:
        second = second.exclude(name=human_set.name)
    #    fisubject.add(Subject)
    return render(request, 'home.html',
                  {'usertutorstu': second, 'userins': first, 'count': count, 'subjectin': subject_in})


def profile_add_subject(request):
    # this func will lead you to subject page
    user_a = Human.objects.get(name=request.user.username)
    check_remove_button = 0
    if user_a.subject.all().count() > 0:
        check_remove_button = 1
    return render(request, 'add_subject.html', {
        'User': user_a, 'checkremovebutton': check_remove_button
    })


def add_subject(request):
    # this func will made you can add expert subject
    subject = request.POST.get('item_subject', '')
    subject = subject.lower().strip().replace(" ", "")
    if subject != '':
        if not Subject.objects.filter(name=subject).exists():
            first_subject = Subject(name=subject)
            first_subject.save()
        if not Human.objects.filter(name=request.user.username).exists():
            user_a = Human(name=request.user.username)
            user_a.save()
        start_subject = Subject.objects.get(name=subject)
        Human.objects.get(name=request.user.username).subject.add(start_subject)
        user_a = Human.objects.get(name=request.user.username)
        check_remove_button = 0
        if user_a.subject.all().count() > 0:
            check_remove_button = 1
        return render(request, 'add_subject.html', {
            'User': user_a, 'checkremovebutton': check_remove_button
        })
    else:
        fill_user_box = "Type your expert subject"
        user_a = Human.objects.get(name=request.user.username)
        check_remove_button = 0
        if user_a.subject.all().count() > 0:
            check_remove_button = 1
        return render(request, 'add_subject.html', {
            'User': user_a, 'checkremovebutton': check_remove_button, 'fillyourbox': fill_user_box
        })


def clean_model(request):
    # remove all subject in class subject
    user_a = Human.objects.get(name=request.user.username)
    # user1= Human.objects.get(pk=1).delete()
    new_subject_list = request.POST.getlist('new_subject')
    check_remove_button = 0

    if len(new_subject_list) == 0:
        # Redisplay the question voting form.
        if user_a.subject.all().count() > 0:
            check_remove_button = 1
        return render(request, 'add_subject.html', {
            'User': user_a,
            'error_message': "You didn't select a subject.",
            'checkremovebutton': check_remove_button
        })
    else:
        user_b = get_object_or_404(Human, name=request.user.username)
        for index in new_subject_list:
            print(index)
            selected_subject = user_b.subject.get(pk=index)

            user_b.subject.remove(selected_subject)
        if user_a.subject.all().count() > 0:
            check_remove_button = 1
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.

        return render(request, 'add_subject.html', {'User': user_a, 'checkremovebutton': check_remove_button})


def change_password_done(request):
    # this func will lead you to change password done page
    return render(request, 'registration/change_password_done.html')


def help_app(request):
    # this func will lead you to help page
    return render(request, 'help.html')


def remove_review(request, profile_name):
    if request.user.is_authenticated:
        object_id = int(request.POST['review_id'])
        review_delete = Review.objects.get(id=object_id)
        review_delete.delete()
        # delete comment review
        return redirect(reverse('friendprofile', args=(profile_name,)))
        # set all variable to friend profiles functions
    else:
        return redirect('login')