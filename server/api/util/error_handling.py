class SecurityError(Exception):
    def error_msg(self):
        return "Security Error"