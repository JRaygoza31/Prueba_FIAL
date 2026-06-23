import requests

ACCESS_TOKEN = "EAAXmcCj5Sz4BRSLmi7W45JRgPtvEWV1ZCYHjyoqZBz48Nnetr7S0Ifn7kQtEGc4rpowiJwnrWTCYHvSCrWu5E3iz5MLO0lZBnfd0Irlm5D6WLAAxYzJs7v5bQ2SvH3M0HqIZCJhZB1wjxWXh53U2hrYbr1S5GT8H0xRZBaE7kwetZBhPkWstd0bgU4ZA24iPUdSH86C87Ql7i7Nxri3CvTRv4T4JYdEbihkaZB5Cz6sVpr9ZBoyKr7yD5L8g4P7rKXXECSZBfhtdgrVxTesKiVa3HkZCUF0vRJEZD"

PHONE_NUMBER_ID = "1059660540573198"

url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "523113963847",
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

respuesta = requests.post(
    url,
    headers=headers,
    json=data
)

print(respuesta.text)