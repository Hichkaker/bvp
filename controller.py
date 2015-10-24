from app import app
import twilio.twiml
import pdb

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
  resp = twilio.twiml.Response()

  resp.message("Press 1 for the nearest shelter, press 2 for the nearest meal.", action="/handle-key", method="POST")

  return str(resp)

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
  pdb.set_trace();
  digit_pressed = request.values.get('Digits', None)
  resp = twilio.twiml.Response()

  if digit_pressed == "1":
    resp.message("The nearest shelter is ...")
    return str(resp)
  elif digit_pressed == "2":
    resp.message("The nearest meal is ..!")
    return str(resp)
  else:
    return redirect("/")