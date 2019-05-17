import traceback
from tinydb import TinyDB, where
from rauth import OAuth2Service, OAuth2Session
from datetime import datetime
import requests
import logging
import jsoncfg

# <editor-fold desc="Logging definitions">
from colorlog import ColoredFormatter

log = logging.getLogger(__name__)
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
# </editor-fold>

db = TinyDB('instance/db/sessions.json', default_table='site_sessions')
config = jsoncfg.load_config('config/wordpress.json')


class Oauth2:
    def __init__(self):
        self.oauth2 = OAuth2Service(
            name=config.oauth2.appname(),
            client_id=config.oauth2.client_id(),
            client_secret=config.oauth2.client_secret(),
            access_token_url=config.oauth2.accessurl(),
            authorize_url=config.oauth2.authorizeurl(),
            base_url=config.oauth2.siteaddress())
        self.redirect = config.oauth2.redirect()

        self.oauth2session = OAuth2Session(
            client_id=config.oauth2.client_id(),
            client_secret=config.oauth2.client_secret(),
            access_token=self.get_access_token())

    def get_access_token(self):
        session = db.get(where('sitename') == config.siteconnection())
        if session:
            if session['settings'][0] is not None:
                return session['settings'][0]['access_token']
            else:
                log.warning('WordPress site connection is enabled but does not have a saved session! '
                            'Please run the WordPress setup.')
                return 'none'
        else:
            log.warning('WordPress site connection is enabled but does not have a saved session! '
                        'Please run the WordPress setup.')
            return 'none'

    def oauth_request(self):
        params = {
            'response_type': 'code',
            'client_id': self.oauth2.client_id,
            'redirect_uri': self.redirect
        }
        url = self.oauth2.base_url + self.oauth2.get_authorize_url(**params)
        return url

    def oauth_authorize(self, code):
        parameters = {
            'redirect_uri': self.redirect,
            'code': code,
            'grant_type': 'authorization_code',
        }
        response = requests.post(
            self.oauth2.base_url + self.oauth2.access_token_url,
            auth=(
                config.oauth2.client_id(),
                config.oauth2.client_secret(),
            ),
            data=parameters,
        )
        return response

    def oauth_access(self, response):
        access_token = response.json().get('access_token')
        self.oauth_store_token(response)
        return access_token

    def oauth_store_token(self, session):
        if session:
            try:
                db.upsert({
                    'sitename': config.siteconnection(),
                    'settings': [
                        {'session_type': 'oauth2',
                         'token_type': session.json().get('token_type'),
                         'access_token': session.json().get('access_token'),
                         'refresh_token': session.json().get('refresh_token'),
                         'client_key': self.oauth2.client_id,
                         'client_secret': self.oauth2.client_secret,
                         'token_date': str(datetime.now().strftime("%Y-%m-%d"))}
                    ]
                }, where('sitename') == config.siteconnection())
            except Exception as e:
                traceback.print_exc()
        else:
            return log.error('Could not add entry to sessions file.')

    def oauth_query(self, query, payload):
        r = requests.get(
            self.oauth2.base_url + query % payload,
            headers={
                'Authorization': 'Bearer %s' % self.oauth2session.access_token
            }
        )
        response = r.text
        return response

    def oauth_post(self, query, *payload):
        email = payload[0]
        r = requests.get(
            self.oauth2.base_url + 'wp-json/instance/v1/email/%s' % email,
            headers={
                'Authorization': 'Bearer %s' % self.oauth2session.access_token
            }
        )
        data = jsoncfg.loads(r.text)
        id = data['id']
        if id is not 'null':
            if 'administrator' in data['roles']:
                return 'This account can not be modified'
            else:
                payloadroles = []
                for role in data['roles']:
                    payloadroles.append(role)
                payloadroles.append(payload[1])
                update = {'roles': payloadroles}
                r = requests.post(
                    self.oauth2.base_url + query % id, json=update,
                    headers={
                        'Authorization': 'Bearer %s' % self.oauth2session.access_token
                    }
                )
                return r
        else:
            response = email + ' could not be located.'
            return response

    def delete_wpsession(self, settings):
        if settings:
            try:
                for entry in settings[0]['settings']:
                    print(entry[0])
                    print(settings[0]['settings'])
                    del (settings[0]['settings'][0])
                db.update(settings[0], eids=[settings.eid])
                return 'Deletion Completed'
            except:
                return 'Deletion Failed'
        else:
            return 'No invoice found.'