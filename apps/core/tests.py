from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.core.validators import validate_ecuadorian_cedula


class CedulaValidatorTests(TestCase):
	def test_valid_cedula(self):
		# Ejemplo de cédula ecuatoriana válida (puedes cambiar por una real de prueba)
		valid = '1710034065'
		# No debe lanzar excepción
		try:
			validate_ecuadorian_cedula(valid)
		except ValidationError:
			self.fail('validate_ecuadorian_cedula lanzó ValidationError para una cédula válida')

	def test_invalid_cedula_length(self):
		with self.assertRaises(ValidationError):
			validate_ecuadorian_cedula('12345')

	def test_invalid_cedula_checksum(self):
		# Mismo prefijo pero último dígito alterado
		with self.assertRaises(ValidationError):
			validate_ecuadorian_cedula('1710034064')
