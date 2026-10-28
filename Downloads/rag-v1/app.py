import logging
from typing import Annotated

from flask import Flask, jsonify, render_template, request
from pydantic import BaseModel, Field, StringConstraints, ValidationError
from werkzeug.exceptions import HTTPException

from rag_core import (
    EMBEDDING_MODEL,
    RagError,
    Settings,
    add_doc,
    ask,
    list_docs,
    load_settings,
    rebuild_all,
    remove_doc,
)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


class DocRequest(BaseModel):
    name: str
    content: str


class AskRequest(BaseModel):
    question: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)]
    docs: list[str] = Field(min_length=1)
    top_k: int = Field(ge=1, le=20)


def body_or_400() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise RagError(400, "invalid_request", "Invalid JSON body.")
    return data


def validate(model, data):
    try:
        return model.model_validate(data)
    except ValidationError as e:
        first = e.errors()[0]
        field = ".".join(str(x) for x in first["loc"])
        raise RagError(400, "invalid_request", f"{field}: {first['msg']}")


@app.errorhandler(RagError)
def handle_rag_error(e):
    return jsonify({"error": e.code, "message": e.message}), e.status


@app.errorhandler(413)
def handle_too_large(e):
    return jsonify({"error": "invalid_request", "message": "The request is too large (max 5 MB)."}), 413


@app.errorhandler(Exception)
def handle_unexpected(e):
    if isinstance(e, HTTPException):
        return e
    app.logger.exception("unexpected error")
    return jsonify({"error": "internal_error", "message": "Internal error."}), 500


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/docs")
def docs_list():
    return jsonify({"docs": list_docs(), "settings": load_settings().model_dump(), "model": EMBEDDING_MODEL})


@app.post("/api/docs")
def docs_add():
    req = validate(DocRequest, body_or_400())
    chunks = add_doc(req.name, req.content)
    return jsonify({"name": req.name, "chunks": chunks})


@app.delete("/api/docs/<name>")
def docs_delete(name):
    remove_doc(name)
    return jsonify({"deleted": name})


@app.post("/api/reindex")
def reindex():
    settings = validate(Settings, body_or_400())
    return jsonify({"chunks": rebuild_all(settings)})


@app.post("/api/ask")
def ask_route():
    req = validate(AskRequest, body_or_400())
    return jsonify(ask(req.question, req.docs, req.top_k))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)