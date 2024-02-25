from requests import session, get, Session
from re import findall, search
from urllib.parse import unquote
from random import choice
from time import sleep
from fake_useragent import UserAgent

class MailService:
    def __init__(self) -> None:
        self.session = session()
        
    def create_email(self, proxy: dict = None) -> str:
        self.session.proxies.update(proxy) if proxy else ''

        res = self.session.get('https://email-fake.com/').text

        email: str = search(r'id="email_ch_text">(.*)</span>', res).group(1)
        self.session.cookies.update({'surl': '/'.join(email.split('@')[::-1])})

        return email

    def get_mail(self) -> str:
        while True:
            try: return search(r'<a href="(.*)" style="color: #3366cc" rel="nofollow" target="_blank">', self.session.get('https://email-fake.com/').text).group(1) # url validation
            except: continue


class Clictune:
    def __init__(self) -> None:
        self.headers = {
            'accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'connection'     : 'keep-alive',
            'host'           : 'www.clictune.com',
            'referer'        : 'https://clictune.com/',
            'user-agent'     :  UserAgent().chrome
            }
        

    def register(self) -> tuple[str, str] or False:
        sess = session()
        sess.get('https://www.clictune.com/auth/signup')

        infos = get('https://random-data-api.com/api/v2/users').json()

        mailservice = MailService()
        email = mailservice.create_email()

        data = {
            'email'                     : email,
            'password'                  : infos['password'],
            'password_conf'             : infos['password'],
            'prefix'                    : choice(['Mr', 'Ms']),
            'last_name'                 : infos['last_name'],
            'first_name'                : infos['first_name'],
            'dob'                       : infos['date_of_birth'],
            'type'                      : 'private',
            'company_name'              : infos['username'].replace('.', ''),
            'address[address]'          : infos['address']['street_address'],
            'address[postal_code]'      : infos['address']['zip_code'],
            'address[city]'             : infos['address']['city'],
            'address[countrycode]'      : 'FR',
            'language'                  : '5746e28a552aca6ed18b456e',
            'address[dialCode]'         : '33',
            'telephone[number]'         : '0638463000',
            'electronic_address[skype]' : '',
            'agree'                     : '1',
            'referer'                   : 'https://clictune.com/'
        }

        response = sess.post('https://www.clictune.com/auth/signup', data=data, allow_redirects=False)

        if "Earn money with your links" in response.text: 
            return False

        elif response.status_code == 303 and get(mailservice.get_mail(), allow_redirects=True).status_code == 200: 
            return email, infos['password']
        
        return False

    def login(self, email: str, password: str) -> bool:
        sess = session()
        response = sess.get('https://www.clictune.com/auth/login', headers=self.headers).text

        sess.headers.update({'referer': 'https://www.clictune.com/auth/login'})

        values = dict(findall(r'<input type="submit" name="(.*)" class="button" value="(.*)" />', response))

        _response_ = sess.post('https://www.clictune.com/auth/login', data=values | {'email': email, 'password': password, 'submit': 'Login'}).text

        if email in _response_:
            self.loged = sess
            return True
        
        return False

    def create_links(self, urls: list, time_per_url: int = 1) -> dict:
        """
        return {link: id}
        """

        self.loged.headers.update({'referer': 'https://www.clictune.com/links/index'})

        data = {
            'link': '\n'.join(urls * time_per_url),
            'validate': 'Valider'
        }
        self.loged.post('https://www.clictune.com/links/index', data=data)
        
        response = self.loged.get('https://www.clictune.com/links/index').text

        return dict(zip(findall(r'<a target="blank" href="(.*)">', response), findall(r'<form method="post" action="(.*)">', response)))

    def delete_links(self, ids: list) -> bool:
        self.loged.headers.update({'referer': 'https://www.clictune.com/links/index'})

        try: self.loged.post('https://www.clictune.com/links/delete', data={'id': ','.join(ids)})
        except: return False
        
        return True
    
    def get_profit(self) -> float or False:
        self.loged.headers.update({'referer': 'https://www.clictune.com/auth/dash'})
        try: return float(findall(r'Vous avez (.*) EUR dans votre compte.', self.loged.get('https://www.clictune.com/auth/dash').text)[-1])
        except: return False

    def earn(self, links: list, proxy=None) -> bool:
        try:
            for link in links:
                headers = {'user-agent': UserAgent().chrome}
                res = get(link, proxies=proxy if proxy else None, headers=headers, timeout=10)

                if res.status_code == 403:
                    return False
                
                path: str = findall(r'<iframe src="(.*)" frameborder="0">', res.text)[0] + choice(['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY']).lower()
                cook = res.cookies.get_dict()

                get(f'https://www.dlink2.com{path}', cookies=cook, proxies=proxy if proxy else None, headers=headers, timeout=10)

                sleep(10)

                res = get(unquote(findall(r'<a href="(.*)"', res.text)[-1]), cookies=cook, proxies=proxy if proxy else None, headers=headers, timeout=10)
                
                return True

        except: return False

