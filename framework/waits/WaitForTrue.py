class WaitForTrue(object):
    def __init__(self, browser, expression):
        self.browser = browser
        self.expression = expression

    def __call__(self, driver):
        try:
            return self.expression()
        except Exception:
            return False
