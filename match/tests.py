from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from match.views import *
from match.models import Human, Subject, WantMatch, Review, Matched, ChatRoomName, Tutor, Student, ChatLog

'''
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
        first_subject = Subject.objects.create(name='first_subject')
        first_user.subject.add(first_subject)

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
        self.assertEqual(found.func, sign_up_view())

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
        self.user_a = User.objects.create_user(username='testuser',
                                               first_name='firstname',
                                               password='Password12345',
                                               email='test@example.com')
        self.user_a.save()
        self.client.login(username='testuser', password='Password12345')

        found = resolve("/profile/")
        self.assertEqual(found.func, profile_view)

    def test_profile_url_resolve_to_profile_view(self):
        found = resolve("/profile/")
        self.assertEqual(found.func, profile_view)

    def test_profile_form(self):
        self.user_a = User.objects.create_user(username='testuser',
                                               first_name='firstname',
                                               password='Password12345',
                                               email='test@example.com')
        self.user_a.save()
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
        self.user_a = User.objects.create_user(username='testuser',
                                               first_name='firstname',
                                               password='Password12345',
                                               email='test@example.com')
        self.user_a.save()
        self.client.login(username='testuser', password='Password12345')

        response = self.client.get("/accounts/change_password/")
        self.assertTemplateUsed(response, template_name='registration/change_password.html')

    def test_change_password_page_form(self):
        self.user_a = User.objects.create_user(username='testuser',
                                               first_name='firstname',
                                               password='Password12345',
                                               email='test@example.com')
        self.user_a.save()
        self.client.login(username='testuser', password='Password12345')

        users = User.objects.get(username='testuser')
        hash_password_first = users.password

        users.set_password('Password67890')
        users.save()

        hash_password2 = users.password
        self.assertNotEquals(hash_password_first, hash_password2)


class AddSubject(TestCase):
    def test_add_subject(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        User.objects.create_user(username='detmon123', password='ohmpassword')
        self.client.login(username="kitsanapong", password="kpassword")
        all_subject = Subject.objects.all()
        self.assertEqual(all_subject.count(), 0)
        self.client.post(f'/add_subject/', {'item_subject': 'mathematic'})
        all_subject = Subject.objects.all()
        self.assertEqual(all_subject.count(), 1)


class SearchTest(TestCase):
    def test_search_subject(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        User.objects.create_user(username='detmon123', password='ohmpassword')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        pasakornh = Human.objects.create(name='pasakorn')
        detmonh = Human.objects.create(name='detmon123')
        # kitsanapong login
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_result = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_result)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_result)
        self.client.login(username="kitsanapong", password="kpassword")
        physic = Subject.objects.create(name='physic')
        pasakornh.subject.add(physic)
        biology = Subject.objects.create(name='biology')
        detmonh.subject.add(biology)
        user_add_physic_subject = self.client.post(f'/write_review/{pasakornh.name}', {'item_subject2': 'physic'})
        self.assertContains(user_add_physic_subject, 'pasakorn')
        self.assertNotContains(user_add_physic_subject, 'detmon123')


class RequestTest(TestCase):

    def test_sent_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        self.client.login(username="kitsanapong", password="kpassword")
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_result = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_result)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_result)

        self.client.post(f'/matching/{pasakornh.name}')

        request_count = WantMatch.objects.all()
        print('wmcount =', request_count.count())
        self.assertEqual(request_count.count(), 1)

        first_want_match = request_count[0]

        self.assertEqual(first_want_match.name, 'kitsanapong')

    def test_cancel_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')
        self.client.login(username="kitsanapong", password="kpassword")

        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_request = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_request)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_request)

        self.client.post(f'/matching/{pasakornh.name}')

        request_to_other = pasakornh.want_match.filter(name='kitsanapong')
        self.assertEqual(request_to_other.count(), 1)

        self.client.post(f'/unmatching/{pasakornh.name}')

        request_to_other = pasakornh.want_match.filter(name='kitsanapong')
        self.assertEqual(request_to_other.count(), 0)

    def test_accept_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_request = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_request)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_request)
        first_request = WantMatch.objects.create(name='pasakorn')
        Human.objects.get(name='kitsanapong').want_match.add(first_request)
        tutor_all = Tutor.objects.all()
        self.assertEqual(tutor_all.count(), 0)
        student_all = Student.objects.all()
        self.assertEqual(student_all.count(), 0)
        self.client.post(f'/acceptmatch/{pasakornh.name}')
        tutor_all = Tutor.objects.all()
        self.assertEqual(tutor_all.count(), 1)
        self.assertEqual(tutor_all[0].name, 'kitsanapong')
        student_all = Student.objects.all()
        self.assertEqual(student_all.count(), 1)
        self.assertEqual(student_all[0].name, 'pasakorn')

    def test_decline_request(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')

        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_r = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_r)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_r)
        first_request = WantMatch.objects.create(name='pasakorn')
        kitsanapongh.want_match.add(first_request)

        all_request_for_k_user = Human.objects.get(name='kitsanapong').want_match.filter(name='pasakorn')
        self.assertEqual(all_request_for_k_user.count(), 1)
        Human.objects.get(name='kitsanapong').want_match.add(first_request)

        self.client.post(f'/declinematch/{pasakornh.name}')
        all_request_for_k_user = Human.objects.get(name='kitsanapong').want_match.filter(name='pasakorn')
        self.assertEqual(all_request_for_k_user.count(), 0)

    def test_unmatched(self):
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        kitsanapongh = Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_r = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_r)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_r)
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
        chat_name = ChatRoomName.objects.create(name='kitsanapong' + 'pasakorn')
        chat_name.save()
        chat_name_r = ChatRoomName.objects.get(name='kitsanapong' + 'pasakorn')
        Human.objects.get(name='kitsanapong').chat_room_name.add(chat_name_r)
        Human.objects.get(name='pasakorn').chat_room_name.add(chat_name_r)

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
        test_room = ChatLog.objects.create(chatroom='room1')
        test_chatlog = 'Example_Chatlog_1'
        test_room.chatlo = test_chatlog
        test_room.save()

        all_user = ChatLog.objects.all()
        room_test_a = all_user[0]

        self.assertEqual(all_user.count(), 1)
        self.assertEqual(room_test_a.chatlo, 'Example_Chatlog_1')
'''


class DeleteReviewTest(TestCase):
    def test_remove_review(self):
        # create two user
        User.objects.create_user(username='kitsanapong', password='kpassword')
        User.objects.create_user(username='pasakorn', password='mpassword')
        pasakornh = Human.objects.create(name='pasakorn')
        Human.objects.create(name='kitsanapong')

        # kitsanapong login
        self.client.login(username="kitsanapong", password="kpassword")

        # he write review on pasakorn profile
        Review.objects.filter(post=pasakornh)
        self.client.post(f'/write_review_matched/{pasakornh.name}',
                         {'item_review': 'Your teaching is so bad.', 'star': [0, 0, 0, 0, ]}, follow=True)

        #  he saw his comment but he change his mind he want to delete comment
        total_review = Review.objects.filter(post=pasakornh).all()
        self.assertEqual(total_review.count(), 1)
        self.assertEqual(total_review[0].message, 'Your teaching is so bad.')

        # he  click on delete review button
        self.client.post(f'/remove_review/{total_review[0].id}/{pasakornh.name}', follow=True)

        # now his review is gone
        total_review = Review.objects.filter(post=pasakornh).all()
        self.assertEqual(total_review.count(), 0)
