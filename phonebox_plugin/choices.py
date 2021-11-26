from utilities.choices import ChoiceSet
from django.db.models import Q


class VoiceCircuitTypeChoices(ChoiceSet):
    SIP_TRUNK = 'sip_trunk'
    DIGITAL_VOICE_CIRCUIT = 'digital_voice_circuit'
    ANALOG_VOICE_CIRCUIT = 'analog_voice_circuit'
    CHOICES = (
        (SIP_TRUNK, 'SIP Trunk'),
        (DIGITAL_VOICE_CIRCUIT, 'Digital Voice Circuit'),
        (ANALOG_VOICE_CIRCUIT, 'Analog Voice Circuit'),
    )


VOICE_CIRCUIT_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='interface') |
    Q(app_label='virtualization', model='vminterface')
)
