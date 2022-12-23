from app import create_app

app = create_app(prod=False)

if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)

    app.run(debug=True, port=3000)
