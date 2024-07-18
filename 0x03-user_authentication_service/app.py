#!/usr/bin/env python3
"""
A basic flask app with user authentication.
"""
from flask import Flask, jsonify, redirect, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET '/'
    Return: The home page's payload.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
