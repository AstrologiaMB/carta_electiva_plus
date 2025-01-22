#python built in
import json
from datetime import datetime
import csv
import sys
import os
#third party
from immanuel import charts
from immanuel.const import chart, dignities
from immanuel.classes.serialize import ToJSON
from immanuel.setup import settings
import pandas as pd
import numpy as np

#yours
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from astro_package.settings_astro import *

#run your settings
astro_avanzada_settings()

#Clase para todas las preguntas asociadas a aspectos
