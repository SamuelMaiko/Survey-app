from django.contrib.auth.tokens import PasswordResetTokenGenerator

class Token(PasswordResetTokenGenerator):
    
    def _make_token_value(self, user, timestamp):
        return str(user.pk) + str(timestamp)
    

generate_token=Token()