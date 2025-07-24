# api/meu_endpoint_com_apikey.py

from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import os

# A CHAVE DEVE VIR DE UMA VARIÁVEL DE AMBIENTE DO VERCEL!
API_KEY_SECRETA = os.environ.get("MINHA_API_KEY")

class handler(BaseHTTPRequestHandler):
    def _verify_api_key(self):
        # Tenta pegar a chave do cabeçalho X-API-Key ou do query parameter 'api_key'
        api_key_header = self.headers.get('X-API-Key')

        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        api_key_param = dic.get('api_key')

        if not API_KEY_SECRETA: # Verifica se a chave secreta foi configurada
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "API Key não configurada no servidor."}).encode('utf-8'))
            return False

        if api_key_header == API_KEY_SECRETA or api_key_param == API_KEY_SECRETA:
            return True
        else:
            self.send_response(401) # Unauthorized
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Chave de API inválida ou ausente."}).encode('utf-8'))
            return False

    def do_GET(self):
        if not self._verify_api_key():
            return

        # ... seu código GET aqui ...
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with open('C:\Users\daniel.rios\Desktop\Bots\APIs bot Gemini\API\Relatorios.txt', 'r', encoding='utf-8') as f:
            texto_para_retornar = f.read()
        response_data = {'message': f'''{texto_para_retornar}
'''}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return

    def do_POST(self):
        if not self._verify_api_key():
            return

        # ... seu código POST aqui ...
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = {'message': 'POST liberado com API Key!'}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return