import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from faker.providers import person, file, internet, phone_number

fake = Faker()
fake.add_provider(person)
fake.add_provider(file)
fake.add_provider(internet)
fake.add_provider(phone_number)


class Randoms:
    @staticmethod
    def get_hash(length):
        choices = '0123456789abcdefghijklmnopqrstuvwxyz'
        results = ''.join(random.choice(choices) for i in range(length))
        return results

    @staticmethod
    def get_datetime(min_year=1900, max_year=datetime.now().year):
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    @staticmethod
    def get_datetime_with_timezone(min_year=1900, max_year=datetime.now().year):
        start = datetime(min_year, 1, 1, 00, 00, 00, tzinfo=timezone.utc)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    @staticmethod
    def get_number():
        return str(random.randint(1, 999))

    @staticmethod
    def get_boolean():
        return random.choice([True, False])

    @staticmethod
    def get_value_from_list(selected_list):
        return random.choice(selected_list)

    @staticmethod
    def get_custom_text(column_name):
        column_name = str(column_name).lower()
        if column_name == 'first_name' or column_name == 'firstname':
            return fake.first_name()
        elif column_name == 'last_name' or column_name == 'lastname':
            return fake.last_name()
        elif column_name == 'phone_number' or column_name == 'phonenumber':
            return fake.phone_number()
        elif column_name == 'file_name' or column_name == 'filename':
            fake_files = [fake.file_path(depth=5, extension='csv'),
                          fake.file_path(depth=5, extension='txt'),
                          fake.file_path(depth=5, extension='bat')]
            return Randoms.get_value_from_list(fake_files)
        elif column_name == 'uri':
            return fake.uri()
        else:
            return Randoms.get_hash(25)