from .models import Settings

class Generals:

    def getSettingParammeter(variable):
        val = Settings.objects.filter(variable_name=variable).first().variable_value

        return val