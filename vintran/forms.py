from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class FileUploadForm(FlaskForm):
    file = FileField("File", validators=[FileRequired()])
    submit = SubmitField("Upload")


class FileDownloadForm(FlaskForm):
    submit = SubmitField("Download")
