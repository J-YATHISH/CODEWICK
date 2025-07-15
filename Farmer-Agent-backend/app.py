from flask import Flask
from flask_cors import CORS
from routes.advisory import advisory_bp
from routes.weather import weather_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(weather_bp, url_prefix="/weather")
app.register_blueprint(advisory_bp, url_prefix="/advisory")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
