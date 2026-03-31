from django import forms
from .models import DiagnosticoGenerador


class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoGenerador
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 estilo general
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # 🧠 PREGUNTAS
        self.fields['placas'].label = "¿El generador eléctrico cuenta con todas las placas de identificación y especificaciones técnicas legibles?"
        self.fields['nivel_aceite'].label = "¿En qué condición se encuentra el nivel de aceite lubricante del motor del generador?"
        self.fields['ruido'].label = "Describa cualquier ruido, vibración o anomalía detectada durante el funcionamiento del generador."
        self.fields['horometro'].label = "Indique la lectura actual del horómetro del generador (horas de operación acumuladas)."
        self.fields['enfriamiento'].label = "El sistema de enfriamiento del generador (radiador y ventiladores) está libre de obstrucciones y fugas."
        self.fields['foto'].label = "Capture una fotografía del panel de control mostrando los indicadores de voltaje, frecuencia y corriente durante la operación."
        self.fields['estructura'].label = "Estado general de la estructura metálica"
        self.fields['oxidacion'].label = "Describa ubicaciones de puntos críticos de oxidación (base, soportes, esquineros)"
        self.fields['cableado'].label = "Indique el estado del cableado eléctrico visible"
        self.fields['tablero'].label = "Indique el estado del tablero de control"
        self.fields['aceite'].label = "Nivel y aspecto del aceite"
        self.fields['filtro_aceite'].label = "Estado del filtro de aceite"
        self.fields['filtro_aire'].label = "Estado del filtro de aire"
        self.fields['filtro_combustible'].label = "Estado del filtro de combustible"
        self.fields['escape'].label = "Estado del sistema de escape (tubos, silenciador y uniones)"
        self.fields['bateria'].label = "Estado de la batería y bornes"
        self.fields['arranca'].label = "¿Arranca el motor?"

        # 🔥 NUEVOS CAMPOS
        self.fields['marca'].label = "Marca del generador"
        self.fields['modelo'].label = "Modelo del generador"
        self.fields['tecnico'].label = "Nombre del técnico"
        self.fields['informacion_extra'].label = "Información adicional / observaciones"

    # 🔥 VALIDACIÓN GENERAL (NO VACÍOS)
    def clean(self):
        cleaned_data = super().clean()

        for campo, valor in cleaned_data.items():
            if campo not in ['informacion_extra', 'foto']:  # opcionales
                if valor in [None, '', []]:
                    self.add_error(campo, 'Este campo es obligatorio.')

        return cleaned_data

    # 🔥 VALIDACIÓN HORÓMETRO (SOLO NÚMEROS)
    def clean_horometro(self):
        valor = self.cleaned_data.get('horometro')

        if valor is None:
            raise forms.ValidationError("Este campo es obligatorio.")

        if valor < 0:
            raise forms.ValidationError("No puede ser negativo.")

        return valor

    # 🔥 VALIDACIÓN TÉCNICO (SIN NÚMEROS)
    def clean_tecnico(self):
        valor = self.cleaned_data.get('tecnico')

        if not valor:
            raise forms.ValidationError("Este campo es obligatorio.")

        if any(char.isdigit() for char in valor):
            raise forms.ValidationError("No debe contener números.")

        return valor

    # 🔥 VALIDACIÓN MARCA
    def clean_marca(self):
        valor = self.cleaned_data.get('marca')

        if not valor:
            raise forms.ValidationError("Este campo es obligatorio.")

        return valor

    # 🔥 VALIDACIÓN MODELO
    def clean_modelo(self):
        valor = self.cleaned_data.get('modelo')

        if not valor:
            raise forms.ValidationError("Este campo es obligatorio.")

        return valor