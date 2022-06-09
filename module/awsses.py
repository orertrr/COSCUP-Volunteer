''' AWS SDK API Integration

Integration `S3.client`, `SES.client`

'''
from email import encoders
from email.charset import Charset
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from os.path import basename
from typing import Any

import boto3  # type:ignore


class AWSS3:
    ''' AWSS3

    Attributes:
        aws_access_key_id (str): aws_access_key_id.
        aws_secret_access_key (str): aws_secret_access_key.
        bucket (str): bucket name.

    '''
    __slots__ = ('client', 'bucket')

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, bucket: str) -> None:
        self.client = boto3.client('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   )
        self.bucket = bucket

    def get_object(self, key: str) -> Any:
        ''' Get object

        Args:
            key (str): Object key.

        Returns:
            Return the object. -> [S3.Client.get_object][]

        '''
        return self.client.get_object(Bucket=self.bucket, Key=key)

    def convert_to_attachment(self, key: str) -> MIMEBase:
        ''' Convert the object to match attachment

        Args:
            key (str): Object key.

        Returns:
            Get the object and turn into attachment format to use.

        '''
        s3object = self.get_object(key)
        attachment = MIMEBase(
            s3object['ContentType'].split('/')[0],
            f'''{s3object['ContentType'].split('/')[1]}; name="{Charset('utf-8').header_encode(basename(key))}"'''  # pylint: disable=line-too-long
        )
        attachment.add_header(
            'Content-Disposition',
            f'''attachment; filename="{Charset('utf-8').header_encode(basename(key))}"''')
        attachment.set_payload(s3object['Body'].read())
        encoders.encode_base64(attachment)

        return attachment


class AWSSES:
    ''' AWSSES

    Attributes:
        aws_access_key_id (str): aws_access_key_id.
        aws_secret_access_key (str): aws_secret_access_key.
        source (dict): `{'name': <str>, 'mail': <str>}`, for mail `FROM`.

    '''

    __slots__ = ('client', 'source')

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str,
                 source: dict[str, str]) -> None:
        self.client = boto3.client('ses',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name='us-east-1')
        self.source = source

    @staticmethod
    def format_mail(name: str, mail: str) -> str:
        ''' Encode the `user`, `mail` to base64 for Email-Headers format.

            Args:
                name (str): name.
                mail (str): mail address.

            Returns:
                Return the excoded string.

        '''
        if name:
            return formataddr((name, mail))

        return mail

    def send_email(self, *args: Any, **kwargs: Any) -> Any:
        ''' Send mail

        ``*args``, ``**kwargs`` are the same with [SES.Client.send_email][]

        See Also:
            [SES.Client.send_email][]

        '''
        return self.client.send_email(*args, **kwargs)

    def raw_mail(self, **kwargs: Any) -> Any:
        ''' To make raw mail content

        :param list to_addresses: to
        :param str subject: subject
        :param str body: body
        :param str text_body: body format in text
        :param str x_coscup: (optional) for mail header ``X-Coscup``
        :param list cc_addresses: (optional) cc
        :param list attachment: (optional) attachment
        :param str list_unsubscribe: (Optional) url for unsubscribe

        :rtype: :py:class:`email.mime.multipart.MIMEMultipart`

        '''
        msg_all = MIMEMultipart('mixed')

        msg_all['From'] = self.format_mail(
            self.source['name'], self.source['mail'])

        to_list = []
        for to_user in kwargs['to_addresses']:
            to_list.append(self.format_mail(to_user['name'], to_user['mail']))
        msg_all['To'] = ','.join(to_list)

        cc_list = []
        if 'cc_addresses' in kwargs and kwargs['cc_addresses']:
            for cc_user in kwargs['cc_addresses']:
                cc_list.append(self.format_mail(
                    cc_user['name'], cc_user['mail']))

            if cc_list:
                msg_all['Cc'] = ','.join(cc_list)

        msg_all['Subject'] = kwargs['subject']

        if 'x_coscup' in kwargs and kwargs['x_coscup']:
            msg_all['X-Coscup'] = kwargs['x_coscup']

        if 'list_unsubscribe' in kwargs and kwargs['list_unsubscribe']:
            msg_all['List-Unsubscribe'] = kwargs['list_unsubscribe']

        body_mine = MIMEMultipart('alternative')

        if 'text_body' in kwargs and kwargs['text_body']:
            body_mine.attach(MIMEText(kwargs['text_body'], 'plain', 'utf-8'))

        body_mine.attach(MIMEText(kwargs['body'], 'html', 'utf-8'))

        msg_all.attach(body_mine)

        if 'attachment' in kwargs and kwargs['attachment']:
            for attach in kwargs['attachment']:
                msg_all.attach(attach)

        return msg_all

    def send_raw_email(self, **kwargs: Any) -> Any:
        ''' send raw email

        if no ``data``, must have ``from``, ``to``, ``subject``, ``body``, ``attachment``

        :param str source: (optional) from
        :param str to_addresses: (optional) to
        :param str subject: (optional) subject
        :param str body: (optional) body
        :param list attachment: (optional) attachment
        :param data: (optional) MIMEMultipart data
        :param data_str: (optional) MIMEMultipart to str data
        :type data: :py:class:`email.mime.multipart.MIMEMultipart`

        .. seealso::
            :meth:`SES.Client.send_raw_email`

        '''
        if 'data_str' in kwargs:
            return self.client.send_raw_email(
                RawMessage={'Data': kwargs['data_str']})

        data = kwargs.get('data')
        if not data:
            data = self.raw_mail(**kwargs)

        return self.client.send_raw_email(
            RawMessage={'Data': data.as_string()})
