import requests
import json

def GerarQrcode(Usuario,quantidade):
  url = "https://api.mercadopago.com/v1/payments"

  payload = json.dumps({
    "transaction_amount": 78*quantidade,
    "description": f"Confirmação de presença de {Usuario}",
    "payment_method_id": "pix",
    "payer": {
      "email": "ejesantos.outlook@gmail.com",
      "first_name": Usuario,
      "last_name": "User",
      #"identification": {
      #  "type": "CPF",
      #  "number": "19119119100"
      },

     # "address": {
     #   "zip_code": "06233200",
     #   "street_name": "Av. das Nações Unidas",
     #   "street_number": "3003",
     #   "neighborhood": "Bonfim",
     #   "city": "Osasco",
     #   "federal_unit": "SP"
     # }
    #}
  })
  headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': 'Bearer APP_USR-8994682358026592-102420-361da1d854dbdc35d9d7293c600ea73f-407100150',
    'X-Idempotency-Key': f"{Usuario}T"
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  Qrcode=response.json()
  Copia_e_Cola = Qrcode['point_of_interaction']['transaction_data']['qr_code']
  img = Qrcode['point_of_interaction']['transaction_data']['qr_code_base64']
  StatusPag = Qrcode['status']
  return Copia_e_Cola,img,StatusPag

print(GerarQrcode("ewerton",float("2")))
