# api/application.py
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
import os
from scraper import main, scrape_prices, target_urls

socketio = None  # global reference for SocketIO if needed

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'outputs'

    # Initialize SocketIO with the app.
    global socketio
    socketio = SocketIO(app)

    # Ensure necessary folders exist
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            file = request.files.get('excel_file')
            if file and file.filename.endswith('.xlsx'):
                input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test.xlsx')
                file.save(input_path)
                try:
                    main()
                    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'merged.xlsx')
                    return send_file(output_path, as_attachment=True)
                except Exception as e:
                    return f"Error: {str(e)}"
        return render_template('index.html')

    @app.route('/search')
    def search():
        return render_template('search.html')

    @socketio.on('search_artikul')
    def handle_search_artikul(data):
        artikul = data.get('artikul')
        results = []
        for url in target_urls:
            prices = scrape_prices(url, artikul)
            results.append({
                'artikul': artikul,
                'url': url + artikul,
                'price': ", ".join(prices) if prices else "Не найдено"
            })
        emit('search_results', results)

    return app
