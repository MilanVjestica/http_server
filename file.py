from os import path, mkdir

class File:

    """
    Object that stores all needed file data that is parsed
    from multipart/form-data response.
    """

    def __init__(self, field_name, file_name, file_content_type, file_data, content_type):
        """
        Assigns all provided arguments to class.
        :param field_name: Field name, usually 'name' of the 'input'.
        :param file_name: Name of the sent file.
        :param file_content_type: Content type of file.
        :param file_data: Raw file data, do not decode.
        :param content_type: Content type of HTTP response.
        """
        self.field_name = field_name
        self.file_name = file_name
        self.file_content_type = file_content_type
        self.file_data = file_data
        self.content_type = content_type

    def get_field_name(self):
        """
        :return: Field name. Type: string
        """
        return self.field_name

    def get_file_name(self):
        """
        :return: Filename. Type: string
        """
        return self.file_name

    def get_file_content_type(self):
        """
        :return: File content type. Type: string
        """
        return self.file_content_type

    def get_file_data(self):
        """
        :return: Raw/binary file data. Type: binary string
        """
        return self.file_data

    def get_content_type(self):
        """
        :return: HTTP response content type. Type: string
        """
        return self.content_type

    def save_file(self, filename=None, upload_dir=None):
        """
        Saves file to provided directory.

        :param filename: Filename to save the file as. Default: filename
        :param upload_dir: Upload directory to save the file to. Default: ./
        """
        if filename is None:
            filename = self.get_file_name()
        if filename != "":
            if upload_dir is None:
                upload_dir = "./"
            if not path.isdir(upload_dir):
                mkdir(upload_dir)
            with open(upload_dir + filename, "wb") as f:
                f.write(self.get_file_data())
                f.close()

    def __repr__(self):
        return "<File ({}:{})>".format(self.get_field_name(), self.get_file_name())
