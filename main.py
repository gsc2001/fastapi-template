"""
    :author: gsc2001
    :brief: Sample FastAPI app with mongoDB
"""

from app import app


def main():
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
