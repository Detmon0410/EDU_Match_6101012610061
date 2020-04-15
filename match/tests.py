from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from match.views import *
from match.models import Human, Subject, Wantmatch, Review, Matched, Chatroomname, Tutor, Student, chatlog


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.post('/')
        self.assertRedirects(response, '/accounts/login/')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        response2 = self.client.post('/')
        self.assertTemplateUsed(response2, 'home.html')


class HumanModelTest(TestCase):
    def test_saving_fav_subject(self):
        first_user = Human.objects.create(name='first_user')
        firstsubject = Subject.objects.create(name='first_subject')
        first_user.subject.add(firstsubject)

        second_user = Human.objects.create(name='second_user')
        second_subject = Subject.objects.create(name='second_subject')
        second_user.subject.add(second_subject)

        all_user = Human.objects.all()
        first_saved_user = all_user[0]
        second_saved_user = all_user[1]
        self.assertEqual(all_user.count(), 2)
        self.assertEqual(first_saved_user.subject.first().name, 'first_subject')
        self.assertEqual(second_saved_user.subject.first().name, 'second_subject')


class SignUpPageTests(TestCase):

    def test_signup_page_url(self):
        response = self.client.get("/signup/")
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_url_resolve_to_sign_up_view(self):
        found = resolve("/signup/")
        self.assertEqual(found.func, SignUpView)

    def test_sign_up_form(self):
        response = self.client.post("/signup/", {
            'username': 'testuser',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'Pasakorn24130',
            'password2': 'Pasakorn24130'
        })

        self.assertEqual(response.status_code, 302)  # 302 มีการเปลี่ยนเส้นทาง
        users = User.objects.all()
        self.assertEqual(users.count(), 1)


class ProfilePageTests(TestCase):

    def test_profile_page_url(self):
        self.user1 = User.objects.create_user(username='testuser',
                                              first_name='firstname',
                                              password='Password12345',
                                              email='test@example.com')
        self.user1.save()
        self.client.login(username='testuser', password='Password12345')

        found = resolve("/profile/")
        self.assertEqual(found.func, ProfileView)

    def test_profile_url_resolve_to_profile_view(self):
        found = resolve("/profile/")
        self.assertEqual(found.func, ProfileView)

    def test_profile_form(self):
        self.user1 = User.objects.create_user(username='testuser',
                                              first_name='firstname',
                                              password='Password12345',
                                              email='test@example.com')
        self.user1.save()
        self.client.login(username='testuser', password='Password12345')

        response = self.client.post("/profile/", {
            'first_name': 'Pasakorn',
            'email': 'test@example.com',
        })

        users = User.objects.filter(username='testuser').first()
        # print(users.first_name)

        self.assertEqual('Pasakorn', users.first_name)


class ChangePasswordPageTest(TestCase):
    def test_change_password_page_url(self):
        self.user1 = User.objects.create_user(username='testuser',
                                              first_name='firstname',
                                              password='Password12345',
                                              email='test@example.com')
        self.user1.save()
        self.client.login(username='testuser', password='Password12345')

        response = self.client.get("/accounts/change_password/")
        self.assertTemplateUsed(response, template_name='registration/change_password.html')

    def test_change_password_page_form(self):
        self.user1 = User.objects.create_user(username='testuser',
                                              first_name='firstname',
                                              password='Password12345',
                                              email='test@example.com')
        self.user1.save()
        self.client.login(username='testuser', password='Password12345')

        users = User.objects.get(username='testuser')
        hash_password1 = users.password

        users.set_password('Password67890')
        users.save()

        hash_password2 = users.password
        self.assertNotEquals(hash_password1, hash_password2)


