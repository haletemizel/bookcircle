import unittest
from app.models import User, Book

class TestUserModel(unittest.TestCase):
    def test_password_hashing(self):
        u = User(username='test_user', email='test@example.com')
        u.set_password('my_secure_password')
        # Şifrelerin düz metin olarak kaydedilmediğini kontrol et
        self.assertNotEqual(u.password_hash, 'my_secure_password')
        # Şifre doğrulama (check_password) fonksiyonunun çalıştığını test et
        self.assertTrue(u.check_password('my_secure_password'))
        self.assertFalse(u.check_password('wrong_password'))

class TestBookModel(unittest.TestCase):
    def test_book_creation(self):
        # Yeni bir kitap nesnesinin oluşturulabildiğini test et
        b = Book(
            title='1984',
            author='George Orwell',
            total_pages=328,
            series_name='Dystopian Classics'
        )
        self.assertEqual(b.title, '1984')
        self.assertEqual(b.author, 'George Orwell')
        self.assertEqual(b.total_pages, 328)
        self.assertEqual(b.series_name, 'Dystopian Classics')

if __name__ == '__main__':
    unittest.main()
