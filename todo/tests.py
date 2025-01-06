

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import CustomUserCreationForm, TaskForm

class TodoAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        
        # Create a test task
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task',
            completed=False
        )
        
        # Initialize the client
        self.client = Client()

    def test_signup_view(self):
        # Test GET request to signup page
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/signup.html')
        
        # Test POST request to signup page
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        # Test GET request to login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')
        
        # Test POST request to login page
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout_view(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword123')
        
        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_task_list_view(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword123')
        
        # Test GET request to task list page
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword123')
        
        # Test GET request to task create page
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')
        
        # Test POST request to create a new task
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'This is a new task',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpassword123')
        
        # Test GET request to task update view
        response = self.client.get(reverse('task_update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')
        
        # Test POST request to update the task
        response = self.client.post(reverse('tas…