class Addsubject(TestCase):
    def test_add_subject(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        User.objects.create_user(username='detmon123', password='ohmpassword')
        self.client.login(username="kitsanapong", password="kpassword")
        allsubject = Subject.objects.all()
        self.assertEqual(allsubject.count(), 0)
        self.client.post(f'/add_subject/', {'item_subject': 'mathematic'})
        allsubject = Subject.objects.all()
        self.assertEqual(allsubject.count(), 1)


class SearchTest(TestCase):
    def test_search_subject(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        User.objects.create_user(username='detmon123', password='ohmpassword')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        pasakornh = Human.objects.create(name='pasakorn')
        detmonh = Human.objects.create(name='detmon123')
        # kitsanapong login
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)
        self.client.login(username="kitsanapong", password="kpassword")
        physic = Subject.objects.create(name='physic')
        pasakornh.subject.add(physic)
        biology = Subject.objects.create(name='biology')
        detmonh.subject.add(biology)
        useraddphy = self.client.post(f'/write_review/{pasakornh.name}', {'item_subject2': 'physic'})
        self.assertContains(useraddphy, 'pasakorn')
        self.assertNotContains(useraddphy, 'detmon123')


class RequestTest(TestCase):

    def test_sent_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        self.client.login(username="kitsanapong", password="kpassword")
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)

        self.client.post(f'/matching/{pasakornh.name}')

        wmcount = Wantmatch.objects.all()
        print('wmcount =', wmcount.count())
        self.assertEqual(wmcount.count(), 1)

        firstwm = wmcount[0]

        self.assertEqual(firstwm.name, 'kitsanapong')

    def test_cancel_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        self.client.login(username="kitsanapong", password="kpassword")

        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)

        self.client.post(f'/matching/{pasakornh.name}')

        wmforpasa = pasakornh.wantmatch.filter(name='kitsanapong')
        self.assertEqual(wmforpasa.count(), 1)

        self.client.post(f'/unmatching/{pasakornh.name}')

        wmforpasa = pasakornh.wantmatch.filter(name='kitsanapong')
        self.assertEqual(wmforpasa.count(), 0)

    def test_accept_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)
        firstwm = Wantmatch.objects.create(name='pasakorn')
        Human.objects.get(name='kitsanapong').wantmatch.add(firstwm)
        ttall = Tutor.objects.all()
        self.assertEqual(ttall.count(), 0)
        stall = Student.objects.all()
        self.assertEqual(stall.count(), 0)
        self.client.post(f'/acceptmatch/{pasakornh.name}')
        ttall = Tutor.objects.all()
        self.assertEqual(ttall.count(), 1)
        self.assertEqual(ttall[0].name, 'kitsanapong')
        stall = Student.objects.all()
        self.assertEqual(stall.count(), 1)
        self.assertEqual(stall[0].name, 'pasakorn')

    def test_decline_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)
        firstwm = Wantmatch.objects.create(name='pasakorn')
        kitsanapongh.wantmatch.add(firstwm)

        allwmfork = Human.objects.get(name='kitsanapong').wantmatch.filter(name='pasakorn')
        self.assertEqual(allwmfork.count(), 1)
        Human.objects.get(name='kitsanapong').wantmatch.add(firstwm)

        self.client.post(f'/declinematch/{pasakornh.name}')
        allwmfork = Human.objects.get(name='kitsanapong').wantmatch.filter(name='pasakorn')
        self.assertEqual(allwmfork.count(), 0)

    def test_unmatched(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)
        stfirst = Student.objects.create(name='pasakorn')
        kitsanapongh.student.add(stfirst)
        ttfirst = Tutor.objects.create(name='kitsanapong')
        pasakornh.tutor.add(ttfirst)

        allstfork = Human.objects.get(name='kitsanapong').student.filter(name='pasakorn')
        self.assertEqual(allstfork.count(), 1)
        allttforp = Human.objects.get(name='pasakorn').tutor.filter(name='kitsanapong')
        self.assertEqual(allttforp.count(), 1)

        self.client.post(f'/unmatched/{pasakornh.name}')
        allstfork = Human.objects.get(name='kitsanapong').student.filter(name='pasakorn')
        self.assertEqual(allstfork.count(), 0)
        allttforp = Human.objects.get(name='pasakorn').tutor.filter(name='kitsanapong')
        self.assertEqual(allttforp.count(), 0)


class ReviewtTest(TestCase):
    def test_review(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        p = User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chatname = Chatroomname.objects.create(name='kitsanapong' + 'pasakorn')
        chatname.save()
        chatnamer = Chatroomname.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chatroomname.add(chatnamer)
        Human.objects.get(name='pasakorn').chatroomname.add(chatnamer)

        totalreview = Review.objects.filter(post=pasakornh)
        self.assertEqual(totalreview.count(), 0)
        self.client.post(f'/write_review/{pasakornh.name}',
                         {'item_review': 'Your teaching is so good.', 'star': [0, 0, 0, 0, ]})
        totalreview = Review.objects.filter(post=pasakornh).all()
        self.assertEqual(totalreview.count(), 1)
        self.assertEqual(totalreview[0].message, 'Your teaching is so good.')
        self.client.post(f'/write_review/{pasakornh.name}', {'item_review': 'You are so cool.', 'star': [0, 0, 0, 0, ]})
        totalreview = Review.objects.filter(post=pasakornh).all()
        self.assertEqual(totalreview.count(), 2)
        self.assertEqual(totalreview[0].message, 'Your teaching is so good.')
        self.assertEqual(totalreview[1].message, 'You are so cool.')


class ChattingTest(TestCase):
    def test_chatroom_template(self):
        response = self.client.post('/chat/roomtest/')
        self.assertTemplateUsed(response, template_name='chat/room.html')

    def test_chatlog_db(self):
        test_room = chatlog.objects.create(chatroom='room1')
        test_chatlog = 'Example_Chatlog_1'
        test_room.chatlo = test_chatlog
        test_room.save()

        all_user = chatlog.objects.all()
        roomtest1 = all_user[0]

        self.assertEqual(all_user.count(), 1)
        self.assertEqual(roomtest1.chatlo, 'Example_Chatlog_1')
