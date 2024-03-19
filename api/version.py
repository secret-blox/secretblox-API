import os
from flask import jsonify
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'sb.env'))

sb_version = os.getenv('SECRET_BLOX_VERSION')
sb_branch = os.getenv('SECRET_BLOX_MAIN')
sb_update = os.getenv('SECRET_BLOX_FORCE_UPDATE')


def secret_blox_bootstrapper():
    return jsonify({"version": sb_version, "branch": sb_branch, "updating": sb_update})