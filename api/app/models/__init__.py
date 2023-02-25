from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import app.models.User
import app.models.Atendimento
import app.models.Cidadao
import app.models.Exame
import app.models.Gestante
import app.models.IniciarConsulta
import app.models.Medicamento
import app.models.Procedimento