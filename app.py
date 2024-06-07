from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 
    # every time you make a change to your Python code, it will automatically rerun the flask web server
    # app.run(debug=True, port=...)