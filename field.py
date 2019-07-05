

class Field:

    """
    Object that stores all needed field data that is parsed
    from multipart/form-data, application/x-www-form-urlencoded,
    or get data.
    """

    def __init__(self, field_name, field_data, content_type=None):
        """
        Assigns all provided arguments to class.
        :param field_name: Field name, usually 'name' of the 'input'.
        :param field_data: Field data, decoded.
        :param content_type: Content type of HTTP response.
        """
        self.field_name = field_name
        self.field_data = field_data
        self.content_type = content_type

    def get_field_name(self):
        """
        :return: Field name. Type: string
        """
        return self.field_name

    def get_file_data(self):
        """
        :return: Field data. Type: string
        """
        return self.field_data

    def get_content_type(self):
        """
        :return: HTTP response content type. Type: string
        """
        return self.content_type

    def __repr__(self):
        return "<Field ({}:{})>".format(self.get_field_name(), self.get_file_data())
