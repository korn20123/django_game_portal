from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Game

class GameAppTests(TestCase):
    def setUp(self):
        # Testuser anlegen
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Ein Spiel für Tests
        self.game = Game.objects.create(title='Testspiel', price='9.99', user=self.user)

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'neuuser',
            'password': 'pass1234',
            'password2': 'pass1234',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='neuuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'neuuser',
            'password': 'pass1234',
            'password2': 'pass5678',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'die Passwörter stimmen nicht über ein.')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'falsch',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username oder passwort sind ungülltig')

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")

    def test_home_shows_user_games(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.game.title)

    def test_add_game_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add.html')

    def test_add_game_post(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('add'), {
            'game': 'Neues Spiel',
            'price': '19.99',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Game.objects.filter(title='Neues Spiel', user=self.user).exists())

    def test_delete_game_post(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('delete', args=[self.game.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Game.objects.filter(id=self.game.id).exists())

    def test_delete_game_only_owner(self):
        anderer_user = User.objects.create_user(username='anderer', password='pass')
        self.client.login(username='anderer', password='pass')
        response = self.client.post(reverse('delete', args=[self.game.id]))
        self.assertEqual(response.status_code, 404)  # darf nicht löschen

    def test_play_game_post_updates_last_played(self):
        import datetime
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('play', args=[self.game.id]))
        self.assertRedirects(response, reverse('home'))
        self.game.refresh_from_db()
        self.assertTrue(self.game.last_played is not None)

    def test_play_game_only_owner(self):
        anderer_user = User.objects.create_user(username='anderer', password='pass')
        self.client.login(username='anderer', password='pass')
        response = self.client.post(reverse('play', args=[self.game.id]))
        self.assertEqual(response.status_code, 404)  # darf nicht spielen

    def test_add_game_requires_login(self):
        response = self.client.get(reverse('add'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add')}")
