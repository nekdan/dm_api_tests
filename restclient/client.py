import curlify
import structlog
import uuid
from requests import Session, JSONDecodeError

from restclient.configuration import Configuration


class RestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.headers = configuration.headers
        self.disable_log = configuration.disable_log
        self.session = Session()
        self.log = structlog.get_logger(__name__).bind(service='api')

    def post(self, endpoint, **kwargs):
        return self._send_request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._send_request('PUT', endpoint, **kwargs)

    def get(self, endpoint, **kwargs):
        return self._send_request('GET', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._send_request('DELETE', endpoint, **kwargs)

    def _send_request(self, method, endpoint, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + endpoint

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)
        print(curl)
        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response),
        )
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
