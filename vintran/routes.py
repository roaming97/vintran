import datetime
import hashlib
import io
import logging
import mimetypes
import random
from string import ascii_letters, digits

from flask import flash, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename

from vintran import app, db
from vintran.forms import FileDownloadForm, FileUploadForm
from vintran.models import VintranFile


@app.route("/", methods=["GET", "POST"])
def upload(file_id: str = None):
    form = FileUploadForm()

    if request.method == "POST":
        ipv4 = request.remote_addr
        if "file" not in request.files:
            flash("No file part found in request.files", "warning")
            return redirect(request.url)
        file = request.files["file"]
        if not file.filename:
            flash("Select a file before uploading", "warning")
            return redirect(request.url)
        if file:
            if form.validate_on_submit():
                try:
                    filename = secure_filename(file.filename)
                    mimetype = mimetypes.guess_type(filename)[0]
                    buffer = file.stream.read()
                    file_hash = hashlib.sha3_256(buffer).hexdigest()
                    file_id = "".join(
                        [random.choice(f"{ascii_letters}{digits}") for _ in range(8)]
                    )
                    expiration = datetime.datetime.now() + datetime.timedelta(days=1)
                    data = VintranFile(
                        filename=filename,
                        mimetype=mimetype,
                        file_id=file_id,
                        file_hash=file_hash,
                        ipv4=ipv4,
                        buffer=buffer,
                        expiration=expiration,
                    )
                    logging.debug(data)
                    db.session.add(data)
                    db.session.commit()
                    flash("File uploaded successfully!", "success")
                except Exception as e:
                    flash(f"File upload error: {e}", "error")
                    logging.error(e)
                    return redirect(request.url)
            else:
                flash("Form was not validated", "error")
                return redirect(request.url)

    return render_template("index.html", home=True, form=form, file_id=file_id)


@app.route("/<id>", methods=["GET", "POST"])
def download(id: str):
    form = FileDownloadForm()

    file = db.one_or_404(db.select(VintranFile).filter_by(file_id=id))
    until = (
        datetime.datetime.strptime(file.expiration, "%Y-%m-%d %H:%M:%S.%f")
        - datetime.datetime.now()
    ).total_seconds()
    hours_until = round(until // 3600)
    minutes_until = round(until // 60 % 60)
    time_until = ""
    if hours_until:
        time_until += f"{hours_until} hours"
    if minutes_until:
        time_until += f", {minutes_until} minutes"
    if minutes_until <= 0 and hours_until <= 0:
        time_until = f"any moment now!"
    if request.method == "POST":
        return send_file(
            path_or_file=io.BytesIO(file.buffer),
            download_name=file.filename,
            as_attachment=True,
            mimetype=file.mimetype,
        )
    else:
        return render_template("download.html", file=file, until=time_until, form=form)


@app.route("/tos")
def tos():
    return render_template("tos.html")
