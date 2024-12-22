from datetime import datetime, timezone


class DatetimeUtil:

    @staticmethod
    def get_str_datetime(exp_format):
        return datetime.now().strftime(exp_format)

    @staticmethod
    def get_current_time(offset_from_utc=0, date_time_format="%H:%M"):
        utc_dt = datetime.now(timezone.utc)
        dt = utc_dt.replace(hour=utc_dt.time().hour + offset_from_utc)
        return dt.strftime(date_time_format)
