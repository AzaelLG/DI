from operaciones import suma, resta, multiplicacion, division

continuar = True

while continuar:

    num1 = int(input("Ingresa el primer número: "))
    num2 = int(input("Ingresa el segundo número: "))


    print("\n¿Qué operación deseas realizar?")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    opcion = input("Elige una opción (1-4): ")

    if opcion == "1":
        resultado = suma(num1, num2)
        print(f"\nResultado: {num1} + {num2} = {resultado}")
    elif opcion == "2":
        resultado = resta(num1, num2)
        print(f"\nResultado: {num1} - {num2} = {resultado}")
    elif opcion == "3":
        resultado = multiplicacion(num1, num2)
        print(f"\nResultado: {num1} * {num2} = {resultado}")
    elif opcion == "4":
        resultado = division(num1, num2)
        print(f"\nResultado: {num1} / {num2} = {resultado}")
    else:
        print("\nOpción no válida")

    respuesta = input("¿Quieres hacer más operaciones? (s/n): ").lower()
    if respuesta != "s":
        continuar = False
        print("¡Hasta luego!")