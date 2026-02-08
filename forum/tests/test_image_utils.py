import io
import tempfile
from django.test import TestCase
from PIL import Image
from utils import image_utils

class ImageUtilsTest(TestCase):
    def create_test_image(self, format='JPEG', size=(100, 100), color=(255, 0, 0)):
        file = io.BytesIO()
        image = Image.new('RGB', size, color)
        image.save(file, format)
        file.name = f'test.{format.lower()}'
        file.seek(0)
        return file

    def test_optimize_image_returns_smaller_image(self):
        original = self.create_test_image(size=(500, 500))
        optimized = image_utils.optimize_image(original, max_size=(100, 100))
        self.assertIsNotNone(optimized)
        img = Image.open(optimized)
        self.assertLessEqual(img.size[0], 100)
        self.assertLessEqual(img.size[1], 100)

    def test_create_favicon_returns_ico(self):
        original = self.create_test_image(format='PNG', size=(64, 64))
        with tempfile.NamedTemporaryFile(suffix='.png') as temp:
            temp.write(original.read())
            temp.flush()
            temp.seek(0)
            # Mock an object with an open() method
            class MockImageField:
                def open(self, mode='rb'):
                    return open(temp.name, mode)
                name = temp.name
            ico = image_utils.create_favicon(MockImageField())
            self.assertIsNotNone(ico)
            self.assertTrue(hasattr(ico, 'read'))
