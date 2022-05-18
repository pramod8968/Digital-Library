from distutils.log import error


securefilename error

Inside flask_uploads change the werkzeug to following

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage