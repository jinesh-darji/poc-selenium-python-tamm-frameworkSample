from hamcrest import assert_that


class SoftAssert:
    verification_errors = []

    @staticmethod
    def soft_assert(condition, message):
        if not condition:
            SoftAssert.verification_errors.append(message)

    @staticmethod
    def final_assert():
        assert_that(len(SoftAssert.verification_errors) == 0, "\n".join(SoftAssert.verification_errors))
        SoftAssert.verification_errors.clear()
