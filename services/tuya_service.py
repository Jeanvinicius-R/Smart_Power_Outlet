import requests
import hashlib
import hmac
import time
import json

ACCESS_KEY = "9fgmjnangqu4ugq9fqqm"
SECRET_KEY = "bb97ef07970c488a96445a6485a60a1b"
DEVICE_ID  = "eb6a9b180e4b9704dbpwff"
BASE_URL   = "https://openapi.tuyaus.com"


def _sign(method, path, body, token=""):
    timestamp = str(int(time.time() * 1000))

    # Garante que o body serializado seja idêntico ao enviado
    if body:
        body_str = json.dumps(body, separators=(',', ':'))
    else:
        body_str = ""
    
    content_hash = hashlib.sha256(body_str.encode()).hexdigest()

    string_to_sign = "\n".join([method, content_hash, "", path])
    message = ACCESS_KEY + token + timestamp + string_to_sign

    sign = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest().upper()

    return sign, timestamp


def get_token():
    path = "/v1.0/token?grant_type=1"
    sign, timestamp = _sign("GET", path, None)

    headers = {
        "client_id":   ACCESS_KEY,
        "sign":        sign,
        "t":           timestamp,
        "sign_method": "HMAC-SHA256"
    }

    response = requests.get(BASE_URL + path, headers=headers)
    result = response.json()

    if not result.get("success"):
        raise Exception(f"Erro ao obter token: {result}")

    return result["result"]["access_token"]


def enviar_comando(value: bool):
    token = get_token()
    path  = f"/v1.0/iot-03/devices/{DEVICE_ID}/commands"
    body  = {"commands": [{"code": "switch_1", "value": value}]}

    sign, timestamp = _sign("POST", path, body, token)

    headers = {
        "client_id":    ACCESS_KEY,
        "access_token": token,
        "sign":         sign,
        "t":            timestamp,
        "sign_method":  "HMAC-SHA256",
        "Content-Type": "application/json"
    }

    # Usa a mesma serialização da assinatura
    response = requests.post(
        BASE_URL + path,
        data=json.dumps(body, separators=(',', ':')),
        headers=headers
    )
    return response.json()


def ligar():
    resultado = enviar_comando(True)
    return {"ok": resultado.get("success", False), "acao": "ligado"}


def desligar():
    resultado = enviar_comando(False)
    return {"ok": resultado.get("success", False), "acao": "desligado"}


def get_status():
    try:
        token = get_token()
        path  = f"/v1.0/iot-03/devices/{DEVICE_ID}/status"

        sign, timestamp = _sign("GET", path, None, token)

        headers = {
            "client_id":    ACCESS_KEY,
            "access_token": token,
            "sign":         sign,
            "t":            timestamp,
            "sign_method":  "HMAC-SHA256"
        }

        response = requests.get(BASE_URL + path, headers=headers)
        data = response.json().get("result", [])

        status = {item["code"]: item["value"] for item in data}

        return {
            "ligada":  status.get("switch_1", False),
            "watts":   round(status.get("cur_power",   0) / 10,   1),
            "volts":   round(status.get("cur_voltage", 0) / 10,   1),
            "amperes": round(status.get("cur_current", 0) / 1000, 3)
        }

    except Exception as e:
        return {
            "ligada": False,
            "watts": "--", "volts": "--", "amperes": "--",
            "erro": str(e)
        }