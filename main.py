from flask import flask, jsonify
import requests
import os
app = Flask(__name__)
window_size = 10
window = []
api_urls = {'p':'http://20.244.56.144/test/primes','f':'http://20.244.56.144/test/Fibo','e':'http://20.244.56.144/test/even','r':'http://20.244.56.144/test/rand'}
def fetch_numbers(numberid):
  url = api_urls.get(numberid)
  try:
    response = requests.get(url,timeout = 0.5)
    if response.status_code==200:
      return response.json().get('numbers',[])
  except requests.exceptions.RequestException:
    return []
  return []
@app.route('/numbers/<numberid>',methods=['GET'])
def get_numbers(numberid):
  if numberid not in api_urls:
    return jsonify({'error':'Invalid numberid'}),400
  prev_state = window.copy()
  numbers = fetch_numbers(numberid)
  for num in numbers:
    if num not in windows:
      window.append(num)
      if len(window)>window_size:
        window.pop(0)
  curr_state = window.copy()
  avg = sum(window)/len(window) if window else 0
  response = {'windowPrevState':prev_state,'windowCurrState':curr_state,'numbers':numbers,'avg':round(avg,2)}
  return jsonify(response)
if __name__=='__main__':
  app.run(port = int(os.environ.get("PORT",9876)))
