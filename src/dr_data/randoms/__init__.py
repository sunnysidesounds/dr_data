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
    """
    Class that produces random data
    """
    @staticmethod
    def get_hash(length):
        """
        Creates a random hash value
        :param length: length of the hadh
        :type length: str
        :return: string hash
        :rtype: str
        """
        choices = '0123456789abcdefghijklmnopqrstuvwxyz'
        results = ''.join(random.choice(choices) for i in range(length))
        return results

    @staticmethod
    def get_datetime(min_year=1900, max_year=datetime.now().year):
        """
        Creates a random Datetime value
        :param min_year: Minimum years to start at, default is 1900
        :type min_year: int
        :param max_year: Maximum years to end at, default is current date
        :type max_year: int
        :return: Datetime
        :rtype: Datetime
        """
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    @staticmethod
    def get_datetime_with_timezone(min_year=1900, max_year=datetime.now().year):
        """
        Creates a random Datetime value with timezone
        :param min_year: Minimum years to start at, default is 1900
        :type min_year: int
        :param max_year: Maximum years to end at, default is current date
        :type max_year: int
        :return: Datetime
        :rtype: Datetime
        """
        start = datetime(min_year, 1, 1, 00, 00, 00, tzinfo=timezone.utc)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        return start + (end - start) * random.random()

    @staticmethod
    def get_number():
        """
        Creates a random number value
        :return: string number
        :rtype: str
        """
        return str(random.randint(1, 999))

    @staticmethod
    def get_boolean():
        """
        Creates a random boolean value
        :return: Boolean
        :rtype: bool
        """
        return random.choice([True, False])

    @staticmethod
    def get_value_from_list(selected_list):
        """
        Gets random value from list
        :param selected_list: The list to select the random item
        :type selected_list: list[str]
        :return: Value from the list
        :rtype: str
        """
        return random.choice(selected_list)

    @staticmethod
    def get_custom_text(column_name):
        """
        Creates custom text values based on the column type
        :param column_name: Name of the column
        :type column_name: str
        :return: string value
        :rtype: str
        """
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
