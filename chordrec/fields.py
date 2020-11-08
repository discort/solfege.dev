from webargs import fields, ValidationError


def validate_file(file):
    if not file.filename.lower().endswith(('.mp3', '.wav')):
        raise ValidationError("Unsupported file format")


annotation_args = {"file": fields.Field(required=True, validate=lambda x: validate_file(x))}
