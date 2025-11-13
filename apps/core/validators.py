from django.core.exceptions import ValidationError


def validate_ecuadorian_cedula(value: str) -> None:
    """
    Valida una cédula ecuatoriana (10 dígitos) usando el algoritmo oficial.

    Lanza ValidationError si no es válida.
    """
    if value is None:
        raise ValidationError("Cédula vacía")

    # Aceptar solo dígitos y longitud 10
    ced = ''.join(ch for ch in str(value) if ch.isdigit())
    if len(ced) != 10:
        raise ValidationError("La cédula debe tener 10 dígitos")

    try:
        digits = [int(d) for d in ced]
    except ValueError:
        raise ValidationError("La cédula contiene caracteres inválidos")

    province = int(ced[0:2])
    third = digits[2]

    # Provincias válidas: 01-24 (y 30 para casos especiales)
    if not (1 <= province <= 24 or province == 30):
        raise ValidationError("Código de provincia inválido en la cédula")

    # Tercer dígito para personas naturales debe ser < 6
    if third >= 6:
        raise ValidationError("Cédula inválida para persona natural (tercer dígito)")

    # Algoritmo de validación (módulo 10)
    total = 0
    for i in range(9):
        num = digits[i]
        if i % 2 == 0:  # posiciones 0,2,4,6,8 (1,3,5,7,9) multiplicar por 2
            prod = num * 2
            if prod > 9:
                prod -= 9
            total += prod
        else:
            total += num

    next_ten = ((total + 9) // 10) * 10
    check_digit = next_ten - total
    if check_digit == 10:
        check_digit = 0

    if check_digit != digits[9]:
        raise ValidationError("Cédula ecuatoriana inválida (checksum no coincide)")

    # Si pasa todas las comprobaciones, no devuelve nada (valid)
